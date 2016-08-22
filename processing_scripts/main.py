#!/usr/bin/python
"""
process Runs
"""
import os, sys, glob
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import config as cfg
import db.dqmdb.dbscripts as dbscripts
import db.dqmdb.config as dbcfg
import utilities.shell_functions as shell
import utilities.re_functions as res
import logging

thismodule = sys.modules[__name__]

def alreadyLocked(lockpath):
    if shell.exists(lockpath): return True
    shell.touch(lockpath)
    return False

def process_cmssw(*args):
    logging.debug("Runing process_cmssw()")
    return 0

def upload_dqmgui(*args):
    logging.debug("Running process_dqmgui()")
    return 0

def reCreate():
    dbscripts.reCreate()

def create():
    dbscripts.create()

def printDB():
    dbscripts.printDB()

def upload():
    """
    upload files that are processed
    """
    try:
        (conn, cur) = dbscripts.open()
        if alreadyLocked(cfg.upload_lock): 
            logging.info("upload(): Lockfile exists")
            return
        
        q = '''
        SELECT * FROM Runs WHERE status=%d
        ''' % dbcfg.processed
        runsToUpload = cur.execute(q).fetchall()
        for run in runsToUpload:
            try:
                rt = upload_dqmgui(run)
                run_number = run[0]
                if rt==0:
                    q = '''
                    UPDATE Runs 
                    SET status=%d
                    WHERE run_number=%d;
                    ''' % (dbcfg.uploaded, run_number)
                    logging.debug(q)
                    cur.execute(q)
                else:
                    raise dbscripts.SQLException("DQMGUI Uploading failed for record=%s" % str(run))
            except dbscripts.SQLException as exc:
                q = '''
                UPDATE Runs 
                SET status=%d
                WHERE run_number=%d;
                ''' % (dbcfg.uploading_failed, run_number)
                logging.debug(q)
                cur.execute(q)
                logging.error("upload(): Error %s with message: %s" % (
                    type(exc).__name__, str(exc.args)))
            except Exception as exc:
                logging.error("upload(): Error %s with message: %s" % (
                    type(exc).__name__, str(exc.args)))
            finally:
                conn.commit()
    except Exception as exc:
        pass
    finally:
        conn.commit()
        conn.close()
        shell.rm(cfg.upload_lock)

def process():
    """
    process something
    """

    #   external try
    try:
        #   configure the current processing
        runlist = glob.glob(os.path.join(cfg.poolsource, cfg.pattern))
        (conn, cur) = dbscripts.open()
        if alreadyLocked(cfg.process_lock): 
            logging.info("process(): Lockfile exists")
            return
       
        #   internal try
        logging.debug(runlist)
        for f in runlist:
            try:
                f = f.split("/")[-1]
                run_number = res.getRunNumber("local", f)
                run_type = "test"
                size = 100000
                logging.debug((run_number, run_type, size))

                #   query our db
                q = '''
                SELECT * FROM Runs WHERE run_number=%d;
                ''' % run_number
                logging.debug(q)
                results = cur.execute(q).fetchall()
                logging.debug(results)
                if len(results)==1:
                    logging.debug("Run %d is already in DB" % run_number)
                    continue
                elif len(results)>1:
                    raise Exception("More than 1 Record for run_number=%d" % run_number)
                else: # if it's ==0
                    q = '''
                    INSERT INTO Runs Values(%d, '%s', %d, %d);
                    ''' % (run_number, run_type, 0, dbcfg.processing)
                    logging.debug(q)
                    cur.execute(q)
                    rt =  process_cmssw(run_number, run_type)
                    if rt==0:
                        q = '''
                        UPDATE Runs
                        SET status=%d
                        WHERE run_number=%d;
                        ''' % (dbcfg.processed, run_number)
                        cur.execute(q)
                    else:
                        raise dbscripts.SQLException("CMSSW Processing failed for record=%s" % (
                           str(run_number, run_type)))
            except dbscripts.SQLException as exc:
                q = '''
                UPDATE Runs 
                SET status=%d
                WHERE run_number=%d;
                ''' % (dbcfg.processing_failed, run_number)
                cur.execute(q)
                logging.error("process(): Error %s with message: %s" % (
                    type(exc).__name__, str(exc.args)))
            except Exception as exc:
                logging.error("process(): Error %s with message: %s" % (
                    type(exc).__name__, str(exc.args)))
            finally:
                conn.commit()
    except Exception as exc:
        logging.error("process(): Exception caught: %s %s" % (
            type(exc).__name__, str(exc.args)))
    finally:
        conn.commit()
        conn.close()
        shell.rm(cfg.process_lock)

def test():
    logging.info("Running function test")

def main():
    #   parsing options
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--function", dest="functionName",
        help="Function to be executed", default="test")
    parser.add_option("-l", "--logfile", dest="logfile", help="Log File pathname",
        default='./log.log')
    (options, args) = parser.parse_args()

    #   init the logging
    lvl = logging.DEBUG
    logging.basicConfig(filename=options.logfile, level=lvl)

    # decide what to process
    logging.info("Started main():")
    logging.info("function to run: %s" % options.functionName)
    logging.info("log file is %s" % options.logfile)
    if hasattr(thismodule, options.functionName):
        try:
            logging.info("Starting Function=%s at %s" % (options.functionName,
                shell.gettimedate()))
            func = getattr(thismodule, options.functionName)
            func()
        except Exception as exc:
            logging.error("main(): Exception")
        finally:
            logging.info("Finished Function=%s at %s" % (options.functionName,
                shell.gettimedate()))
    else:
        logging.error("Cannot find Function=%s" % options.functionName)

if __name__=="__main__":
    main()
