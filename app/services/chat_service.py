from typing import Dict, Any
from app.services.intent_service import intent_service
from app.services.inventory_service import inventory_service
from app.services.attendance_service import attendance_service
from app.services.feedback_service import feedback_service
from app.models.schemas import ChatResponse


class ChatService:
    """Service for handling chat requests and generating responses"""
    
    def process_message(self, message: str) -> ChatResponse:
        """
        Process a user message and generate an appropriate response
        
        Args:
            message: User's input message
        
        Returns:
            ChatResponse with intent, response, and data
        """
        # Detect intent
        intent = intent_service.detect_intent(message)
        params = intent_service.extract_parameters(message, intent)
        
        # Route to appropriate handler based on intent
        if intent == 'inventory_query':
            return self._handle_inventory_query(params)
        elif intent == 'low_stock_alert':
            return self._handle_low_stock_alert()
        elif intent == 'attendance_stats':
            return self._handle_attendance_stats(params)
        elif intent == 'attendance_prediction':
            return self._handle_attendance_prediction()
        elif intent == 'feedback_average':
            return self._handle_feedback_average(params)
        elif intent == 'low_rating_alert':
            return self._handle_low_rating_alert()
        else:
            return self._handle_general(message)
    
    def _handle_inventory_query(self, params: Dict[str, Any]) -> ChatResponse:
        """Handle inventory-related queries"""
        item_name = params.get('item_name')
        
        if item_name:
            # Query specific item
            item = inventory_service.get_item_by_name(item_name)
            if item:
                response_text = f"Found item: {item}"
                return ChatResponse(
                    intent="inventory_query",
                    response=response_text,
                    data={"item": item}
                )
            else:
                return ChatResponse(
                    intent="inventory_query",
                    response=f"Item '{item_name}' not found in inventory",
                    data=None
                )
        else:
            # Get inventory summary
            summary = inventory_service.get_inventory_summary()
            items = inventory_service.get_all_items()
            
            response_text = f"Inventory Summary: {summary['total_items']} total items"
            if summary.get('low_stock_items', 0) > 0:
                response_text += f", {summary['low_stock_items']} items with low stock"
            
            return ChatResponse(
                intent="inventory_query",
                response=response_text,
                data={"summary": summary, "items": items[:10]}  # Limit to 10 items
            )
    
    def _handle_low_stock_alert(self) -> ChatResponse:
        """Handle low stock alert queries"""
        alerts = inventory_service.check_low_stock()
        
        if alerts:
            response_text = f"Found {len(alerts)} low stock alert(s)"
            return ChatResponse(
                intent="low_stock_alert",
                response=response_text,
                data={"alerts": [alert.dict() for alert in alerts]}
            )
        else:
            return ChatResponse(
                intent="low_stock_alert",
                response="No low stock alerts at this time. All items are adequately stocked.",
                data={"alerts": []}
            )
    
    def _handle_attendance_stats(self, params: Dict[str, Any]) -> ChatResponse:
        """Handle attendance statistics queries"""
        stats = attendance_service.get_attendance_stats(days=7)
        
        response_text = f"Attendance Statistics (last 7 days): "
        if 'avg_present' in stats:
            response_text += f"Average present: {stats['avg_present']}, "
        if 'attendance_rate_percentage' in stats:
            response_text += f"Attendance rate: {stats['attendance_rate_percentage']}%"
        
        return ChatResponse(
            intent="attendance_stats",
            response=response_text,
            data={"stats": stats}
        )
    
    def _handle_attendance_prediction(self) -> ChatResponse:
        """Handle attendance prediction queries"""
        prediction = attendance_service.predict_next_day_attendance()
        
        response_text = prediction.get('message', f"Predicted attendance: {prediction.get('predicted_attendance', 'N/A')}")
        
        return ChatResponse(
            intent="attendance_prediction",
            response=response_text,
            data={"prediction": prediction}
        )
    
    def _handle_feedback_average(self, params: Dict[str, Any]) -> ChatResponse:
        """Handle feedback average queries"""
        meal_type = params.get('meal_type')
        feedback_avg = feedback_service.get_feedback_average(days=7, meal_type=meal_type)
        
        meal_info = f" for {meal_type}" if meal_type else ""
        response_text = f"Feedback Average{meal_info} (last 7 days): {feedback_avg.get('average_rating', 0)} stars"
        
        if 'total_feedback' in feedback_avg:
            response_text += f" based on {feedback_avg['total_feedback']} feedback entries"
        
        return ChatResponse(
            intent="feedback_average",
            response=response_text,
            data={"feedback": feedback_avg}
        )
    
    def _handle_low_rating_alert(self) -> ChatResponse:
        """Handle low rating alert queries"""
        alerts = feedback_service.check_low_ratings(days=7)
        
        if alerts:
            response_text = f"Found {len(alerts)} low rating alert(s) in the last 7 days"
            return ChatResponse(
                intent="low_rating_alert",
                response=response_text,
                data={"alerts": [alert.dict() for alert in alerts]}
            )
        else:
            return ChatResponse(
                intent="low_rating_alert",
                response="No low rating alerts in the last 7 days. Food quality is satisfactory.",
                data={"alerts": []}
            )
    
    def _handle_general(self, message: str) -> ChatResponse:
        """Handle general queries"""
        return ChatResponse(
            intent="general",
            response="I can help you with inventory queries, attendance statistics, attendance predictions, feedback averages, and alerts for low stock or low ratings. What would you like to know?",
            data={
                "available_intents": [
                    "inventory_query",
                    "low_stock_alert",
                    "attendance_stats",
                    "attendance_prediction",
                    "feedback_average",
                    "low_rating_alert"
                ]
            }
        )


# Singleton instance
chat_service = ChatService()
