
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

#	we are ready - either upload or process
if [ $cron_processing_type -eq 0 ];
then
	#	Commend this guy in if you have DQM GUI actually avaialable
	source $DQMGUI_BASE/current/apps/dqmgui/128/etc/profile.d/env.sh
	python $HCALDQMTOOLBOX/processing_scripts/main.py --function=upload --logfile=$HCALDQMTOOLBOX/processing_scripts/upload.log -q
elif [ $cron_processing_type -eq 1 ]; then
	cd $CMSSW_HCALDQM_BASE
	source /afs/cern.ch/cms/cmsset_default.sh 
	eval `scramv1 runtime -sh`
	python $HCALDQMTOOLBOX/processing_scripts/main.py --function=process --logfile=$HCALDQMTOOLBOX/processing_scripts/process.log -q
else
	source $DQMGUI_BASE/current/apps/dqmgui/128/etc/profile.d/env.sh
	python $HCALDQMTOOLBOX/processing_scripts/main.py --function=reupload --logfile=$HCALDQMTOOLBOX/processing_scripts/upload.log -q
fi
