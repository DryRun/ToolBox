#!/bin/bash

#	either upload (0) or process (1)
cron_processing_type=$1

#	prepare the env vars
WORKHOME=/afs/cern.ch/work/c/cmshcaldqm
source $WORKHOME/HCALDQM/ToolBox/env.sh
DQMGUI_BASE=/home/HCALDQM/GUI
CMSSW_HCALDQM_BASE=/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src
export SCRAM_ARCH=slc6_amd64_gcc493

echo $DQMGUI_BASE
echo $CMSSW_HCALDQM_BASE
echo $SCRAM_ARCH

processing_904_lock=/tmp/processing_904.lock
uploading_904_lock=/tmp/uploading_904.lock

#	we are ready - either upload or process
if [ $cron_processing_type -eq 0 ];
then
	trap "rm $uploading_904_lock; exit" SIGHUP SIGINT SIGTERM
	#	exit if it has already been locked
	if [ -f $uploading_904_lock ];
	then
		exit
	else
		touch $uploading_904_lock
	fi
	#	source and upload
	source $DQMGUI_BASE/current/apps/dqmgui/128/etc/profile.d/env.sh
	python $HCALDQMTOOLBOX/scripts/main_904.py -v --function=upload --logfile=$HCALDQMTOOLBOX/scripts/upload_904.log -q
	rm $uploading_904_lock
elif [ $cron_processing_type -eq 1 ]; then
	trap "rm $processing_904_lock; exit" SIGHUP SIGINT SIGTERM
	#	lock it up
	if [ -f $processing_904_lock ];
	then
		exit
	else
		touch $processing_904_lock
	fi
	#	process
	cd $CMSSW_HCALDQM_BASE
	source /afs/cern.ch/cms/cmsset_default.sh 
	eval `scramv1 runtime -sh`
	cd $HCALDQMTOOLBOX/scripts
	export TNS_ADMIN=/afs/cern.ch/project/oracle/admin
	python $HCALDQMTOOLBOX/scripts/main_904.py -v --function=process --logfile=$HCALDQMTOOLBOX/scripts/process_904.log -q
	rm $processing_904_lock
else
	source $DQMGUI_BASE/current/apps/dqmgui/128/etc/profile.d/env.sh
	python $HCALDQMTOOLBOX/scripts/main.py -v --function=reupload --logfile=$HCALDQMTOOLBOX/scripts/upload.log -q
fi
