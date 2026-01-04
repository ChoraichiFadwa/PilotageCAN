class RiskScorer:
    """
    Implements the core business logic for CAN 2025 Risk Assessment.
    
    Philosophy:
    - White-box model: Weighted sum of normalized factors.
    - Deterministic: Same inputs always yield same score.
    - Interpretable: We can explain exactly WHY a score is high (e.g. "70% due to Traffic").
    """
    
    # Weights Configuration (Must sum to 1.0)
    WEIGHTS = {
        'affluence': 0.35,  # Crowd density is the biggest safety factor
        'meteo': 0.25,      # Weather aggravates all other risks
        'traffic': 0.20,    # Mobility issues block emergency access
        'infra': 0.20       # Infrastructure failures (lighting, gates)
    }

    # Business Thresholds
    THRESHOLDS = {
        'NORMAL': (0, 40),
        'VIGILANCE': (40, 70),
        'CRITICAL': (70, 101) # > 70
    }

    @staticmethod
    def normalize_input(value, scale_min=0, scale_max=100):
        """
        Normalizes any input to 0.0 - 1.0 scale.
        """
        if value < scale_min: return 0.0
        if value > scale_max: return 1.0
        return (value - scale_min) / (scale_max - scale_min)

    def calculate_score(self, 
                       affluence_pct, 
                       meteo_code, 
                       traffic_idx, 
                       infra_status):
        """
        Calculates the Composite Risk Score (0-100).
        
        Args:
            affluence_pct (float): 0-100 (Fill rate). >100 is treated as 1.0+ (Critical).
            meteo_code (int): 0 (Sunny) to 3 (Storm). Mapped to impact score.
            traffic_idx (int): 0-100 (Congestion Index).
            infra_status (int): 0-100 (Strain/Failure Index).
        """
        
        # 1. Normalization (Data Engineering transformation)
        norm_affluence = affluence_pct / 100.0
        
        # Meteo: Map simplified codes to severity (0-1)
        # 0=Clear, 1=Cloudy/Windy, 2=Rain, 3=Storm
        meteo_map = {0: 0.0, 1: 0.3, 2: 0.7, 3: 1.0}
        norm_meteo = meteo_map.get(meteo_code, 0.5)
        
        norm_traffic = self.normalize_input(traffic_idx, 0, 100)
        norm_infra = self.normalize_input(infra_status, 0, 100)

        # 2. Weighted Sum (The Core Model)
        raw_score_normalized = (
            (norm_affluence * self.WEIGHTS['affluence']) +
            (norm_meteo     * self.WEIGHTS['meteo']) +
            (norm_traffic   * self.WEIGHTS['traffic']) +
            (norm_infra     * self.WEIGHTS['infra'])
        )

        # 3. Scaling to 0-100
        final_score = round(raw_score_normalized * 100, 2)
        
        # Clamp to 100 max
        final_score = min(final_score, 100.0)
        
        details = {
            'components_contribution': {
                'affluence': round(norm_affluence * self.WEIGHTS['affluence'] * 100, 1),
                'meteo': round(norm_meteo * self.WEIGHTS['meteo'] * 100, 1),
                'traffic': round(norm_traffic * self.WEIGHTS['traffic'] * 100, 1),
                'infra': round(norm_infra * self.WEIGHTS['infra'] * 100, 1)
            }
        }
        
        return final_score, details

    def interpret_score(self, score):
        """
        Translates a numeric score into Business Action.
        """
        if score <= self.THRESHOLDS['NORMAL'][1]:
            return "[NORMAL]: Standard operations monitoring."
        elif score <= self.THRESHOLDS['VIGILANCE'][1]:
            return "[VIGILANCE]: Active monitoring required. Check highest contributing factor."
        else:
            return "[CRITICAL]: IMMEDIATE ACTION. Activate Emergency Response protocols."

if __name__ == "__main__":
    scorer = RiskScorer()
    
    print("--- CAN 2025 Risk Scoring Logic Verification ---")
    
    # Scenario 1: Quiet Morning
    s1 = (10, 0, 15, 0) # 10% full, Sunny, Low Traffic, OK Infra
    score1, d1 = scorer.calculate_score(*s1)
    print(f"\nScenario 1 (Quiet): Score {score1}")
    print(f"Interpretation: {scorer.interpret_score(score1)}")
    
    # Scenario 2: Match Day Congestion
    s2 = (85, 1, 90, 20) # 85% full, Windy, Gridlock, Minor infra strain
    score2, d2 = scorer.calculate_score(*s2)
    print(f"\nScenario 2 (Peak): Score {score2}")
    print(f"Breakdown: {d2}")
    print(f"Interpretation: {scorer.interpret_score(score2)}")
    
    # Scenario 3: The 'Casablanca Storm' Case (Context Ref)
    s3 = (95, 3, 80, 60) # Overcrowded, Storm, Traffic jam, Failing infra
    score3, d3 = scorer.calculate_score(*s3)
    print(f"\nScenario 3 (CRITICAL): Score {score3}")
    print(f"Breakdown: {d3}")
    print(f"Interpretation: {scorer.interpret_score(score3)}")
