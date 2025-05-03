-- Schema for financial transactions table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT,
    transaction_date DATETIME,
    transaction_amount DECIMAL(10,2),
    merchant_category VARCHAR(100),
    transaction_type VARCHAR(50),
    card_present BOOLEAN,
    fraud_label BOOLEAN  -- TRUE if fraud, FALSE otherwise
);

-- Sample insert statements (Add more data as needed)
INSERT INTO transactions VALUES
(1, 101, '2024-01-01 10:00:00', 100.00, 'electronics', 'purchase', TRUE, FALSE),
(2, 102, '2024-01-01 11:00:00', 10000.00, 'jewelry', 'purchase', FALSE, TRUE),
(3, 103, '2024-01-02 12:30:00', 45.50, 'grocery', 'purchase', TRUE, FALSE),
(4, 101, '2024-01-02 14:00:00', 200.00, 'electronics', 'purchase', TRUE, FALSE),
(5, 104, '2024-01-03 16:45:00', 5000.00, 'travel', 'purchase', FALSE, TRUE);
