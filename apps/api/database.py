import psycopg
from psycopg.rows import dict_row

def get_connection():
    return psycopg.connect(
        dbname="oscaros",
        host="localhost",
        row_factory=dict_row
    )