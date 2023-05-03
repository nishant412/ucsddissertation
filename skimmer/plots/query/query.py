import psycopg2
import pickle
from pathlib import Path

def create_pickle_file(path, queryFile, recreate=False):
    with open(queryFile) as f:
        query = f.readlines()

    return create_pickle(path, query, recreate)

def create_pickle(path, queryArr, recreate=False):
    res = []
    file = Path(path)
    if not file.is_file() or recreate:
        res = run_query(' '.join(queryArr))
        with file.open('wb') as f_out:
            pickle.dump(res, f_out)
    else:
        with file.open('rb') as f_in:
            res = pickle.load(f_in)
    return res


def run_query(query):
    DB_HOST = 'localhost'
    DB_USER = 'server'
    DB_PASS = 'CutePuppies123!'
    DB_NAME = 'skimmer'
    conn = psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
