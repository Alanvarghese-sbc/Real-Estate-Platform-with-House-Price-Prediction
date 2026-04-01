# Quick Start Guide - ML House Price Prediction

## ✅ System Status
- **Model Trained**: Yes
- **Accuracy**: 93.97%
- **Dataset**: 1000 records
- **Integration**: Complete

## 🚀 Quick Start (3 Steps)

### Step 1: Verify Model is Trained
```bash
cd ml_engine
python predict.py
```

**Expected Output:**
```
Testing price prediction...
[OK] Model loaded successfully

Predicted Price: Rs.9,543,990.99

Model Info:
Training Score: 0.9788
Testing Score: 0.9397
```

### Step 2: Run Django Server
```bash
cd ..
python manage.py runserver
```

### Step 3: Test the System
1. **Login as User**
2. **Add a Property** with:
   - District: Ernakulam
   - Area: 2000 sq ft
   - Bedrooms: 3
   - Location: Kochi
3. **Check Console** - You should see:
   ```
   [OK] Model loaded successfully
   ML Predicted Price: Rs.9,543,990.99
   ```
4. **Login as Broker**
5. **View Property Bids** - You'll see the AI predicted price with a blue "AI" badge

## 📊 How It Works

```
User Adds Property
    ↓
Django calls predict_house_price()
    ↓
ML Model predicts price based on:
  - District (5% importance)
  - Location (9% importance)
  - Area (84% importance) ← Most Important!
  - Bedrooms (2% importance)
    ↓
Price saved to database (price_predicted field)
    ↓
Broker sees AI price on propertyBids page
```

## 🔄 Retrain Model with New Data

### Option 1: Use Your Own Kaggle Dataset
1. Download CSV from Kaggle
2. Place in `ml_engine/house_prices.csv`
3. Run: `python train_model.py`

### Option 2: Generate More Sample Data
1. Edit `generate_data.py` - change `num_samples=1000` to `num_samples=5000`
2. Run: `python generate_data.py`
3. Run: `python train_model.py`

## 🎯 Expected Predictions

Based on current model:

| District | Area | Bedrooms | Predicted Price |
|----------|------|----------|----------------|
| Ernakulam | 2000 | 3 | ~Rs. 9.5M |
| Trivandrum | 2000 | 3 | ~Rs. 8.5M |
| Kottayam | 1500 | 2 | ~Rs. 5M |
| Thrissur | 2500 | 4 | ~Rs. 10M |

*Note: Prices vary based on location and random factors in training data*

## 🐛 Troubleshooting

### Issue: "Model not found"
**Solution:**
```bash
cd ml_engine
python train_model.py
```

### Issue: Prediction shows "N/A" on broker page
**Possible causes:**
1. Property was added before model was trained
2. Model training failed
3. Django server wasn't restarted after training

**Solution:**
1. Train model: `python ml_engine/train_model.py`
2. Restart Django server
3. Add a new property

### Issue: Price seems unrealistic
**Solution:**
- Use a real Kaggle dataset instead of generated data
- The generated data is for demonstration only

## 📈 Improve Accuracy

1. **Use Real Data**: Download from Kaggle
   - [India House Price Dataset](https://www.kaggle.com/datasets/mohamedafsal007/house-price-prediction)
   
2. **Add More Features**: Edit `train_model.py` to include:
   - Property age
   - Number of bathrooms
   - Parking spaces
   - Amenities

3. **Tune Hyperparameters**: In `train_model.py`:
   ```python
   model = RandomForestRegressor(
       n_estimators=200,  # Increase trees
       max_depth=30,      # Deeper trees
       # ... other params
   )
   ```

## 📁 File Structure

```
ml_engine/
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
├── generate_data.py       ← Generate sample data
├── train_model.py         ← Train the model
├── predict.py             ← Make predictions
├── house_prices.csv       ← Training dataset
└── models/                ← Trained model files
    ├── house_price_model.pkl
    ├── encoders.pkl
    └── metrics.pkl
```

## 🎓 Next Steps

1. ✅ **Tested** - Model is working
2. ⏭️ **Deploy** - Run Django and test end-to-end
3. 📊 **Monitor** - Check prediction accuracy
4. 🔄 **Retrain** - Update with real data from Kaggle
5. 🚀 **Enhance** - Add more features

## 💡 Tips

- **Area is most important** (84% importance) - Ensure accurate area input
- **Location matters** (9% importance) - Use consistent location names
- **Retrain periodically** - As you collect more real property data
- **Check console logs** - For prediction debugging

---

**Ready to use!** 🎉

For detailed documentation, see `README.md`
