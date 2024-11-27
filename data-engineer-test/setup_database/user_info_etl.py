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

# Read .csv
try:
    df = pd.read_csv('data-engineer-test/ref/user_info.csv')
except Exception as e:
    print('Unable to access csv file', repr(e))

print(df.head())

# Save data to Postgres

# Connect to database
engine = get_engine()
print(engine)

df.to_sql('user_info', engine, index=False, if_exists='append')

print("Data loaded successfully.")
