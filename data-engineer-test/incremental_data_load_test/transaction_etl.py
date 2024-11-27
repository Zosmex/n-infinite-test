import os
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

def load_to_postgres(input_dir):
    engine = get_engine()

    metadata = MetaData()

    # Reflect the table
    table_name = 'transaction'  # Replace with the table name you want to load
    table = Table(table_name, metadata, autoload_with=engine)

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            print(f'Storing file: {file_path}')
            
            try:
                df = pd.read_csv(file_path)
                records = df.to_dict(orient='records')

                for record in records:
                    insert_stmt = insert(table).values(
                        **record
                    )
                    insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["order_id"])

                    insert_stmt.compile(dialect=postgresql.dialect())

                    with engine.connect() as conn:
                        res = conn.execute(insert_stmt)
                        conn.commit()

                print(f"Inserted data from: {file_path}")

            except Exception as e:
                raise(e)
            
load_to_postgres("data-engineer-test/ref/sales")
