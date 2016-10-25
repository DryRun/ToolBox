"""
Hcal Run Info DB collection of wrapping scripts.
Extraction of useful information and standardization of it to push info downstream 
"""

import os, sys, glob
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import logging
import wbm_http_simple_parser as parser
import httplib
import utilities.shell_functions as shell

def query(cfg, **wargs):
    if cfg.ptype=="local":
        logging.debug("Local WBM Query")
        return query_local(cfg, **wargs)
    elif cfg.ptype=="minidaq":
        logging.debug("Minidaq WBM Query")
        return query_minidaq(cfg, **wargs)
    else:
        logging.debug("No WBM Query")
        return

def query_local(cfg, **wargs):
    """
    Returns the run type
    """
    def parse(out):
        out = out.split("\n")[0]
        logging.debug(out)
        v = out[:-4].split("_")
        v = v[1:]
        t = ""
        for x in v:
            t+=x.lower()
        logging.debug(t)
        return t
    run_number = wargs["run_number"]
    quantity = "CONFIG_NEW"
    selector_type = cfg.quantitymap[quantity][0]
    selector_name = cfg.quantitymap[quantity][1]

    cmd = "sqlplus -S %s@cms_rcms @%s %s %s %s" % (cfg.runinfo_db_name,
        cfg.sql_template, selector_type, selector_name, str(run_number))
    logging.debug(cmd)
    out, err, rt = shell.execute(cmd.split(" "))
    logging.debug(out); logging.debug(rt); logging.debug(err)
    return parse(out)

def query_minidaq(cfg, **wargs):
    """
    Returns a fed enable mask string
    """
    run_number = wargs["run_number"]
    conn = httplib.HTTPConnection("cmswbm2.cms")
    conn.request("GET", "/cmsdb/servlet/RunParameters?RUNNUMBER=%d" % run_number)
    r = conn.getresponse()
    parser.parser.feed(r.read().replace("_hwcfgKey", "TESTTAG"))
    s = ""
    for x in parser.parser.feds:
        s+=x
#    logging.debug(s)
    return s

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    import processing_scripts.config_minidaq as cfg
    s = query_minidaq(cfg, run_number=280509)
    logging.debug(s)
#     donprint query(cfg, 280535)
