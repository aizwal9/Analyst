import os
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (Create a .env file with DATABASE_URL)
load_dotenv()


def get_database():
    """
    Establishes a connection to the PostgreSQL database using the Olist schema.
    """

    # Ensure you have DATABASE_URL in your .env file
    # Format: postgresql://user:password@host:port/database_name
    db_uri = os.getenv("DATABASE_URL")

    if not db_uri:
        raise ValueError("DATABASE_URL not found in environment variables.")

    # We use SQLAlchemy engine configuration
    engine = create_engine(db_uri)

    # Initialize LangChain's SQLDatabase wrapper
    # include_tables: Restrict the LLM to only the 5 specific Olist tables to reduce noise
    db = SQLDatabase(
        engine=engine,
        include_tables=[
            "customers",
            "products",
            "orders",
            "order_items",
            "order_payments"
        ],
        sample_rows_in_table_info=3  # Helps the LLM understand data format
    )

    return db


def get_schema_info():
    """
    Returns the schema information to be injected into the LLM system prompt.
    """
    db = get_database()
    return db.get_table_info()


if __name__ == "__main__":
    # Test connection
    try:
        database = get_database()
        print("✅ Successfully connected to the database.")
        print(f"📂 Dialect: {database.dialect}")
        print(f"📝 Usable Tables: {database.get_usable_table_names()}")

        # Test a simple query to verify data access
        print("\n🔍 Testing Query (Count customers):")
        result = database.run("SELECT count(*) FROM customers;")
        print(f"Result: {result}")

    except Exception as e:
        print(f"❌ Error connecting to database: {e}")