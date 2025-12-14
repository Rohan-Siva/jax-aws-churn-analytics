import jax
import jax.numpy as jnp
import optax
from flax.training import train_state
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from typing import Dict, Tuple
import pickle
from datetime import datetime
from pathlib import Path
import sys
import os

                              
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.jax_classifier import ChurnPredictor
from data.extract_from_db import extract_data_from_db
from data.feature_engineering import extract_user_features, normalize_features, create_train_test_split


class TrainState(train_state.TrainState):
                                                              
    batch_stats: any = None


def create_train_state(rng, model, learning_rate, input_shape):
                                       
    params = model.init(rng, jnp.ones(input_shape))
    tx = optax.adam(learning_rate)
    return train_state.TrainState.create(
        apply_fn=model.apply,
        params=params,
        tx=tx
    )


@jax.jit
def train_step(state, batch_x, batch_y):
                              
    def loss_fn(params):
        logits = state.apply_fn(params, batch_x)
        loss = optax.sigmoid_binary_cross_entropy(logits, batch_y.reshape(-1, 1)).mean()
        return loss
    
    loss, grads = jax.value_and_grad(loss_fn)(state.params)
    state = state.apply_gradients(grads=grads)
    return state, loss


@jax.jit
def eval_step(state, batch_x, batch_y):
                                
    logits = state.apply_fn(state.params, batch_x)
    loss = optax.sigmoid_binary_cross_entropy(logits, batch_y.reshape(-1, 1)).mean()
    return loss, logits


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    epochs: int = 100,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    random_seed: int = 42
) -> Tuple[train_state.TrainState, Dict]:
\
\
\
\
\
       
                      
    rng = jax.random.PRNGKey(random_seed)
    model = ChurnPredictor()
    
                        
    state = create_train_state(
        rng,
        model,
        learning_rate,
        input_shape=(1, X_train.shape[1])
    )
    
                           
    X_train_jax = jnp.array(X_train, dtype=jnp.float32)
    y_train_jax = jnp.array(y_train, dtype=jnp.float32)
    X_test_jax = jnp.array(X_test, dtype=jnp.float32)
    y_test_jax = jnp.array(y_test, dtype=jnp.float32)
    
                   
    history = {'train_loss': [], 'test_loss': []}
    n_batches = len(X_train) // batch_size
    
    print(f"Training for {epochs} epochs with batch size {batch_size}")
    print(f"Number of batches per epoch: {n_batches}")
    
    for epoch in range(epochs):
                               
        perm = np.random.permutation(len(X_train))
        X_train_shuffled = X_train_jax[perm]
        y_train_shuffled = y_train_jax[perm]
        
                  
        epoch_losses = []
        for i in range(n_batches):
            batch_x = X_train_shuffled[i * batch_size:(i + 1) * batch_size]
            batch_y = y_train_shuffled[i * batch_size:(i + 1) * batch_size]
            
            state, loss = train_step(state, batch_x, batch_y)
            epoch_losses.append(float(loss))
        
        train_loss = np.mean(epoch_losses)
        
                    
        test_loss, _ = eval_step(state, X_test_jax, y_test_jax)
        
        history['train_loss'].append(train_loss)
        history['test_loss'].append(float(test_loss))
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.4f}, Test Loss: {float(test_loss):.4f}")
    
    return state, history


def evaluate_model(state, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
\
\
       
    X_test_jax = jnp.array(X_test, dtype=jnp.float32)
    y_test_jax = jnp.array(y_test, dtype=jnp.float32)
    
                     
    _, logits = eval_step(state, X_test_jax, y_test_jax)
    predictions = np.array(logits).flatten()
    predictions_binary = (predictions > 0.5).astype(int)
    
                     
    metrics = {
        'accuracy': accuracy_score(y_test, predictions_binary),
        'precision': precision_score(y_test, predictions_binary, zero_division=0),
        'recall': recall_score(y_test, predictions_binary, zero_division=0),
        'f1': f1_score(y_test, predictions_binary, zero_division=0),
        'roc_auc': roc_auc_score(y_test, predictions) if len(np.unique(y_test)) > 1 else 0.0
    }
    
    return metrics


def save_model(state, version: str, metrics: Dict, output_dir: str = "../../models"):
\
\
       
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
                           
    model_data = {
        'params': state.params,
        'version': version,
        'metrics': metrics,
        'trained_at': datetime.now().isoformat()
    }
    
    model_file = output_path / f"model_{version}.pkl"
    with open(model_file, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved to {model_file}")
    return str(model_file)


def main():
                                
    print("=" * 60)
    print("JAX Churn Prediction Model Training")
    print("=" * 60)
    
                                
    print("\n1. Extracting data from database...")
    users_df, events_df = extract_data_from_db()
    
                         
    print("\n2. Engineering features...")
    features_df = extract_user_features(users_df, events_df)
    
    print(f"Feature distribution:")
    print(features_df['churned'].value_counts())
    
                                 
    feature_cols = [
        'days_since_last_active',
        'total_events',
        'avg_session_duration',
        'active_days',
        'subscription_tier_encoded',
        'event_type_diversity'
    ]
    
                        
    features_normalized, norm_params = normalize_features(features_df, feature_cols)
    
                
    print("\n3. Splitting data...")
    train_df, test_df = create_train_test_split(features_normalized, test_size=0.2)
    
    X_train = train_df[feature_cols].values
    y_train = train_df['churned'].values
    X_test = test_df[feature_cols].values
    y_test = test_df['churned'].values
    
    print(f"Train set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
                 
    print("\n4. Training model...")
    state, history = train_model(
        X_train, y_train,
        X_test, y_test,
        epochs=100,
        batch_size=32,
        learning_rate=0.001
    )
    
              
    print("\n5. Evaluating model...")
    metrics = evaluate_model(state, X_test, y_test)
    
    print("\nModel Performance:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name}: {value:.4f}")
    
                
    print("\n6. Saving model...")
    version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    save_model(state, version, metrics)
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
