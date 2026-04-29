import numpy as np
from typing import List

class FairnessCalculator:
    """Evaluates the starvation bounds ensuring algorithms prevent catastrophic wait allocations."""
    
    @staticmethod
    def calculate_max_starvation(waiting_times: List[int]) -> int:
        if not waiting_times: return 0
        return max(waiting_times)
        
    @staticmethod
    def calculate_jains_fairness_index(waiting_times: List[int]) -> float:
        """
        Jain's Fairness Index. J = (Sum(X))^2 / (n * Sum(X^2)).
        Yields 1.0 continuously if perfectly symmetric; lower indices denote starvation bounds natively.
        """
        if not waiting_times:
            return 1.0
            
        sum_times = sum(waiting_times)
        sum_sq_times = sum(x**2 for x in waiting_times)
        n = len(waiting_times)
        
        if sum_sq_times == 0:
            return 1.0
            
        return (sum_times ** 2) / (n * sum_sq_times)

    @staticmethod
    def evaluate_fairness_profile(waiting_times: List[int]) -> dict:
        return {
            "max_starvation_min": FairnessCalculator.calculate_max_starvation(waiting_times),
            "jains_index": FairnessCalculator.calculate_jains_fairness_index(waiting_times),
            "jfair_raw": max(waiting_times) - min(waiting_times) if waiting_times else 0
        }
