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
import db.wbm.runinfo as wbm
import utilities.shell_functions as shell
import utilities.re_functions as res
import logging

thismodule = sys.modules[__name__]

def listRuns(cfg):
    """
    List all the runs
    """
    if cfg.ptype=="904":
        cmd = "eos ls %s" % cfg.poolsource
        out, err, rt = shell.execute(cmd.split(" "))
        return out
    else: return None

def listFullFilePath(f):
    cmd = "eos ls %" % (os.path.join(cfg.poolsource, f))
    out, err, rt = shell.execute(cmd.split())
    return os.path.join(cfg.poolsource, f, out)

def shouldProcess(cfg, **wargs):
    if cfg.ptype=="904":
        return True
    else: 
        return False

def getRunType(cfg, **wargs):
    """
    Obtain the Run Type of the given run
    http://www.oracle.com/technetwork/articles/dsl/python-091105.html
    """
    if cfg.ptype=="904":
        import cx_Oracle
        db = cx_Oracle.connect(cfg.oracledbstring)
        named_params = {'n_run': wargs["run_number"]}
        cursor = db.cursor()
        cursor = cursor.execute("SELECT VALUE FROM RUNSESSION_PARAMETER, RUNSESSION_STRING WHERE RUNNUMBER=:n_run AND NAME='CMS.HCALFM_LVL1_904Int:LOCAL_RUN_KEY' AND ID=RUNSESSION_PARAMETER_ID", named_params)
        string = ""
        for result in cursor:
            string = result[0].read()
        if "LED" in string.upper():
            return "LED"
        elif "PED" in string.upper():
            return "PEDESTAL"
        else: return ""
    else: return None


def alreadyLocked(lockpath):
    if shell.exists(lockpath): return True
    shell.touch(lockpath)
    return False

def process_cmssw(*kargs, **wargs):
	logging.debug("Runing process_cmssw()")
	runType = wargs["runType"]
	filepath = wargs["filepath"]
	cmd_as_list = cfg.cmsRun_cmd_template.format(cmssw_config=cfg.cmssw_config,
		pathToFileName=filepath, runType=runType).split(" ")
	logging.debug(cmd_as_list)
	out, err, rt = shell.execute(cmd_as_list)
        logging.info(out)
        logging.debug(err)
	return rt

def upload_dqmgui(*kargs, **wargs):
	logging.debug("Running process_dqmgui()")
	runNumber = wargs["runNumber"]
	runType = wargs["runType"]
	fileToUpload = os.path.join(cfg.cmssw_outputpool, 
		cfg.cmssw_output_template.format(runNumber=runNumber, runType=runType))
	cmd_as_list = cfg.dqmupload_cmd_template.format(
		server_name=cfg.dqmgui_server_name,
		pathnameToFile=fileToUpload
	).split(" ")
	logging.debug(cmd_as_list)
	out,err,rt = shell.execute(cmd_as_list)
        logging.info(out)
        logging.debug(err)
	return rt

def reCreateDB():
    dbscripts.reCreate(dbpathname=cfg.dbpathname,
        table_name=cfg.table_name)

def createDB():
    dbscripts.create(dbpathname=cfg.dbpathname, table_name=cfg.table_name)

def printDB():
    dbscripts.printDB(dbpathname=cfg.dbpathname, table_name=cfg.table_name)

def reupload():
	try:
		(conn, cur) = dbscripts.open()
		q = '''
	        SELECT * FROM Runs WHERE status=%d
		''' % dbcfg.uploading_failed
		runsToReupload = cur.execute(q).fetchall()
		for run in runsToReupload:
			try:
				rt = upload_dqmgui(runNumber=run[0],
					runType=run[1])
				runNumber = run[0]
				if rt==0:
					q = '''
					UPDATE Runs
					SET status=%d
					WHERE run_number=%d
					''' % (dbcfg.uploaded, runNumber)
					logging.debug(q)
			                cur.execute(q)
				else:
					raise dbscripts.SQLException("DQMGUI Uploading failed for record=%s" % str(run))
			except Exception as exc:
				q = '''
		                UPDATE Runs 
				SET status=%d
		                WHERE run_number=%d;
				''' % (dbcfg.uploading_failed, runNumber)
				logging.debug(q)
		                cur.execute(q)
				logging.error("upload(): Error %s with message: %s" % (
					type(exc).__name__, exc.args))
			finally:
				conn.commit()
	except Exception as exc:
                logging.error("reupload(): Error %s with message: %s" % (
                    type(exc).__name__, str(exc.args)))
	finally:
		conn.commit()
	        conn.close()

