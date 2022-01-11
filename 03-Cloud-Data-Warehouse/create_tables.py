import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Description:
        Drop all tables if they exists to clean up the database 
    
    Args:
        Cur: Cursor object
        Conn: Connection to Redshift
    """
    
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Description:
        Creates the staging and fact/dimension tables if they didn't exist to store and load data 
    
    Args:
        Cur: Cursor object
        Conn: Connection to Redshift
    """
    
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description:
        Gets credentials from config file and connects to the database
        Performs table deletion and creation to keep database fresh with relevent schema and data
    """
        
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()