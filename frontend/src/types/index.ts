export interface User {
    user_id: number;
    email: string;
    subscription_tier: string;
    churned: boolean;
    created_at: string;
    last_active: string | null;
}

export interface UserAnalytics {
    user_id: number;
    email: string;
    subscription_tier: string;
    churned: boolean;
    days_since_last_active: number | null;
    total_events: number;
    active_days: number;
    avg_session_duration: number | null;
    latest_churn_prediction: number | null;
}

export interface Prediction {
    user_id: number;
    prediction: number;
    confidence: number;
    model_version: string;
    created_at?: string;
}

export interface AnalyticsData {
    total_users: number;
    active_users: number;
    churned_users: number;
    churn_rate: number;
    avg_churn_probability: number;
    model_version: string;
    model_accuracy: number | null;
    total_predictions: number;
}

export interface PredictionTimeline {
    date: string;
    avg_churn_probability: number;
    prediction_count: number;
}

export interface Event {
    event_id: number;
    user_id: number;
    event_type: string;
    event_data: Record<string, any> | null;
    session_duration: number | null;
    timestamp: string;
}
