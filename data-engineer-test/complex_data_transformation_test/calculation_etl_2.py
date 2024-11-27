import pandas as pd
from sqlalchemy import create_engine


DB_CONFIG = {
    'username': 'myuser',
    'password': 'mypassword',
    'host': '0.0.0.0',
    'port': 5432,
    'database': 'mydatabase'
}

def get_engine():
    url = f'postgresql://{DB_CONFIG.get('username')}:{DB_CONFIG.get('password')}@{DB_CONFIG.get('host')}:{DB_CONFIG.get('port')}/{DB_CONFIG.get('database')}'
    return create_engine(url)

def calculate_transaction_amount_by_column(df: pd.DataFrame, group_by_col: str) -> pd.DataFrame:

    calculated_df = df.groupby(group_by_col)['amount'].agg(
        total_amount='sum',
        min_amount='min',
        max_amount='max',
        avg_amount='mean',
        ).reset_index()
    
    return calculated_df

def calculate_top_n_sale_by_location(df: pd.DataFrame, n: int, location: str) -> pd.DataFrame:

    select_col = ['product_id','sales']

    filtered_df = df[df['location'] == location]
    filtered_df['sales'] = filtered_df['quantity'] * filtered_df['amount']

    result_df = filtered_df.sort_values('sales', axis=0, ascending=False).reset_index()

    return result_df[select_col].head(n)

engine = get_engine()

transaction_df = pd.read_sql_query('select * from transaction',con=engine)
user_info_df = pd.read_sql_query('select * from user_info',con=engine)

merged_df = transaction_df.merge(user_info_df, how='inner', on='user_id')

transaction_amount_by_gender = calculate_transaction_amount_by_column(merged_df, 'gender')
print(f"\nTransaction Amount by Gender \n{transaction_amount_by_gender.head()}")

transaction_amount_by_location = calculate_transaction_amount_by_column(merged_df, 'location')
print(f"\nTransaction Amount by Location \n{transaction_amount_by_location.head()}")

top_sale_df = calculate_top_n_sale_by_location(merged_df, 20, 'Chiangmai')
print(f"\nTop 20 sales product in Chiangmai \n{top_sale_df}")
