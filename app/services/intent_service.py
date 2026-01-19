import re
from typing import Dict, Any


class IntentDetectionService:
    """Service for rule-based intent detection from user messages"""
    
    def __init__(self):
        # Define intent patterns
        self.intent_patterns = {
            'inventory_query': [
                r'\b(inventory|stock|items?|quantity|available)\b',
                r'\b(how much|how many)\b.*\b(items?|stock)\b',
                r'\b(check|show|list)\b.*\b(inventory|stock)\b',
            ],
            'low_stock_alert': [
                r'\b(low stock|running low|shortage|need to restock)\b',
                r'\b(alert|warning).*\b(stock|inventory)\b',
            ],
            'attendance_stats': [
                r'\b(attendance|present|absent)\b.*\b(stats?|statistics|count)\b',
                r'\b(how many|total).*\b(students?|people|present|absent)\b',
                r'\b(check|show|display)\b.*\b(attendance)\b',
            ],
            'attendance_prediction': [
                r'\b(predict|forecast|estimate).*\b(attendance|tomorrow|next day)\b',
                r'\b(next day|tomorrow).*\b(attendance)\b',
                r'\b(expected|likely).*\b(attendance)\b',
            ],
            'feedback_average': [
                r'\b(feedback|rating|review).*\b(average|mean|score)\b',
                r'\b(how is|what is).*\b(feedback|rating)\b',
                r'\b(check|show).*\b(feedback|rating|review)\b',
            ],
            'low_rating_alert': [
                r'\b(low rating|poor feedback|bad review)\b',
                r'\b(alert|warning).*\b(rating|feedback)\b',
            ],
            'general': []  # Fallback intent
        }
    
    def detect_intent(self, message: str) -> str:
        """
        Detect the intent of a user message using rule-based pattern matching
        
        Args:
            message: User's input message
        
        Returns:
            Detected intent as a string
        """
        message_lower = message.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            if intent == 'general':
                continue
            
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        # Default to general intent if no match
        return 'general'
    
    def extract_parameters(self, message: str, intent: str) -> Dict[str, Any]:
        """
        Extract relevant parameters from message based on intent
        
        Args:
            message: User's input message
            intent: Detected intent
        
        Returns:
            Dictionary of extracted parameters
        """
        params = {}
        message_lower = message.lower()
        
        # Extract item names for inventory queries
        if intent == 'inventory_query':
            # Try to extract item name after keywords
            item_match = re.search(r'(item|stock|inventory)\s+(of\s+)?([a-z]+)', message_lower)
            if item_match:
                params['item_name'] = item_match.group(3)
        
        # Extract date-related parameters for attendance
        if intent in ['attendance_stats', 'attendance_prediction']:
            if 'today' in message_lower:
                params['date'] = 'today'
            elif 'yesterday' in message_lower:
                params['date'] = 'yesterday'
            elif 'tomorrow' in message_lower or 'next day' in message_lower:
                params['date'] = 'tomorrow'
            else:
                params['date'] = 'today'
        
        # Extract meal type for feedback
        if intent in ['feedback_average', 'low_rating_alert']:
            if 'breakfast' in message_lower:
                params['meal_type'] = 'breakfast'
            elif 'lunch' in message_lower:
                params['meal_type'] = 'lunch'
            elif 'dinner' in message_lower:
                params['meal_type'] = 'dinner'
        
        return params


# Singleton instance
intent_service = IntentDetectionService()
