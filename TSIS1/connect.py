import psycopg2

from config import load_config


def connect(config=None):
    """Connect to the PostgreSQL server.

    Without arguments the parameters are read from database.ini.
    Raises the original error on failure so the caller can show it.
    """
    if config is None:
        config = load_config()

    try:
        return psycopg2.connect(**config)
    except (Exception, psycopg2.DatabaseError) as error:  
        print(f"Could not connect to the database: {error}")
        raise


if __name__ == "__main__":
    conn = connect()
    print("Connected to the PostgreSQL server.")
    conn.close()
