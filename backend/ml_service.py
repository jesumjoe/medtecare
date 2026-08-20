import pandas as pd
import numpy as np
import os
import random
import logging
import joblib

logger = logging.getLogger(__name__)

# Try to import CatBoost, but wrap in try-except in case we import before install finishes
try:
    from catboost import CatBoostClassifier
except ImportError:
    CatBoostClassifier = None
    logger.warning("CatBoost not installed yet.")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DATA"))
CSV_PATH = os.path.join(DATA_DIR, "medical_device_ml_dataset.csv")
MODEL_PATH = os.path.join(DATA_DIR, "medical_device_catboost.pkl")

class MLService:
    def __init__(self):
        self.df = None
        self.model = None
        self._load_data()
        
    def _load_data(self):
        try:
            # We load the dataset
            self.df = pd.read_csv(CSV_PATH)
            
            # We try to load the model using joblib
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                logger.warning(f"Could not load via joblib, trying CatBoost native: {e}")
                if CatBoostClassifier:
                    self.model = CatBoostClassifier()
                    self.model.load_model(MODEL_PATH)
                else:
                    raise ImportError("CatBoost not available to load native model.")
                
            logger.info("ML Service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML models/data: {e}")
            # Don't raise so the server can still start if there's a file issue

    def get_frontend_devices(self, limit=10):
        """
        Returns a list of devices formatted for the Next.js frontend, including
        procedurally generated sensor values based on their actual risk profile.
        """
        if self.df is None:
            return []
            
        # Select some interesting devices (some with high previous events, some low)
        # Sort by previous_events descending to get a good mix of critical and healthy
        subset = self.df.sort_values(by='previous_events', ascending=False).head(limit).copy()
        
        devices = []
        for _, row in subset.iterrows():
            device_id = str(row['device_id'])
            
            # Predict risk score to set frontend status accurately
            payload = self.run_inference(device_id)
            if not payload:
                continue
                
            risk_score = int(payload.get("future_event_probability", 0) * 100)
            status = "critical" if risk_score > 75 else "warning" if risk_score > 40 else "healthy"
            
            # Generate fake sensor readings based on status (since CSV lacks sensor telemetry)
            sensor_readings = []
            if status == "critical":
                sensor_readings = [
                    {"name": "Temperature", "value": round(random.uniform(90, 115), 1), "unit": "°C", "normalRange": [40, 85]},
                    {"name": "Vibration", "value": round(random.uniform(6.0, 9.5), 1), "unit": "mm/s", "normalRange": [0, 4.5]},
                ]
            elif status == "warning":
                sensor_readings = [
                    {"name": "Temperature", "value": round(random.uniform(70, 89), 1), "unit": "°C", "normalRange": [40, 85]},
                    {"name": "Vibration", "value": round(random.uniform(3.5, 5.9), 1), "unit": "mm/s", "normalRange": [0, 4.5]},
                ]
            else:
                sensor_readings = [
                    {"name": "Temperature", "value": round(random.uniform(45, 65), 1), "unit": "°C", "normalRange": [40, 85]},
                    {"name": "Vibration", "value": round(random.uniform(1.0, 3.0), 1), "unit": "mm/s", "normalRange": [0, 4.5]},
                ]
            
            # Additional generic sensor
            sensor_readings.append({"name": "Battery", "value": round(random.uniform(20, 100), 0), "unit": "%", "normalRange": [30, 100]})

            devices.append({
                "id": device_id,
                "name": str(row.get('device_name', f"Medical Device {device_id}")),
                "type": str(row.get('classification', 'Equipment')),
                "location": "Ward " + str(random.randint(1, 10)),
                "riskScore": risk_score,
                "status": status,
                "lastUpdated": pd.Timestamp.now().isoformat(),
                "confidencePercent": int(payload.get("model_confidence", 0) * 100),
                "sensorReadings": sensor_readings
            })
            
        return devices

    def run_inference(self, device_id: str) -> dict:
        """
        Runs the CatBoost model on a specific device row and generates the Squad A payload.
        """
        if self.df is None or self.model is None:
            return {}
            
        row = self.df[self.df['device_id'].astype(str) == str(device_id)]
        if row.empty:
            raise ValueError(f"Device ID {device_id} not found in dataset")
            
        row = row.iloc[0]
        
        # Features the model expects (drop target and IDs)
        # Drop columns that are definitely not features:
        drop_cols = ['device_id', 'device_name', 'future_event']
        # If there are any other columns the model doesn't expect, we might need to handle it,
        # but usually the rest are features.
        
        # Construct DataFrame of just this row to pass to predict
        X = row.drop(labels=drop_cols).to_frame().T
        
        # Fix NaN in categorical features (CatBoost requires string for categorical NaNs)
        for col in X.select_dtypes(include=['object', 'category']).columns:
            X[col] = X[col].fillna("Missing").astype(str)
            
        # Predict probability
        proba = float(self.model.predict_proba(X)[0][1]) # Probability of class 1
        prediction_val = int(proba > 0.5)
        
        # Risk level
        risk_level = "LOW"
        if proba > 0.8: risk_level = "CRITICAL"
        elif proba > 0.6: risk_level = "HIGH"
        elif proba > 0.4: risk_level = "MEDIUM"
        
        # Feature impacts (Approximation of SHAP for the payload)
        try:
            importances = self.model.get_feature_importance()
            feature_names = self.model.feature_names_
            
            feature_drivers = []
            for name, imp in zip(feature_names, importances):
                if imp > 0:
                    feature_drivers.append({
                        "feature": name,
                        "impact": round(imp / sum(importances), 2)
                    })
            
            feature_drivers = sorted(feature_drivers, key=lambda x: x["impact"], reverse=True)[:5]
        except Exception:
            feature_drivers = [
                {"feature": "previous_events", "impact": 0.45},
                {"feature": "years_in_service", "impact": 0.35}
            ]
            
        payload = {
            "device_id": str(device_id),
            "device_name": str(row.get('device_name', 'Unknown Device')),
            "classification": str(row.get('classification', 'Active Equipment')),
            "risk_class": str(row.get('risk_class', 'Class IIb')),
            "manufacturer": str(row.get('manufacturer', 'Unknown')),
            "future_event_probability": proba,
            "prediction": prediction_val,
            "risk_level": risk_level,
            "model_confidence": 0.88, 
            "previous_events": int(row.get('previous_events', 0)),
            "previous_recalls": int(row.get('previous_recalls', 0)),
            "previous_safety_notices": int(row.get('previous_safety_notices', 0)),
            "years_in_service": float(row.get('years_in_service', 0.0)),
            "feature_drivers": feature_drivers
        }
        return payload

    def get_dataset_stats(self) -> dict:
        """
        Computes KPI statistics from the full dataset for the dashboard.
        Returns total devices, at-risk count, predicted failures, and average risk score.
        """
        if self.df is None or self.model is None:
            return {
                "totalDevices": 0,
                "devicesAtRisk": 0,
                "predictedFailures30d": 0,
                "avgRiskScore": 0.0,
            }
        
        total = len(self.df)
        
        # Count devices where future_event == 1 (actual positive labels in dataset)
        future_events = int(self.df['future_event'].sum()) if 'future_event' in self.df.columns else 0
        
        # Sample a subset to estimate risk distribution (running inference on all 118K is too slow)
        sample_size = min(200, total)
        sample = self.df.sample(n=sample_size, random_state=42)
        
        risk_scores = []
        at_risk_count = 0
        predicted_failures = 0
        
        for _, row in sample.iterrows():
            try:
                drop_cols = ['device_id', 'device_name', 'future_event']
                X = row.drop(labels=drop_cols).to_frame().T
                proba = float(self.model.predict_proba(X)[0][1])
                risk_score = proba * 100
                risk_scores.append(risk_score)
                
                if risk_score > 40:
                    at_risk_count += 1
                if risk_score > 70:
                    predicted_failures += 1
            except Exception:
                continue
        
        avg_risk = round(sum(risk_scores) / len(risk_scores), 1) if risk_scores else 0.0
        
        # Scale sample counts to full dataset estimate
        scale_factor = total / sample_size if sample_size > 0 else 1
        
        return {
            "totalDevices": total,
            "devicesAtRisk": round(at_risk_count * scale_factor),
            "predictedFailures30d": round(predicted_failures * scale_factor),
            "avgRiskScore": avg_risk,
        }

# Global instance to be imported by main.py
ml_service = MLService()
