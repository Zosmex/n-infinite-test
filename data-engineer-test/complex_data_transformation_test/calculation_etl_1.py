import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert


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

def calculate_user_transaction_amount(df: pd.DataFrame) -> pd.DataFrame:
    
    df['sales'] = df['amount'] * df['quantity']
    calculated_df = df.groupby('user_id')['sales'].agg(total_sales='sum', avg_sales='mean').reset_index()

    return calculated_df

def calculate_daily_transaction_amount(df: pd.DataFrame) -> pd.DataFrame:

    df['order_date'] = pd.to_datetime(df['order_date'])

    # Calculate sales
    df['sales'] = df['amount'] * df['quantity']
    df['vat'] = df['amount'] * 0.7

    calculated_df = df.groupby('order_date').agg(
        total_sales=('sales', 'sum'),
        min_sales=('sales', 'min'),
        max_sales=('sales', 'max'),
        avg_sales=('sales', 'mean'),
        total_vat=('vat', 'sum'),
        min_vat=('vat', 'min'),
        max_vat=('vat', 'max'),
        avg_vat=('vat', 'mean')
    ).reset_index()

    return calculated_df

def calculate_product_sale(df: pd.DataFrame) -> pd.DataFrame:

    calculated_df = df.groupby('product_id').agg(
        number_of_transactions=('sales', 'count'),
        total_sales=('sales', 'sum')
    ).reset_index()

    return calculated_df

def load_to_postgres(input_df:pd.DataFrame, table_name: str, primary_key: str) -> None:
    engine = get_engine()
    metadata = MetaData()

    table = Table(table_name, metadata, autoload_with=engine)

    records = input_df.to_dict(orient='records')

    for record in records:
        insert_stmt = insert(table).values(**record)
        insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=[primary_key])

        insert_stmt.compile(dialect=postgresql.dialect())

        with engine.connect() as conn:
            res = conn.execute(insert_stmt)
            conn.commit()

    print(f"Inserted data to: {table}")


engine = get_engine()

df = pd.read_sql_query('select * from transaction',con=engine)

user_transaction_amount_df = calculate_user_transaction_amount(df)
daily_transaction_amount_df = calculate_daily_transaction_amount(df)
product_sale_df = calculate_product_sale(df)

load_to_postgres(user_transaction_amount_df, 'user_transaction_amount', 'user_id')
load_to_postgres(daily_transaction_amount_df, 'daily_transaction_amount', 'order_date')
load_to_postgres(product_sale_df, 'product_sales', 'product_id')
