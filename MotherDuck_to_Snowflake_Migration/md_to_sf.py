import os
from dotenv import load_dotenv
import duckdb
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

# connect to motherduck
md_token = os.getenv("MOTHERDUCK_TOKEN")
print("Connecting to MotherDuck...")
md_conn = duckdb.connect(f"md:?token={md_token}")
print("Connected to MotherDuck successfully.")


# connect to snowflake with mfa auth // created .env file to host the account login and authentication info
print("Connecting to Snowflake using MFA passcode...")
ctx = snowflake.connector.connect(
    user = os.getenv("sf_user"),
    account = os.getenv("sf_account"),
    password = os.getenv("sf_password"),
    passcode = os.getenv("sf_passcode"), # google authenticator code
    authenticator = 'username_password_mfa', # forces snowflake to accept the code
    warehouse = 'compute_wh'
)
cursor = ctx.cursor()
print("Connected to Snowflake successfully.")


# migration logic
print("Ensuring target database and schema exist in Snowflake...")
cursor.execute("CREATE DATABASE IF NOT EXISTS raw;")
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw.motherduck_migration;")
cursor.execute("USE DATABASE raw;")
cursor.execute("USE SCHEMA motherduck_migration;")
print("Database and schema are ready.")

try:
    tables_query = "SELECT table_name FROM information_schema.tables WHERE table_catalog = 'data_jobs' AND table_schema = 'main';"
    tables = [row[0] for row in md_conn.sql(tables_query).fetchall()]
    
    print(f"\nFound {len(tables)} tables to migrate from the 'data_jobs' share: {tables}\n")
    
    for table in tables:
        print(f"Processing Table: {table}")
        print(f"Extracting data from data_jobs.main.{table}...")
        df = md_conn.sql(f"SELECT * FROM data_jobs.main.{table}").df()
        sf_table_name = table.upper()
        
        print(f"Loading '{sf_table_name}' into Snowflake...")
        success, nchunks, nrows, _ = write_pandas(
            conn = ctx,
            df = df,
            table_name = sf_table_name,
            auto_create_table = True
        )
        print(f"Successfully migrated {nrows} rows for {sf_table_name}.")
        
    print("\nMigration completed successfully.")
finally:
    cursor.close()
    ctx.close()
    md_conn.close()
    print("Connections closed.")