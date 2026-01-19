import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.sheets_service import sheets_service
from app.config import settings
from app.models.schemas import Alert


class FeedbackService:
    """Service for managing feedback data and ratings"""
    
    def __init__(self):
        self.sheet_id = settings.feedback_sheet_id
        self.low_rating_threshold = settings.low_rating_threshold
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """
        Get all feedback records
        
        Returns:
            List of feedback records as dictionaries
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_feedback_average(self, days: int = 7, meal_type: str = None) -> Dict[str, Any]:
        """
        Get average feedback ratings
        
        Args:
            days: Number of days to include in average (default: 7)
            meal_type: Filter by meal type (optional)
        
        Returns:
            Dictionary with average rating and statistics
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return {
                "message": "No feedback data available",
                "average_rating": 0
            }
        
        # Find relevant columns
        rating_col = None
        date_col = None
        meal_type_col = None
        
        for col in ['rating', 'Rating', 'RATING', 'score', 'Score']:
            if col in df.columns:
                rating_col = col
                break
        
        for col in ['date', 'Date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        for col in ['meal_type', 'Meal Type', 'meal', 'Meal', 'type', 'Type']:
            if col in df.columns:
                meal_type_col = col
                break
        
        if not rating_col:
            return {
                "message": "Rating column not found in feedback data",
                "average_rating": 0
            }
        
        # Convert rating to numeric
        df[rating_col] = pd.to_numeric(df[rating_col], errors='coerce')
        df = df.dropna(subset=[rating_col])
        
        # Filter by date if available
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.sort_values(by=date_col, ascending=False)
                df = df.head(days * 3)  # Approximate, assuming 3 meals per day
            except:
                pass
        else:
            df = df.tail(days * 3)
        
        # Filter by meal type if specified
        if meal_type and meal_type_col:
            df = df[df[meal_type_col].str.lower() == meal_type.lower()]
        
        if df.empty:
            return {
                "message": f"No feedback data available for {meal_type}" if meal_type else "No feedback data available",
                "average_rating": 0
            }
        
        # Calculate statistics
        avg_rating = df[rating_col].mean()
        
        result = {
            "average_rating": round(avg_rating, 2),
            "total_feedback": len(df),
            "max_rating": float(df[rating_col].max()),
            "min_rating": float(df[rating_col].min()),
            "days_analyzed": days
        }
        
        if meal_type:
            result["meal_type"] = meal_type
        
        # Add rating distribution
        if len(df) > 0:
            result["rating_distribution"] = {
                "excellent (4-5)": len(df[df[rating_col] >= 4]),
                "good (3-4)": len(df[(df[rating_col] >= 3) & (df[rating_col] < 4)]),
                "average (2-3)": len(df[(df[rating_col] >= 2) & (df[rating_col] < 3)]),
                "poor (<2)": len(df[df[rating_col] < 2])
            }
        
        return result
    
    def check_low_ratings(self, days: int = 7) -> List[Alert]:
        """
        Check for meals with low ratings
        
        Args:
            days: Number of days to check (default: 7)
        
        Returns:
            List of low rating alerts
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        alerts = []
        
        # Find relevant columns
        rating_col = None
        date_col = None
        meal_type_col = None
        
        for col in ['rating', 'Rating', 'RATING', 'score', 'Score']:
            if col in df.columns:
                rating_col = col
                break
        
        for col in ['date', 'Date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        for col in ['meal_type', 'Meal Type', 'meal', 'Meal', 'type', 'Type']:
            if col in df.columns:
                meal_type_col = col
                break
        
        if not rating_col:
            return alerts
        
        # Convert rating to numeric
        df[rating_col] = pd.to_numeric(df[rating_col], errors='coerce')
        df = df.dropna(subset=[rating_col])
        
        # Filter by date if available
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.sort_values(by=date_col, ascending=False)
                df = df.head(days * 3)
            except:
                pass
        else:
            df = df.tail(days * 3)
        
        # Find low ratings
        low_ratings = df[df[rating_col] < self.low_rating_threshold]
        
        for _, feedback in low_ratings.iterrows():
            meal_info = f" for {feedback[meal_type_col]}" if meal_type_col and meal_type_col in feedback else ""
            date_info = f" on {feedback[date_col]}" if date_col and date_col in feedback else ""
            
            alerts.append(Alert(
                type="low_rating",
                message=f"Low rating alert{meal_info}{date_info}: {feedback[rating_col]} stars",
                severity="warning",
                timestamp=datetime.now().isoformat()
            ))
        
        return alerts
    
    def get_recent_feedback(self, limit: int = 10, meal_type: str = None) -> List[Dict[str, Any]]:
        """
        Get recent feedback records
        
        Args:
            limit: Maximum number of records to return
            meal_type: Filter by meal type (optional)
        
        Returns:
            List of recent feedback records
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        # Filter by meal type if specified
        meal_type_col = None
        for col in ['meal_type', 'Meal Type', 'meal', 'Meal', 'type', 'Type']:
            if col in df.columns:
                meal_type_col = col
                break
        
        if meal_type and meal_type_col:
            df = df[df[meal_type_col].str.lower() == meal_type.lower()]
        
        # Sort by date if available
        date_col = None
        for col in ['date', 'Date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.sort_values(by=date_col, ascending=False)
            except:
                pass
        
        return df.head(limit).to_dict('records')


# Singleton instance
feedback_service = FeedbackService()
