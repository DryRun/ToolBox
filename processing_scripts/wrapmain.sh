
#	either upload (0) or process (1)
cron_processing_type=$1

#	prepare the env vars
#source /afs/cern.ch/work/c/cmshcaldqm/HCALDQM/ToolBox/env.sh
source $HCALDQM/ToolBox/env.sh
DQMGUI_BASE=/home/HCALDQM/GUI
CMSSW_HCALDQM_BASE=/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src

#	we are ready - either upload or process
if [ $cron_processing_type -eq 0 ];
then
	#	Commend this guy in if you have DQM GUI actually avaialable
#	source $DQMGUI_BASE/current/apps/dqmgui/128/etc/profile.d/env.sh
	python $HCALDQMTOOLBOX/processing_scripts/main.py --function=upload --logfile=upload.log
else
#	cd $CMSSW_HCALDQM_BASE
#	cmsenv
	python $HCALDQMTOOLBOX/processing_scripts/main.py --function=process --logfile=process.log
fi
