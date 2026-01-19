from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    intent: str
    response: str
    data: Optional[dict] = None


class InventoryItem(BaseModel):
    """Model for inventory item"""
    item_name: str
    quantity: int
    unit: str
    last_updated: Optional[str] = None


class AttendanceRecord(BaseModel):
    """Model for attendance record"""
    date: str
    present: int
    absent: int
    total: int


class FeedbackRecord(BaseModel):
    """Model for feedback record"""
    date: str
    meal_type: str
    rating: float
    comments: Optional[str] = None


class Alert(BaseModel):
    """Model for alerts"""
    type: str
    message: str
    severity: str
    timestamp: str
