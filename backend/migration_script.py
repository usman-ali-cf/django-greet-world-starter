import sqlite3
from sqlalchemy import create_engine, inspect, text, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, \
    ForeignKey
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from tqdm import tqdm
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional, Tuple

# Load environment variables
load_dotenv()

# Database configurations
SQLITE_DB = 'mysqlite3.db'
POSTGRES_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'your_database'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

# Type mapping from SQLite to PostgreSQL
TYPE_MAPPING = {
    'TEXT': 'TEXT',
    'VARCHAR': 'VARCHAR',
    'INTEGER': 'BIGINT',
    'REAL': 'DOUBLE PRECISION',
    'BLOB': 'BYTEA',
    'NUMERIC': 'NUMERIC',
    'BOOLEAN': 'BOOLEAN',
    'DATE': 'DATE',
    'DATETIME': 'TIMESTAMP',
    'TIMESTAMP': 'TIMESTAMP'
}


def get_sqlite_connection():
    """Get SQLite connection with row factory for better column access"""
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_sqlite_tables(conn):
    """Get list of all tables in SQLite database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall() if table[0] != 'sqlite_sequence']


def get_table_schema(conn, table_name):
    """Get the schema of a SQLite table"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    # Get primary keys
    cursor.execute(f"PRAGMA table_info({table_name})")
    primary_keys = [col[1] for col in cursor.fetchall() if col[5] == 1]

    # Get foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()

    return {
        'columns': columns,
        'primary_keys': primary_keys,
        'foreign_keys': foreign_keys
    }


async def create_postgres_table(pg_engine, table_name, schema):
    """Create a table in PostgreSQL if it doesn't exist"""
    # Check if table exists
    inspector = inspect(pg_engine)
    if table_name in inspector.get_table_names():
        print(f"Table {table_name} already exists, skipping creation")
        return True

    # Start building the CREATE TABLE statement
    create_table_sql = [f'CREATE TABLE IF NOT EXISTS "{table_name}" (']

    # Add columns
    column_defs = []
    for col in schema['columns']:
        col_name = col[1]
        col_type = col[2].upper().split('(')[0]  # Remove length/precision

        # Map SQLite types to PostgreSQL types
        pg_type = TYPE_MAPPING.get(col_type, 'TEXT')

        # Handle column constraints
        constraints = []
        if col[5] == 1:  # PRIMARY KEY
            constraints.append('PRIMARY KEY')
        if col[3]:  # NOT NULL
            constraints.append('NOT NULL')
        if col[4]:  # DEFAULT value
            default_val = str(col[4])
            # Handle string defaults
            if isinstance(col[4], str) and not default_val.startswith("'"):
                default_val = f"'{default_val}'"
            constraints.append(f'DEFAULT {default_val}')

        column_def = f'    "{col_name}" {pg_type}'
        if constraints:
            column_def += ' ' + ' '.join(constraints)
        column_defs.append(column_def)

    # Add primary key constraint if not already defined in columns
    if schema['primary_keys'] and not any('PRIMARY KEY' in col for col in column_defs):
        pk_columns = ', '.join(f'"{pk}"' for pk in schema['primary_keys'])
        column_defs.append(f'    PRIMARY KEY ({pk_columns})')

    create_table_sql.append(',\n'.join(column_defs))
    create_table_sql.append(');')

    # Execute the CREATE TABLE statement
    with pg_engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text('\n'.join(create_table_sql)))
            trans.commit()
            print(f"Created table {table_name}")

            # Add foreign key constraints
            if schema['foreign_keys']:
                for fk in schema['foreign_keys']:
                    fk_sql = f"""
                    ALTER TABLE "{table_name}"
                    ADD CONSTRAINT fk_{table_name}_{fk[3]}_{fk[2]}
                    FOREIGN KEY ("{fk[3]}") 
                    REFERENCES "{fk[2]}" (id);
                    """
                    try:
                        conn.execute(text(fk_sql))
                        trans.commit()
                    except Exception as e:
                        print(f"Warning: Could not add foreign key for {table_name}.{fk[3]}: {str(e)}")
                        trans.rollback()

            return True
        except Exception as e:
            trans.rollback()
            print(f"Error creating table {table_name}: {str(e)}")
            return False


async def migrate_table(conn_sqlite, pg_engine, table_name):
    """Migrate a single table from SQLite to PostgreSQL"""
    try:
        # Get the table schema
        schema = get_table_schema(conn_sqlite, table_name)

        # Create the table in PostgreSQL
        if not await create_postgres_table(pg_engine, table_name, schema):
            return False

        # Read data from SQLite
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn_sqlite)

        if df.empty:
            print(f"Table {table_name} is empty, nothing to migrate")
            return True

        # Clean column names (remove quotes if any)
        df.columns = [col.replace('"', '') for col in df.columns]

        # Write to PostgreSQL in chunks to handle large tables
        chunksize = 1000
        total_chunks = (len(df) // chunksize) + (1 if len(df) % chunksize else 0)

        with pg_engine.connect() as conn:
            for i in range(0, len(df), chunksize):
                chunk = df[i:i + chunksize]
                chunk.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists='append',
                    index=False,
                    method='multi'
                )
                print(f"Migrated chunk {i // chunksize + 1}/{total_chunks} of {table_name}")

        print(f"Successfully migrated data to table: {table_name}")
        return True

    except Exception as e:
        print(f"Error migrating table {table_name}: {str(e)}")
        return False


async def main():
    try:
        # Connect to SQLite
        conn_sqlite = get_sqlite_connection()

        # Create SQLAlchemy engine for PostgreSQL
        pg_engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@"
            f"{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"
        )

        # Get all tables
        tables = get_sqlite_tables(conn_sqlite)
        print(f"Found {len(tables)} tables to migrate: {', '.join(tables)}")

        # Disable triggers temporarily
        with pg_engine.connect() as conn:
            conn.execute(text("SET session_replication_role = 'replica';"))
            conn.commit()

        # Migrate each table
        success_count = 0
        for table in tqdm(tables, desc="Migrating tables"):
            if await migrate_table(conn_sqlite, pg_engine, table):
                success_count += 1

        # Re-enable triggers
        with pg_engine.connect() as conn:
            conn.execute(text("SET session_replication_role = 'origin';"))
            conn.commit()

        print(f"\nMigration completed! {success_count}/{len(tables)} tables migrated successfully.")

    except Exception as e:
        print(f"Migration failed: {str(e)}")
    finally:
        if 'conn_sqlite' in locals():
            conn_sqlite.close()
        if 'pg_engine' in locals():
            pg_engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())