#!/usr/bin/python
"""
process fiber id runs. Executable to run is from Ted Laird
"""

import os, sys, glob
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)

import logging
import time
import utilities.shell_functions as shell
import db.wbm.runinfo as wbm
import config_fiberid as cfg
import db.dqmdb.config as dbcfg
import db.dqmdb.dbscripts as dbscripts
import utilities.re_functions as res

thismodule = sys.modules[__name__]

def listRuns(cfg):
    if cfg.ptype=="local":
        logging.debug("Local Run Type Listing")
        return glob.glob(os.path.join(cfg.poolsource, "*.root"))
    elif cfg.ptype == "minidaq":
        pass
    elif cfg.ptype=="904":
        pass

def getRunType(cfg, **wargs):
    if cfg.ptype=="904":
        pass
    elif cfg.ptype=="minidaq":
        pass
    elif cfg.ptype=="local":
        return wbm.query(cfg, **wargs)

def alreadyLocked(lockpath):
    if shell.exists(lockpath): return True
    shell.touch(lockpath)
    return False

def shouldProcess(cfg, **wargs):
    if cfg.ptype=="904":
        return False
    elif cfg.ptype=="minidaq":
        return False
    elif cfg.ptype=="local":
        run_number = wargs["run_number"]
        run_type = wargs["run_type"]
        if run_number>=cfg.min_runnumber_to_process and "fiberid" in run_type.lower():
            return True
        else:
            return False

def execute(filepath):
    cmd = "%s %s" % (cfg.executable, filepath)
    cmd_as_list = cmd.split()
    out, err, rt = shell.execute(cmd_as_list)
    logging.error(err)
    return rt

def createDB():
    dbscripts.create(cfg.dbpathname, cfg.table_name)

def process():
    """
    process something
    """
    logging.info("Running function process")
    try:
        runlist = listRuns(cfg)
        logging.debug("RunList: " + str(runlist))
        (conn, cur) = dbscripts.open(cfg.dbpathname)
        if alreadyLocked(cfg.process_lock):
            logging.info("process(): Lockfile exists")
            return

        logging.debug("Starting the Run Loop")
        #   do initialization before looping over all files
        for f in runlist:
            try:
                fstripped = f.split("/")[-1]
                logging.debug(fstripped)
                run_number = res.getRunNumber(cfg.ptype, fstripped)
                logging.debug(run_number)
                run_type = getRunType(cfg, run_number=run_number)
                logging.debug((run_number, run_type))
                if not shouldProcess(run_number=run_number,
                    run_type=run_type, cfg=cfg): continue
                q = '''
                SELECT * FROM %s WHERE run_number=%d;
                ''' % (cfg.table_name, run_number)
                logging.debug(q)
                results = cur.execute(q).fetchall()
                logging.debug(results)
                if len(results)==1:
                    logging.debug("Run %s is already in DB" % run_number)
                    continue
                elif len(results)>1:
                    raise Exception("More than 1 Record for run_number=%d" % run_number)
                else:
                    q = '''
                    INSERT INTO %s Values(%d, '%s', %d, %d);
                    ''' % (cfg.table_name, run_number, run_type, 0, dbcfg.processing)
                    logging.debug(q)
                    cur.execute(q)
                    rt = execute(filepath=f)
                    if rt==0:
                        q = '''
                        UPDATE %s 
                        SET status=%d
                        WHERE run_number=%d;
                        ''' % (cfg.table_name, dbcfg.processed, run_number)
                        cur.execute(q)
                    else:
                        raise dbscripts.SQLException("Processing failed for record=%s" % str(run_number))
            except Exception as exc:
                q = '''
                UPDATE %s
                SET status=%d
                WHERE run_number=%d;
                ''' % (cfg.table_name, dbcfg.processing_failed, run_number)
                cur.execute(q)
                logging.error("process(): Error %s with message: %s" % (
                    type(exc).__name__, exc.args))
            finally:
                conn.commit()
    except Exception as exc:
        logging.error("process(): Exception caught: %s %s" % (
            type(exc).__name__, exc.args))
    finally:
        conn.commit()
        conn.close()
        shell.rm(cfg.process_lock)

def test():
    logging.info("Running function test")

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--function", dest="functionName",
        help="Function to be executed", default="test")
    parser.add_option("-l", "--logfile", dest="logfile", help="Log File pathname",
        default='./log.log')
    parser.add_option("-v", action="store_true", dest="verbose", default=True)
    parser.add_option("-q", action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    #init the logging
    lvl = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(filename=options.logfile, level=lvl)

    # decide what to process
    logging.info("")
    logging.info("-"*40)
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
    logging.info("-"*40)

if __name__=="__main__":
    main()
