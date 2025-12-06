


CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    churned BOOLEAN DEFAULT FALSE,
    churn_date TIMESTAMP
);


CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    session_duration FLOAT,
    timestamp TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS predictions (
    prediction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL,
    prediction_type VARCHAR(100) NOT NULL,
    predicted_value FLOAT NOT NULL,
    confidence FLOAT,
    features JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS model_metadata (
    model_id SERIAL PRIMARY KEY,
    version VARCHAR(50) UNIQUE NOT NULL,
    accuracy FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    deployed_at TIMESTAMP DEFAULT NOW(),
    storage_path VARCHAR(500),
    metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE
);


CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_users_last_active ON users(last_active);
CREATE INDEX IF NOT EXISTS idx_users_churned ON users(churned);


CREATE OR REPLACE VIEW user_analytics AS
SELECT 
    u.user_id,
    u.email,
    u.subscription_tier,
    u.churned,
    EXTRACT(DAY FROM (NOW() - u.last_active)) as days_since_last_active,
    COUNT(DISTINCT e.event_id) as total_events,
    COUNT(DISTINCT DATE(e.timestamp)) as active_days,
    AVG(e.session_duration) as avg_session_duration,
    MAX(e.timestamp) as last_event_time,
    (SELECT predicted_value 
     FROM predictions p 
     WHERE p.user_id = u.user_id 
     ORDER BY p.created_at DESC 
     LIMIT 1) as latest_churn_prediction
FROM users u
LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.user_id, u.email, u.subscription_tier, u.churned, u.last_active;


INSERT INTO model_metadata (version, accuracy, deployed_at, storage_path, is_active)
VALUES ('v0.0.0', 0.0, NOW(), 'models/initial', FALSE)
ON CONFLICT (version) DO NOTHING;
