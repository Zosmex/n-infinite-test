CREATE TABLE user_transaction_amount (
  user_id VARCHAR(255) PRIMARY KEY,
  total_sales DOUBLE PRECISION,
  avg_sales DOUBLE PRECISION
);

CREATE TABLE daily_transaction_amount (
  order_date DATE PRIMARY KEY,
  total_sales DOUBLE PRECISION,
  min_sales DOUBLE PRECISION,
  max_sales DOUBLE PRECISION,
  avg_sales DOUBLE PRECISION,
  total_vat DOUBLE PRECISION,
  min_vat DOUBLE PRECISION,
  max_vat DOUBLE PRECISION,
  avg_vat DOUBLE PRECISION
);

CREATE TABLE product_sales (
	product_id VARCHAR(255) PRIMARY KEY,
	number_of_transactions INT,
	total_sales INT
);