CREATE TABLE transaction (
  order_id VARCHAR(255) PRIMARY KEY,
  user_id VARCHAR(255),
  product_id VARCHAR(255),
  quantity INT,
  amount INT,
  order_date DATE
);