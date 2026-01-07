from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


              
class UserBase(BaseModel):
    email: EmailStr
    subscription_tier: str = "free"


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    last_active: Optional[datetime] = None
    churned: bool = False
    
    class Config:
        from_attributes = True


               
class EventCreate(BaseModel):
    user_id: int
    event_type: str
    event_data: Optional[Dict[str, Any]] = None
    session_duration: Optional[float] = None


class EventResponse(BaseModel):
    event_id: int
    user_id: int
    event_type: str
    event_data: Optional[Dict[str, Any]] = None
    session_duration: Optional[float] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True


                    
class PredictionRequest(BaseModel):
    user_id: int


class PredictionResponse(BaseModel):
    user_id: int
    prediction: float = Field(..., ge=0.0, le=1.0, description="Churn probability")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")
    model_version: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PredictionHistory(BaseModel):
    prediction_id: int
    user_id: int
    predicted_value: float
    confidence: float
    model_version: str
    created_at: datetime
    
    class Config:
        from_attributes = True


                   
class AnalyticsResponse(BaseModel):
    total_users: int
    active_users: int
    churned_users: int
    churn_rate: float
    avg_churn_probability: float
    model_version: str
    model_accuracy: Optional[float] = None
    total_predictions: int


class UserAnalytics(BaseModel):
    user_id: int
    email: str
    subscription_tier: str
    churned: bool
    days_since_last_active: Optional[float] = None
    total_events: int
    active_days: int
    avg_session_duration: Optional[float] = None
    latest_churn_prediction: Optional[float] = None
    
    class Config:
        from_attributes = True


                        
class ModelMetadataResponse(BaseModel):
    model_id: int
    version: str
    accuracy: Optional[float] = None
    precision_score: Optional[float] = None
    recall_score: Optional[float] = None
    f1_score: Optional[float] = None
    deployed_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
