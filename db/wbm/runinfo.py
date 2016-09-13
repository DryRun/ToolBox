"""
Hcal Run Info DB collection of wrapping scripts.
Extraction of useful information and standardization of it to push info downstream 
"""

import os, sys, glob
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import logging

def query(cfg, run_number):
    if cfg.ptype=="local":
        return query_local(cfg, run_number)
    elif cfg.ptype=="minidaq":
        return query_minidaq(cfg, run_number)
    else:
        return

def query_local(cfg, run_number):
    def parse(out):
        out = out.split("\n")[0]
        logging.debug(out)
        v = out.rstrip(".xml").split("_")
        v = v[1:]
        t = ""
        for x in v:
            t+=x.lower()
        logging.debug(t)
        return t
    quantity = "CONFIG_NEW"
    selector_type = cfg.quantitymap[quantity][0]
    selector_name = cfg.quantitymap[quantity][1]

    cmd = "sqlplus -S %s@cms_rcms @%s %s %s %s" % (cfg.runinfo_db_name,
        cfg.sql_template, selector_type, selector_name, str(run_number))
    logging.debug(cmd)
    out, err, rt = shell.execute(cmd.split(" "))
    return parse(out)

def query_minidaq(cfg, run_number):
    pass

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    import processing_scripts.config as cfg
    print query(cfg, 280535)
