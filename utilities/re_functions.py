"""
Predefine some common REs for HCAL DQM format. 
Predefine some commond patterns for files...
Predefine some functions to discover files based on patterns
"""

import re

template = "/(\w+)"

import logging
import glob

def getRunNumber(ptype, filename):
	if ptype=="local":
		return int(filename[4:-5])
	elif ptype=="904":
		return int(filename[17:-5])
	else:
		return -1

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
