#
#   An example of a config for db
#
import sys, os
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)

#   db 
dbpathname = os.path.join(pathToToolBox, "rundb.db")

#   define status codes
processing = 0
processed = 1
uploaded = 2
processing_failed = 3
uploading_failed = 4
