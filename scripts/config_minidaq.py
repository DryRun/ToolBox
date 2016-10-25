ptype = "minidaq"
poolsource = ""
pattern = "*.root"
process_lock = "process_minidaq.lock"
upload_lock = "upload_minidaq.lock"

cmssw_config = "/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src/hcal_dqm_local_cfg.py"
cmssw_outputpool = "/home/HCALDQM/output"
cmssw_src_directory = "/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src"
cmssw_output_template = "DQM_V0001_R{runNumber}__{runType}__Commissioning2016__DQMIO.root"
cmsRun_cmd_template = "cmsRun {cmssw_config} inputFiles=file:{pathToFileName} runType={runType}"

dqmgui_server_name = "cmshcaldqm-vm.cern.ch:8070/dqm/online-dev"
dqmupload_cmd_template = "visDQMUpload http://{server_name} {pathnameToFile}"
