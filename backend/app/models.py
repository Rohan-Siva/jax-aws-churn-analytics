from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
                    
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True))
    subscription_tier = Column(String(50), default="free")
    churned = Column(Boolean, default=False, index=True)
    churn_date = Column(DateTime(timezone=True))


class Event(Base):
                                                
    __tablename__ = "events"
    
    event_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_data = Column(JSON)
    session_duration = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class Prediction(Base):
                                         
    __tablename__ = "predictions"
    
    prediction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    model_version = Column(String(50), nullable=False)
    prediction_type = Column(String(100), nullable=False)
    predicted_value = Column(Float, nullable=False)
    confidence = Column(Float)
    features = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class ModelMetadata(Base):
                                       
    __tablename__ = "model_metadata"
    
    model_id = Column(Integer, primary_key=True, index=True)
    version = Column(String(50), unique=True, nullable=False)
    accuracy = Column(Float)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    deployed_at = Column(DateTime(timezone=True), server_default=func.now())
    storage_path = Column(String(500))
    metrics = Column(JSON)
    is_active = Column(Boolean, default=False)
