"""
ML Price Prediction Module
Loads trained model and predicts house prices
"""
import pickle
import os
import numpy as np

class HousePricePredictor:
    def __init__(self, model_dir='ml_engine/models'):
        """Initialize predictor by loading model and encoders"""
        self.model_dir = model_dir
        self.model = None
        self.encoders = None
        self.metrics = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            model_path = os.path.join(self.model_dir, 'house_price_model.pkl')
            encoders_path = os.path.join(self.model_dir, 'encoders.pkl')
            metrics_path = os.path.join(self.model_dir, 'metrics.pkl')
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(encoders_path, 'rb') as f:
                self.encoders = pickle.load(f)
            
            with open(metrics_path, 'rb') as f:
                self.metrics = pickle.load(f)
            
            print("[OK] Model loaded successfully")
            return True
        except FileNotFoundError:
            print("[WARNING] Model not found. Please train the model first.")
            return False
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            return False
    
    def predict_price(self, property_data):
        """
        Predict house price based on property features
        
        Args:
            property_data: Dictionary with keys:
                - district: str
                - location: str (optional)
                - area: int (square feet)
                - bedrooms: int
        
        Returns:
            predicted_price: float
        """
        if self.model is None:
            raise ValueError("Model not loaded. Cannot make predictions.")
        
        # Prepare features based on what the model expects
        features = {}
        
        # Get feature columns from metrics
        feature_cols = self.metrics.get('feature_columns', [])
        
        # Map property data to feature columns
        for col in feature_cols:
            col_lower = col.lower()
            
            if 'district' in col_lower:
                value = property_data.get('district', 'Unknown')
                if col in self.encoders:
                    try:
                        features[col] = self.encoders[col].transform([value])[0]
                    except ValueError:
                        # Unknown category, use most common
                        features[col] = 0
                else:
                    features[col] = value
            
            elif 'location' in col_lower:
                value = property_data.get('location', 'Unknown')
                if col in self.encoders:
                    try:
                        features[col] = self.encoders[col].transform([value])[0]
                    except ValueError:
                        features[col] = 0
                else:
                    features[col] = value
            
            elif 'area' in col_lower or 'sqft' in col_lower or 'square' in col_lower:
                features[col] = property_data.get('area', 1000)
            
            elif 'bedroom' in col_lower or 'bed' in col_lower:
                features[col] = property_data.get('bedrooms', 2)
            
            else:
                # Default value for unknown features
                features[col] = 0
        
        # Create feature array in correct order
        feature_array = np.array([[features[col] for col in feature_cols]])
        
        # Predict
        predicted_price = self.model.predict(feature_array)[0]
        
        return max(0, predicted_price)  # Ensure non-negative
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.metrics:
            return {
                'train_score': self.metrics.get('train_score', 0),
                'test_score': self.metrics.get('test_score', 0),
                'features': self.metrics.get('feature_columns', [])
            }
        return None


# Singleton instance
_predictor_instance = None

def get_predictor():
    """Get or create predictor instance"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = HousePricePredictor()
    return _predictor_instance


def predict_house_price(district, area, bedrooms, location=None):
    """
    Convenience function to predict house price
    
    Args:
        district: str - Property district
        area: int - Area in square feet
        bedrooms: int - Number of bedrooms
        location: str - Specific location (optional)
    
    Returns:
        float - Predicted price
    """
    predictor = get_predictor()
    
    property_data = {
        'district': district,
        'area': area,
        'bedrooms': bedrooms,
        'location': location or 'Unknown'
    }
    
    return predictor.predict_price(property_data)


if __name__ == "__main__":
    # Test prediction
    print("Testing price prediction...")
    
    test_property = {
        'district': 'Ernakulam',
        'location': 'Kochi',
        'area': 2000,
        'bedrooms': 3
    }
    
    try:
        predictor = HousePricePredictor(model_dir='models')
        price = predictor.predict_price(test_property)
        print(f"\nPredicted Price: Rs.{price:,.2f}")
        
        info = predictor.get_model_info()
        if info:
            print(f"\nModel Info:")
            print(f"Training Score: {info['train_score']:.4f}")
            print(f"Testing Score: {info['test_score']:.4f}")
    except Exception as e:
        print(f"Error: {e}")
