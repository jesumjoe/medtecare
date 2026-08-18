"""
Squad A to Squad B Integration Layer.
Converts Squad A CatBoost prediction outputs into Squad B MLPrediction contracts.
"""

from logic.integration.squad_a_adapter import adapt_squad_a_prediction, SquadAAdapter

__all__ = ["adapt_squad_a_prediction", "SquadAAdapter"]
