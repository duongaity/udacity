"""Create your fact and dimension tables for the star schema in Redshift."""

import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop tables.

            Parameters:
                    conn (connection): instance of connection class
                    cur (cursor): instance of cursor class

            Returns:
                    none
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create tables.

            Parameters:
                    conn (connection): instance of connection class
                    cur (cursor): instance of cursor class

            Returns:
                    none
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Create your fact and dimension tables .

            Parameters:
                    none

            Returns:
                    none
    """
    # Config
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Connection to database
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                            .format(*config['CLUSTER'].values()))

    # Create cusor object
    cur = conn.cursor()

    # ETL queries
    drop_tables(cur, conn)
    create_tables(cur, conn)

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()
