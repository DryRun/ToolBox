"""
Predefine some common REs for HCAL DQM format. 
Predefine some commond patterns for files...
Predefine some functions to discover files based on patterns
"""

import re

template = "/(\w+)"

import logging
import glob

def shouldProcess(**wargs):
    runnumber = wargs["run_number"]
    runtype = wargs["run_type"]
    size = wargs["size"]
    cfg = wargs["cfg"]
    if cfg.ptype=="local":
        for t in cfg.run_type_patterns:
            if t in runtype and runnumber>=cfg.min_runnumber_to_process:
                return True
        return False
    elif cfg.ptype=="904":
        return True
    else:
        return False

def listRuns(cfg):
    if cfg.ptype=="local":
        logging.debug("Local Run Type Listing")
        return glob.glob(os.path.join(cfg.poolsource, "*.root"))
    elif cfg.ptype=="904":
        l1 = glob.glob(os.path.join(cfg.poolsource, "LED", cfg.pattern))
        l2 = glob.glob(os.path.join(cfg.poolsource, "PED", cfg.pattern))
        logging.debug(l1)
        logging.debug(l2)
        return l1+l2
    else:
        return []

def getRunNumber(ptype, filename):
	if ptype=="local":
		return int(filename[4:-5])
	elif ptype=="904":
		return int(filename[17:-5])
	else:
		return -1

def getRunType(ptype, filepath):
    if ptype=="904":
        if "PED" in filepath:
            return "PEDESTAL"
        elif "LED" in filepath:
            return "LED"
        else:
            return "UNKNOWNTYPE"
    else:
        return "UNKNOWNTYPE"

def match_path(path):
    """
    Match Path to the ROOT Object in the ROOT TFile
    """
    nslash = path.count("/")
    rep = ""
    if nslash>0:
        for i in range(nslash):
            rep+=template
    r = re.match(rep, path)
    l = r.groups()
    d = {}
    d["module"] = l[0]
    d["variable"] = None
    if len(l)>1:
        d["variable"] = l[1]
    d["hasher"] = "NOHASHER"
    if len(l)>2:
        d["hasher"] = l[2]

    return d

def match_filename(filename, convention="Online"):
    d = {}
    if convention == "Offline":
        r = re.match("^DQM_V(\d+)_R(\d+)((__[-A-Za-z0-9_]+){3})\.root$",
            filename)
    elif convention == "Online" : 
        r = re.match("^DQM_V(\d+)(_[A-Za-z0-9]+)?_R(\d+)\.root$",
            filename)
        l = r.groups()
        d["subsystem"] = l[1][1:]
        d["run"] = int(l[2])

    return d

if __name__=="__main__":
    d = match_filename("DQM_V0001_Hcal_R000266421.root")
    print d
