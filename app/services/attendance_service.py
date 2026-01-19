import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.services.sheets_service import sheets_service
from app.config import settings


class AttendanceService:
    """Service for managing attendance data and predictions"""
    
    def __init__(self):
        self.sheet_id = settings.attendance_sheet_id
    
    def get_all_attendance(self) -> List[Dict[str, Any]]:
        """
        Get all attendance records
        
        Returns:
            List of attendance records as dictionaries
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_attendance_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Get attendance statistics for the specified number of days
        
        Args:
            days: Number of days to include in statistics (default: 7)
        
        Returns:
            Dictionary with attendance statistics
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return {
                "message": "No attendance data available",
                "total_records": 0
            }
        
        # Try to find the relevant columns
        date_col = None
        present_col = None
        absent_col = None
        total_col = None
        
        for col in ['date', 'Date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        for col in ['present', 'Present', 'PRESENT']:
            if col in df.columns:
                present_col = col
                break
        
        for col in ['absent', 'Absent', 'ABSENT']:
            if col in df.columns:
                absent_col = col
                break
        
        for col in ['total', 'Total', 'TOTAL']:
            if col in df.columns:
                total_col = col
                break
        
        # Convert numeric columns
        if present_col:
            df[present_col] = pd.to_numeric(df[present_col], errors='coerce')
        if absent_col:
            df[absent_col] = pd.to_numeric(df[absent_col], errors='coerce')
        if total_col:
            df[total_col] = pd.to_numeric(df[total_col], errors='coerce')
        
        # Sort by date if available
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.sort_values(by=date_col, ascending=False)
                df = df.head(days)
            except:
                pass
        else:
            df = df.tail(days)
        
        # Calculate statistics
        stats = {
            "total_records": len(df),
            "days_analyzed": min(days, len(df))
        }
        
        if present_col:
            stats["avg_present"] = round(df[present_col].mean(), 2)
            stats["total_present"] = int(df[present_col].sum())
            stats["max_present"] = int(df[present_col].max())
            stats["min_present"] = int(df[present_col].min())
        
        if absent_col:
            stats["avg_absent"] = round(df[absent_col].mean(), 2)
            stats["total_absent"] = int(df[absent_col].sum())
        
        if total_col:
            stats["avg_total"] = round(df[total_col].mean(), 2)
        
        if present_col and total_col:
            attendance_rate = (df[present_col] / df[total_col] * 100).mean()
            stats["attendance_rate_percentage"] = round(attendance_rate, 2)
        
        return stats
    
    def predict_next_day_attendance(self) -> Dict[str, Any]:
        """
        Predict next day's attendance based on historical data
        Uses simple moving average for prediction
        
        Returns:
            Dictionary with prediction details
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return {
                "prediction": "Unable to predict",
                "message": "No attendance data available"
            }
        
        # Find present column
        present_col = None
        for col in ['present', 'Present', 'PRESENT']:
            if col in df.columns:
                present_col = col
                break
        
        if not present_col:
            return {
                "prediction": "Unable to predict",
                "message": "Present column not found in attendance data"
            }
        
        # Convert to numeric
        df[present_col] = pd.to_numeric(df[present_col], errors='coerce')
        df = df.dropna(subset=[present_col])
        
        if len(df) < 3:
            return {
                "prediction": "Unable to predict",
                "message": "Insufficient data for prediction (need at least 3 records)"
            }
        
        # Use last 7 days for moving average
        recent_data = df.tail(7)
        avg_attendance = recent_data[present_col].mean()
        
        # Simple trend analysis
        if len(recent_data) >= 2:
            recent_trend = recent_data[present_col].iloc[-1] - recent_data[present_col].iloc[0]
            trend_direction = "increasing" if recent_trend > 0 else "decreasing" if recent_trend < 0 else "stable"
        else:
            trend_direction = "stable"
        
        return {
            "predicted_attendance": round(avg_attendance, 0),
            "prediction_method": "7-day moving average",
            "trend": trend_direction,
            "confidence": "medium",
            "based_on_days": len(recent_data),
            "message": f"Based on last {len(recent_data)} days, predicted attendance is approximately {round(avg_attendance, 0)} students"
        }
    
    def get_today_attendance(self) -> Optional[Dict[str, Any]]:
        """
        Get today's attendance record
        
        Returns:
            Dictionary with today's attendance or None if not found
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return None
        
        # Find date column
        date_col = None
        for col in ['date', 'Date', 'DATE']:
            if col in df.columns:
                date_col = col
                break
        
        if not date_col:
            # Return most recent record
            return df.tail(1).to_dict('records')[0] if len(df) > 0 else None
        
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            today = datetime.now().date()
            today_records = df[df[date_col].dt.date == today]
            
            if not today_records.empty:
                return today_records.iloc[-1].to_dict()
        except:
            pass
        
        # Return most recent record as fallback
        return df.tail(1).to_dict('records')[0] if len(df) > 0 else None


# Singleton instance
attendance_service = AttendanceService()
