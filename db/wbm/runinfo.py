"""
Hcal Run Info DB collection of wrapping scripts
"""

import os, sys, glob
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)
import logging
import config as cfg

def query(run_number):
    quantity = "CONFIG_NEW"
    selector_type = cfg.quantitymap[quantity][0]
    selector_name = cfg.quantitymap[quantity][1]

    cmd = "sqlplus -S %s@cms_rcms @%s %s %s %s" % (cfg.runinfo_db_name,
        cfg.sql_template, selector_type, selector_name, str(run_number))

if __name__=="__main__":
    pass
