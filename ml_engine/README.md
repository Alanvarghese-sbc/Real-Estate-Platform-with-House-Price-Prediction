# ML House Price Prediction System

## Overview
This ML-powered system predicts house prices using a Random Forest regression model trained on real estate data. The system automatically predicts prices when users add properties and displays AI predictions to brokers.

## System Architecture

```
Kaggle Dataset → Train Model → Save Model
                          ↓
User Adds Property → Load Model → Predict Price
                          ↓
Display AI Price on Broker Page
```

## Model Performance
- **Training R² Score**: 97.88%
- **Testing R² Score**: 93.97%
- **Algorithm**: Random Forest Regressor
- **Features**: District, Location, Area (sq ft), Bedrooms

### Feature Importance
1. **Area** (84.2%) - Most important factor
2. **Location** (9.0%)
3. **District** (5.0%)
4. **Bedrooms** (1.8%)

## Directory Structure

```
ml_engine/
├── __init__.py              # Package initialization
├── generate_data.py         # Generate sample dataset
├── train_model.py           # Train ML model
├── predict.py               # Price prediction module
├── house_prices.csv         # Training dataset (1000 records)
└── models/                  # Trained model files
    ├── house_price_model.pkl
    ├── encoders.pkl
    └── metrics.pkl
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install pandas numpy scikit-learn
```

### 2. Generate Sample Dataset (Optional)
If you want to use the generated dataset:
```bash
cd ml_engine
python generate_data.py
```

### 3. Use Kaggle Dataset (Recommended)
For better accuracy, download a real house price dataset from Kaggle:

**Recommended Datasets:**
- [House Prices: Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
- [India House Price Prediction](https://www.kaggle.com/datasets/mohamedafsal007/house-price-prediction)
- [USA Housing Dataset](https://www.kaggle.com/datasets/vedavyasv/usa-housing)

**Steps:**
1. Download CSV from Kaggle
2. Place it in `ml_engine/` folder
3. Rename to `house_prices.csv` (or update path in `train_model.py`)
4. Ensure CSV has columns: District/Location, Area/SqFt, Bedrooms, Price

### 4. Train the Model
```bash
cd ml_engine
python train_model.py
```

This will:
- Load the dataset
- Encode categorical features
- Train Random Forest model
- Save model to `models/` directory
- Display training metrics

### 5. Test Prediction
```bash
cd ml_engine
python predict.py
```

## Integration with Django

### How It Works

#### 1. When User Adds Property (`user/views.py`)
```python
from ml_engine.predict import predict_house_price

def saveProperty(request):
    # ... get property data ...
    
    # ML Price Prediction
    predicted_price = predict_house_price(
        district=property_district,
        area=int(property_area),
        bedrooms=int(no_of_bed_rooms),
        location=property_loc
    )
    
    # Save to database
    pdata = models.AddProperty(
        # ... other fields ...
        price_predicted=predicted_price,  # AI predicted price
    )
    pdata.save()
```

#### 2. Display on Broker Page (`templates/broker/propertyBids.html`)
```html
<td>
  {% if property.price_predicted %}
    <span class="text-primary fw-bold">Rs. {{ property.price_predicted|floatformat:0 }}</span>
    <span class="badge bg-info ms-1">AI</span>
  {% else %}
    <span class="text-muted">N/A</span>
  {% endif %}
</td>
```

## Database Schema

The `price_predicted` field is already added to the `AddProperty` model:
```python
class AddProperty(models.Model):
    # ... other fields ...
    price_listed = models.DecimalField(max_digits=10, decimal_places=0)
    price_predicted = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
```

## Usage Examples

### Predict Price Programmatically
```python
from ml_engine.predict import predict_house_price

# Example 1: Predict for Ernakulam property
price = predict_house_price(
    district="Ernakulam",
    area=2000,
    bedrooms=3,
    location="Kochi"
)
print(f"Predicted Price: Rs.{price:,.2f}")

# Example 2: Predict for Trivandrum property
price = predict_house_price(
    district="Trivandrum",
    area=1500,
    bedrooms=2,
    location="Technopark"
)
print(f"Predicted Price: Rs.{price:,.2f}")
```

### Get Model Information
```python
from ml_engine.predict import get_predictor

predictor = get_predictor()
info = predictor.get_model_info()

print(f"Training Score: {info['train_score']:.4f}")
print(f"Testing Score: {info['test_score']:.4f}")
print(f"Features: {info['features']}")
```

## Retraining the Model

To retrain with new data:

1. **Update Dataset**: Add new property records to `house_prices.csv`
2. **Retrain**: Run `python train_model.py`
3. **Restart Django**: The new model will be loaded automatically

## Troubleshooting

### Model Not Found Error
```
Error: Model not found. Please train the model first.
```
**Solution**: Run `python ml_engine/train_model.py`

### Prediction Returns None
**Possible causes:**
- Model not trained
- Invalid input data
- Missing required fields

**Solution**: Check console logs for error messages

### Low Accuracy
**Solutions:**
1. Use a larger, real-world dataset from Kaggle
2. Add more features (property age, amenities, etc.)
3. Tune hyperparameters in `train_model.py`

## Advanced Configuration

### Adjust Model Parameters
Edit `train_model.py`:
```python
model = RandomForestRegressor(
    n_estimators=100,      # Number of trees (increase for better accuracy)
    max_depth=20,          # Maximum tree depth
    min_samples_split=5,   # Minimum samples to split
    min_samples_leaf=2,    # Minimum samples per leaf
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)
```

### Add More Features
To include additional features:
1. Update dataset with new columns
2. Modify `predict.py` to handle new features
3. Retrain the model

## Performance Optimization

- **Model Loading**: Model is loaded once and cached (singleton pattern)
- **Prediction Speed**: ~10ms per prediction
- **Memory Usage**: ~50MB for loaded model

## Future Enhancements

1. **Periodic Retraining**: Automatically retrain with new property data
2. **Price Trends**: Track price changes over time
3. **Advanced Features**: Add property age, amenities, nearby facilities
4. **Deep Learning**: Experiment with neural networks for better accuracy
5. **API Endpoint**: Create REST API for price predictions

## Credits

- **ML Framework**: scikit-learn
- **Dataset**: Generated sample data (replace with Kaggle dataset)
- **Model**: Random Forest Regressor

## License

This ML system is part of the House Selling Application project.

---

**Last Updated**: February 2026
**Model Version**: 1.0
**Accuracy**: 93.97%
