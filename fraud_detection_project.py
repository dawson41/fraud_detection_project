"""
Intelligent Financial Fraud Detection System with Real-Time Detection

This script connects to a SQL database containing financial transactions,
extracts the data, preprocesses it, trains a fraud detection model using PyCaret,
and supports real-time fraud detection for new transactions.

Dependencies:
- pycaret
- pandas
- sqlalchemy
- scikit-learn
- matplotlib (for PyCaret)
- pyodbc or appropriate DB API driver for your SQL DB

Usage:
- Configure your database connection string in DATABASE_URI.
- Run the script to train and save the model.
- Use real_time_predict function for new transaction fraud prediction.
"""

import pandas as pd
from pycaret.classification import setup, compare_models, finalize_model, predict_model, save_model, load_model
from sqlalchemy import create_engine
import os

# Configure your database connection here
DATABASE_URI = 'sqlite:///transactions.db'
MODEL_PATH = 'fraud_detection_model.pkl'

def create_sample_database(engine):
    """Create sample transactions table and insert sample data."""
    with engine.connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            transaction_date TEXT,
            transaction_amount REAL,
            merchant_category TEXT,
            transaction_type TEXT,
            card_present INTEGER,
            fraud_label INTEGER
        )
        """)
        # Insert sample data if empty
        result = conn.execute("SELECT COUNT(*) FROM transactions")
        count = result.fetchone()[0]
        if count == 0:
            conn.execute("""
            INSERT INTO transactions (transaction_id, user_id, transaction_date, transaction_amount,
            merchant_category, transaction_type, card_present, fraud_label) VALUES
            (1, 101, '2024-01-01 10:00:00', 100.00, 'electronics', 'purchase', 1, 0),
            (2, 102, '2024-01-01 11:00:00', 10000.00, 'jewelry', 'purchase', 0, 1),
            (3, 103, '2024-01-02 12:30:00', 45.50, 'grocery', 'purchase', 1, 0),
            (4, 101, '2024-01-02 14:00:00', 200.00, 'electronics', 'purchase', 1, 0),
            (5, 104, '2024-01-03 16:45:00', 5000.00, 'travel', 'purchase', 0, 1),
            (6, 105, '2024-01-03 17:00:00', 75.00, 'grocery', 'purchase', 1, 0),
            (7, 106, '2024-01-04 10:00:00', 120.00, 'electronics', 'purchase', 1, 0),
            (8, 107, '2024-01-05 09:00:00', 9999.99, 'jewelry', 'purchase', 0, 1)
            """)
        conn.commit()

def load_data(engine):
    """Load transaction data from the database."""
    df = pd.read_sql("SELECT * FROM transactions", con=engine)
    return df

def preprocess_data(df):
    """Basic preprocessing for the dataset."""
    # Convert card_present and fraud_label to boolean
    df['card_present'] = df['card_present'].astype(bool)
    df['fraud_label'] = df['fraud_label'].astype(bool)
    # Convert transaction_date to datetime and extract features
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['transaction_hour'] = df['transaction_date'].dt.hour
    df['transaction_dayofweek'] = df['transaction_date'].dt.dayofweek
    df = df.drop(columns=['transaction_id', 'transaction_date'])
    return df

def train_and_save_model(df):
    """Train fraud detection model using PyCaret, save model to disk."""
    clf = setup(data=df, target='fraud_label', session_id=123, silent=True,
                categorical_features=['merchant_category', 'transaction_type', 'card_present'],
                numeric_features=['transaction_amount', 'transaction_hour', 'transaction_dayofweek'],
                preprocess=True)

    best_model = compare_models()
    final_model = finalize_model(best_model)

    save_model(final_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return final_model

def load_trained_model():
    """Load the trained model from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model file not found. Please train the model first.")
    model = load_model(MODEL_PATH)
    return model

def preprocess_real_time_data(new_data):
    """
    Preprocess a new transaction record (dict or DataFrame with one row) for prediction.
    new_data should contain keys:
    - user_id
    - transaction_date (string datetime)
    - transaction_amount (float)
    - merchant_category (string)
    - transaction_type (string)
    - card_present (bool or int 0/1)
    """
    df = pd.DataFrame([new_data]) if isinstance(new_data, dict) else new_data.copy()
    # Ensure card_present is boolean
    df['card_present'] = df['card_present'].astype(bool)
    # Convert transaction_date to datetime and extract features
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['transaction_hour'] = df['transaction_date'].dt.hour
    df['transaction_dayofweek'] = df['transaction_date'].dt.dayofweek
    # Drop transaction_id and transaction_date if present
    to_drop = []
    if 'transaction_id' in df.columns:
        to_drop.append('transaction_id')
    to_drop.append('transaction_date')
    df = df.drop(columns=to_drop)
    return df

def real_time_predict(model, new_transaction):
    """
    Predict fraud for a new transaction.
    new_transaction: dict or DataFrame with one row (transaction info, see preprocess_real_time_data)
    Returns prediction label and score.
    """
    df = preprocess_real_time_data(new_transaction)
    prediction = predict_model(model, data=df)
    pred_label = prediction.loc[0, 'Label']  # 1 for fraud, 0 for non-fraud
    pred_score = prediction.loc[0, 'Score'] # confidence score
    return pred_label, pred_score

def main():
    engine = create_engine(DATABASE_URI)

    # Create sample data if not exists (for demo)
    create_sample_database(engine)

    # Load and preprocess data
    df = load_data(engine)
    df_processed = preprocess_data(df)

    # Train and save model
    model = train_and_save_model(df_processed)

    # Demonstrate real-time detection with a new sample transaction
    sample_new_txn = {
        'user_id': 108,
        'transaction_date': '2024-06-01 13:15:00',
        'transaction_amount': 15000.00,
        'merchant_category': 'jewelry',
        'transaction_type': 'purchase',
        'card_present': False
    }
    print("\nReal-time Transaction for Fraud Prediction:")
    print(sample_new_txn)
    pred_label, pred_score = real_time_predict(model, sample_new_txn)
    print(f"Predicted Fraud Label: {pred_label} (1=Fraud, 0=Not Fraud), Score: {pred_score:.4f}")

if __name__ == "__main__":
    main()
