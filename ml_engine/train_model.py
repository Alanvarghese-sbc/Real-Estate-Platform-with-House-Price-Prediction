"""
ML Model Training Script for House Price Prediction
Uses real Kaggle dataset to train a Random Forest model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_house_price_model(dataset_path):
    """
    Train a Random Forest model on house price data
    
    Args:
        dataset_path: Path to the CSV dataset
    
    Returns:
        model: Trained model
        encoders: Dictionary of label encoders for categorical features
        metrics: Training metrics
    """
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    print(f"Dataset loaded: {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    
    # Identify feature columns (adjust based on your Kaggle dataset)
    # Common columns in house price datasets:
    # - Area/Square Feet
    # - Bedrooms
    # - Location/District
    # - Price (target)
    
    # Create encoders dictionary
    encoders = {}
    
    # Encode categorical features
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        if col.lower() not in ['price', 'id']:  # Skip target and ID columns
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            print(f"Encoded column: {col}")
    
    # Identify target column (price)
    price_cols = [col for col in df.columns if 'price' in col.lower()]
    if not price_cols:
        raise ValueError("No price column found in dataset")
    
    target_col = price_cols[0]
    print(f"Target column: {target_col}")
    
    # Prepare features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Remove any non-numeric columns that weren't encoded
    X = X.select_dtypes(include=[np.number])
    
    print(f"Features: {X.columns.tolist()}")
    print(f"Training samples: {len(X)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest model
    print("\nTraining Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nModel Training Complete!")
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Testing R² Score: {test_score:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Important Features:")
    print(feature_importance.head())
    
    metrics = {
        'train_score': train_score,
        'test_score': test_score,
        'feature_importance': feature_importance.to_dict(),
        'feature_columns': X.columns.tolist()
    }
    
    return model, encoders, metrics


def save_model(model, encoders, metrics, save_dir='models'):
    """Save trained model and encoders"""
    os.makedirs(save_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(save_dir, 'house_price_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to: {model_path}")
    
    # Save encoders
    encoders_path = os.path.join(save_dir, 'encoders.pkl')
    with open(encoders_path, 'wb') as f:
        pickle.dump(encoders, f)
    print(f"Encoders saved to: {encoders_path}")
    
    # Save metrics
    metrics_path = os.path.join(save_dir, 'metrics.pkl')
    with open(metrics_path, 'wb') as f:
        pickle.dump(metrics, f)
    print(f"Metrics saved to: {metrics_path}")


if __name__ == "__main__":
    # Path to your Kaggle dataset
    dataset_path = "house_prices.csv"
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please download a house price dataset from Kaggle and place it in ml_engine/")
        print("Example datasets:")
        print("- House Prices: Advanced Regression Techniques")
        print("- USA Housing Dataset")
        print("- India House Price Prediction")
        exit(1)
    
    # Train model
    model, encoders, metrics = train_house_price_model(dataset_path)
    
    # Save model
    save_model(model, encoders, metrics)
    
    print("\n[SUCCESS] Model training and saving complete!")
