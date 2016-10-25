#!/usr/bin/python
"""
various examples of db scripts
"""

import os, sys
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import sqlite3 as dbms
import utilities.shell_functions as shell
import logging

def open(dbpathname):
    conn = dbms.connect(dbpathname)
    cur = conn.cursor()
    return (conn, cur)

def create(dbpathname, table_name):
    (conn, cur) = open(dbpathname)
    #   create the Run Table
    q = ''' CREATE TABLE {table_name}
    (run_number INTEGER, run_type TEXT, num_events INTEGER, status INTEGER);
    '''.format(table_name=table_name)
    cur.execute(q)
    conn.commit()
    conn.close()

def reCreate(dbpathname, table_name):
    shell.rm(dbpathname)
    create(dbpathname, table_name)

def printDB(dbpathname, table_name):
    (conn, cur) = open(dbpathname)
    q = ''' SELECT * FROM {table_name}
    '''.format(table_name=table_name)
    logging.debug(q)
    rows = cur.execute(q).fetchall()
    for r in rows:
        logging.debug(r)

def query_select(**wargs):
    result = None
    try:
        (conn, cur) = open(wargs["dbpathname"]) 
        result = cur.execute(wargs["query"]).fetchall()
    except Exception as exc:
        logging.error("dbscripts.query_select(): Error %s with message: %s" % (
            type(exc).__name__, exc.args))
        result = None
    finally:
        conn.close()
        return result

    return result

def query_update(**wargs):
    try:
        (conn, cur) = open(wargs["dbpathname"])
        cur.execute(wargs["query"])
    except Exception as exc:
        logging.error("dbscripts.query_select(): Error %s with message: %s" % (
            type(exc).__name__, exc.args))
    finally:
        conn.commit()
        conn.close()

class SQLException(Exception):
    """Define a customary exception class"""
    def __init__(self, args):
	    logging.debug(args)
	    self.msg = args
	    self.args = args
	    self.args = args

if __name__=="__main__":
    pass
