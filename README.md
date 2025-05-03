# Intelligent Financial Fraud Detection System

This project demonstrates an intelligent financial fraud detection system using Python, PyCaret, SQL, and Tableau.

## Components

- **SQL:** Used to store transaction data.
- **Python + PyCaret:** Used for loading data, preprocessing, training, real-time prediction, and exporting fraud detection results.
- **Tableau:** Used for visualizing fraud predictions and trends interactively.

## Setup and Running

1. Install required Python packages:

2. The provided Python script `fraud_detection.py` uses a SQLite database for demo purposes. It creates a sample dataset if one doesn't exist.

3. Run the fraud detection script to train the model and see a real-time prediction example:

4. The script saves the trained model to `fraud_detection_model.pkl`.

## Real-Time Fraud Detection

- Use the `real_time_predict(model, new_transaction)` function inside `fraud_detection.py` to predict fraud on new transactions instantly.
- A sample new transaction example is included in the main script.

## Using Tableau for Visualization

1. Export prediction results to CSV from the Python script to use in Tableau or connect Tableau directly to your SQL database.

2. Create visualizations such as:
   - Fraud distribution by merchant category.
   - Fraud detection accuracy using actual vs predicted fraud fields.
   - Trends over time using transaction hour and day of week.
   - Highlight high-risk transactions by sorting by prediction score.

3. Build interactive dashboards for fraud monitoring and pattern analysis.

## Extending

- Replace SQLite with your production SQL database by updating `DATABASE_URI` in `fraud_detection.py`.
- Build a REST API or web application for real-time predictions.
- Automate data refresh, model retraining, and alerting.

## File Descriptions

- `schema_and_sample_data.sql`: SQL schema and sample data for the transactions table.
- `fraud_detection.py`: Main Python script for training, prediction, real-time detection, and data export.
- `README.md`: This documentation file.

---
