"""
file:				utilities.py
author:				Viktor Khristenko
Description:
	A Set of Utility Functions/Classes
"""

import sys, os
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)

#
#	Imports
#
import subprocess, glob, time
import logging

#	
#	File System Management
#
def mkdir(dirName):
	if not os.path.exists(dirName):
		cmd = "mkdir %s" % dirName
		subprocess.call(cmd, shell=True)

def rm(pathfile):
	cmd = "rm %s" % pathfile
	subprocess.call(cmd, shell=True)

def rmdir(pathdir):
	cmd = "rm -rf %s" % pathdir
	subprocess.call(cmd, shell=True)

def touch(pathfile):
	if not os.path.exists(pathfile):
		cmd = "touch %s" % pathfile
		subprocess.call(cmd, shell=True)

def call(cmd):
	subprocess.call(cmd, shell=True)

def exists(path):
	return os.path.exists(path)

def getsize(path):
	return os.path.getsize(path)

def fork():
	return os.fork()

def gettimedate():
	""" return (time, data) """
	return time.strftime("%X"),time.strftime("%x")

def cd(dirName):
	os.chdir(dirName)

def ls_glob(pathpattern):
	return glob.glob(pathpattern)

def ls_os(path):
	return os.listdir(path)

def split(pathfile):
	return os.path.split(pathfile)

def join(path, filename):
	return os.path.join(path, filename)

def execute(cmd_as_list):
	out="";err="";rt=100
	try:
		logging.debug(cmd_as_list)
		p = subprocess.Popen(cmd_as_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		rt = p.returncode
		logging.debug(rt)
	except Exception as exc:
            logging.error("shell_functions:execute() Error %s with message %s:" % 
                type(exc).__name__, str(exc.args))
            out = None; err=None; rt = None
	finally:
                logging.debug(out)
		logging.debug(err)
		logging.debug(rt)
		return out,err,rt

if __name__=="__main__":
	print join("/data/hcaldqm/HCALDQM/Utilities/Processing/scripts", "process.sh")
