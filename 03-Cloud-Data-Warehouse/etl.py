import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description:
        Loads the staging tables by copying the data in the json files in S3
       
    Args:
        Cur: Cursor object
        Conn: Connection to Redshift
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
     Description:
        Inserts the relevent data from the staging tables to the fact and dimension tables
     
    Args:
        Cur: Cursor object
        Conn: Connection to Redshift
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description:
        Reads configs file and passes relevent credential to estalish connection to S3 and Redshift.
        Data would be loaded into staging and data inserted into the fact and dimension tables
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()