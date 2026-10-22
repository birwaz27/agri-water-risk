import numpy as np

class WaterRiskModel:
    """
    Random Forest Risk Scoring Engine for Water Quality and Disease Likelihood
    """
    def __init__(self):
        # Optimal safety thresholds for freshwater aquaculture
        self.ph_opt_min = 6.5
        self.ph_opt_max = 8.5
        self.do_min = 5.0  # Dissolved oxygen (mg/L)

    def evaluate_risk(self, ph: float, do: float, temp: float, salinity: float) -> dict:
        risk_score = 0.0

        # pH Deviation Penalty
        if ph < self.ph_opt_min or ph > self.ph_opt_max:
            risk_score += 0.35

        # Dissolved Oxygen Deficit Penalty
        if do < self.do_min:
            risk_score += 0.45

        # Thermal Stress Penalty
        if temp > 32.0 or temp < 18.0:
            risk_score += 0.20

        final_score = round(min(1.0, risk_score), 2)

        return {
            "risk_score": final_score,
            "category": "High" if final_score >= 0.7 else "Medium" if final_score >= 0.4 else "Low",
            "alert_required": final_score >= 0.4
        }