def upload():
    """
    upload files that are processed
    """
    try:
        if alreadyLocked(cfg.upload_lock): 
            logging.info("upload(): Lockfile exists")
            return
        
        q = '''
        SELECT * FROM Runs WHERE status=%d
        ''' % dbcfg.processed
        runsToUpload = dbscripts.query_select(query=q, dbpathname=cfg.dbpathname)
        for run in runsToUpload:
            try:
                rt = upload_dqmgui(runNumber=run[0],
                    runType=run[1])
                run_number = run[0]
                if rt==0:
                    q = '''
                    UPDATE Runs 
                    SET status=%d
                    WHERE run_number=%d;
                    ''' % (dbcfg.uploaded, run_number)
                    logging.debug(q)
                    dbscripts.query_update(dbpathname=cfg.dbpathname, query=q)
                else:
                    raise dbscripts.SQLException("DQMGUI Uploading failed for record=%s" % str(run))
            except Exception as exc:
                q = '''
                UPDATE Runs 
                SET status=%d
                WHERE run_number=%d;
                ''' % (dbcfg.uploading_failed, run_number)
                logging.debug(q)
                dbscripts.query_update(dbpathname=cfg.dbpathname, query=q)
                logging.error("upload(): Error %s with message: %s" % (
                    type(exc).__name__, exc.args))
            finally:
                pass
    except Exception as exc:
        pass
    finally:
        shell.rm(cfg.upload_lock)

def process():
    """
    process something
    """

    #   external try
    try:
        #   configure the current processing
	runlist = listRuns(ptype)
	logging.debug("RunList: " + str(runlist))
	if alreadyLocked(cfg.process_lock): 
		logging.info("process(): Lockfile exists")
		return
	#   build the CMSSW
	shell.execute(["cd", cfg.cmssw_src_directory])
	#shell.execute(["scram", "b", "-j", "8"])

        #   internal try
        for f in runlist:
            try:
                f = listFilePath(f)
                fstripped = f.split("/")[-1]
                run_number = res.getRunNumber(cfg.ptype, fstripped)
                run_type = getRunType(cfg, run_number=run_number)
                if not shouldProcess(run_number=run_number, 
                    run_type=run_type, cfg=cfg): continue
                logging.debug((run_number, run_type, size))

                #
                #   query our db
                #   for MT, each query is wrapped into a separate connection
                #   inefficient - but given processing time of cmssw, it's negligible
                #   
                q = '''
                SELECT * FROM Runs WHERE run_number=%d;
                ''' % run_number
                logging.debug(q)
                results = dbscripts.query_select(dbpathname=cfg.dbpathname,
                    query=q)
                if result==None: continue

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
                    dbscripts.query_update(dbpathname=cfg.dbpathname,
                        query=q)

                    rt =  process_cmssw(runType=run_type,
                        filepath=f)
                    if rt==0:
                        q = '''
                        UPDATE Runs
                        SET status=%d
                        WHERE run_number=%d;
                        ''' % (dbcfg.processed, run_number)
                        dbscripts.query_update(dbpathname=cfg.dbpathname,
                            query=q)

                    else:
                        raise dbscripts.SQLException("CMSSW Processing failed for record=%s" % str(run_number))
            except Exception as exc:
                q = '''
                UPDATE Runs 
                SET status=%d
                WHERE run_number=%d;
                ''' % (dbcfg.processing_failed, run_number)
                dbscripts.query_update(dbpathname=cfg.dbpathname,
                    query=q)
                logging.error("process(): Error %s with message: %s" % (
                    type(exc).__name__, exc.msg))
            finally:
                pass
    except Exception as exc:
        logging.error("process(): Exception caught: %s %s" % (
            type(exc).__name__, exc.args))
    finally:
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
    parser.add_option("-v", action="store_true", dest="verbose", default=True)
    parser.add_option("-q", action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    #   init the logging
    lvl = logging.DEBUG if options.verbose else logging.INFO
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
