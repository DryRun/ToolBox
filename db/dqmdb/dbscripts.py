#!/usr/bin/python
"""
various examples of db scripts
"""

import os, sys
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import config as cfg
import sqlite3 as dbms
import utilities.shell_functions as shell
import logging

def main():
    create()

def open():
    conn = dbms.connect(cfg.dbpathname)
    cur = conn.cursor()
    return (conn, cur)

def create(table_name):
    (conn, cur) = open()

    #   create the Run Table
    q = ''' CREATE TABLE {table_name}
    (run_number INTEGER, run_type TEXT, num_events INTEGER, status INTEGER);
    '''.format(table_name=table_name)
    cur.execute(q)
    conn.commit()
    conn.close()

def reCreate():
    shell.rm(cfg.dbpathname)
    create()

def printDB(table_name):
    (conn, cur) = open()
    q = ''' SELECT * FROM {table_name}
    '''.format(table_name=table_name)
    logging.debug(q)
    rows = cur.execute(q).fetchall()
    for r in rows:
        logging.debug(r)

class SQLException(Exception):
    """Define a customary exception class"""
    def __init__(self, args):
	    logging.debug(args)
	    self.msg = args
	    self.args = args

if __name__=="__main__":
    main()
