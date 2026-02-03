"""
Scoring and Ranking Module
Handles airfoil scoring based on application requirements
"""
import pandas as pd
from config import APPLICATION_WEIGHTS
from utils import normalize


class AirfoilScorer:
    """Scores and ranks airfoils based on application-specific criteria"""
    
    def __init__(self, application="payload"):
        """
        Initialize scorer with application type
        
        Args:
            application: One of 'payload', 'endurance', or 'trainer'
        """
        if application not in APPLICATION_WEIGHTS:
            raise ValueError(f"Unknown application: {application}. "
                           f"Choose from {list(APPLICATION_WEIGHTS.keys())}")
        self.application = application
        self.weights = APPLICATION_WEIGHTS[application]
    
    def normalize_features(self, df):
        """
        Normalize all scoring features to [0,1] range
        
        Args:
            df: DataFrame with airfoil features
        
        Returns:
            DataFrame with normalized features
        """
        scored = df.copy()
        
        # Normalize each feature (invert CD since lower is better)
        scored["Optimum_CL_n"] = normalize(scored["Optimum_CL"])
        scored["Optimum_CD_n"] = normalize(scored["Optimum_CD"], invert=True)
        scored["MAX_CL/CD_n"] = normalize(scored["MAX_CL/CD"])
        scored["CL_max_n"] = normalize(scored["CL_max"])
        scored["CL_at_0_deg_n"] = normalize(scored["CL_at_0_deg"])
        scored["angle_diff_n"] = normalize(scored["angle_diff"])
        
        return scored
    
    def calculate_scores(self, df):
        """
        Calculate weighted scores for each airfoil configuration
        
        Args:
            df: DataFrame with normalized features
        
        Returns:
            DataFrame with scores added
        """
        df = df.copy()
        
        # Calculate weighted sum based on application
        df["score"] = sum(
            self.weights[feature] * df[feature] 
            for feature in self.weights
        )
        
        return df
    
    def rank_airfoils(self, df):
        """
        Complete scoring and ranking pipeline
        
        Args:
            df: DataFrame with airfoil features
        
        Returns:
            Ranked DataFrame sorted by score (descending)
        """
        # Normalize features
        normalized = self.normalize_features(df)
        
        # Calculate scores
        scored = self.calculate_scores(normalized)
        
        # Sort by score
        ranked = scored.sort_values("score", ascending=False).reset_index(drop=True)
        
        return ranked
    
    def get_top_n(self, df, n=10):
        """
        Get top N ranked airfoils
        
        Args:
            df: Ranked DataFrame
            n: Number of top airfoils to return
        
        Returns:
            DataFrame with top N airfoils
        """
        return df.head(n)
    
    def get_summary_columns(self):
        """Get list of key columns for summary display"""
        return [
            "airfoil_name", "Re", "Optimum_angle", "Optimum_CL", 
            "Optimum_CD", "MAX_CL/CD", "CL_max", "CL_at_0_deg",
            "stall_angle_deg", "angle_diff", "score"
        ]


def compare_applications(df, applications=["payload", "endurance", "trainer"]):
    """
    Compare airfoil rankings across different applications
    
    Args:
        df: DataFrame with airfoil features
        applications: List of application types to compare
    
    Returns:
        Dictionary with rankings for each application
    """
    results = {}
    
    for app in applications:
        scorer = AirfoilScorer(application=app)
        ranked = scorer.rank_airfoils(df)
        results[app] = ranked
    
    return results


def get_best_airfoil_per_application(df, top_n=5):
    """
    Get best airfoils for each application type
    
    Args:
        df: DataFrame with airfoil features
        top_n: Number of top airfoils per application
    
    Returns:
        Dictionary with top airfoils per application
    """
    comparison = compare_applications(df)
    
    best_per_app = {}
    for app, ranked_df in comparison.items():
        scorer = AirfoilScorer(application=app)
        top_airfoils = ranked_df[scorer.get_summary_columns()].head(top_n)
        best_per_app[app] = top_airfoils
    
    return best_per_app
