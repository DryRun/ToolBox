#
#   An example of a config for db
#
import sys, os
pathToToolBox = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToToolBox)

#   define status codes
not_tobe_processed = -1
processing = 0
processed = 1
uploaded = 2
processing_failed = 3
uploading_failed = 4
