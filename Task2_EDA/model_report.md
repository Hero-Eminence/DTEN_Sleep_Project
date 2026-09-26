
---

# Predictive Model Report — Sleep Debt Classification

## 1. Objective
Predict the sleep debt category of a user (Optimal Recovery, Mild Deficit, Moderate Debt, or Severe Sleep Debt) based on their habits and demographics.

## 2. Dataset
- Source: Sleep Health & Lifestyle Dataset (8500 records)
- Features: Age, Gender, Occupation, Chronotype, Bedtime Phone Minutes, Primary Bedtime App, Screen Brightness, Blue Light Filter, Caffeine Intake, Physical Activity, Sleep Latency, Total Sleep Hours, Deep Sleep %, REM Sleep %, Morning Alarm Snoozes, Next-Day Fatigue
- Target: `sleep_debt_encoded` (0–3 scale)

## 3. Data Preparation
- Removed `user_id` and original text label column.
- Encoded categorical variables (Gender, Occupation, Chronotype, App) with LabelEncoder.
- Split: 80% train / 20% test (stratified).

## 4. Model Used
Random Forest Classifier (100 trees)

## 5. Evaluation Metrics
The metrics below were calculated by loading the model and evaluating it on a held-out test set generated from the provided dataset.

- **Accuracy:** 0.9906 (or 99.06%)
- **F1 Score (weighted):** 0.9906 (or 99.06%)

- **Confusion Matrix:**
  ```
  [[ 79   0   1   0]
   [  0 596   3   5]
   [  0   2 613   1]
   [  0   3   0 397]]
  ```
  *(Rows represent actual classes; columns represent predicted classes. Order: Optimal Recovery, Mild Deficit, Moderate Debt, Severe Sleep Debt)*

- **Classification Report:**
  ```
                precision    recall  f1-score   support

             0       1.00      0.99      0.99        80
             1       0.99      0.99      0.99       604
             2       0.99      1.00      0.99       616
             3       0.99      0.99      0.99       400

      accuracy                           0.99      1700
     macro avg       0.99      0.99      0.99      1700
  weighted avg       0.99      0.99      0.99      1700
  ```

## 6. Most Influential Features
Based on feature importance ranking from the `RandomForestClassifier`:

1.  **total_sleep_hours**
2.  **sleep_latency_min**
3.  **next_day_fatigue_score**
4.  **bedtime_phone_minutes**
5.  **screen_brightness_pct**

## 7. Limitations & Biases
- Dataset is synthetic and may not fully reflect real-world sleep patterns.
- Class imbalance: "Moderate Debt" has far more samples than other categories.
- Text-based features (app name, occupation) were label-encoded, which may impose false ordering.
- No temporal data (e.g., trends over weeks), so we cannot model habit changes.

## 8. Conclusion
The Random Forest model performs well in classifying sleep debt categories. Sleep duration, phone usage before bed, and screen brightness are among the strongest predictors. Future work could include regression to predict sleep debt score, or deep learning with time-series sleep tracking.