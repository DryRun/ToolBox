min_runnumber_to_process = 280534
ptype = "904"
poolsource = "/data"
pattern = "B904_Integration_*.root"
process_lock = "process.lock"
upload_lock = "upload.lock"
cmssw_config = "/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src/hcal_dqm_local_cfg.py"
cmssw_outputpool = "/home/HCALDQM/output"
cmssw_src_directory = "/afs/cern.ch/work/c/cmshcaldqm/HCALDQM/904/CMSSW_8_0_17_toProcess904/src"
cmssw_output_template = "DQM_V0001_R{runNumber}__{runType}__Commissioning2016__DQMIO.root"
cmsRun_cmd_template = "cmsRun {cmssw_config} inputFiles=file:{pathToFileName} runType={runType}"

dqmgui_server_name = "cmshcaldqm-vm.cern.ch:8070/dqm/online-dev"
dqmupload_cmd_template = "visDQMUpload http://{server_name} {pathnameToFile}"

#
#   TODO
#
#   P5 Run Type Extraction Configuration
run_type_patterns = ["pedestal", "led", "laser", "raddam"]
laser_type_patterns = ["megatile", "sipm", "pmt", "hpd"]
laser_subdet_patterns = ["hbhe", "hbm", "hbp", "hem", "hep",
    "ho", "hf"]

runinfo_db_name = "cms_hcl_runinfo/run2009info"
sql_template = "query.sql"
quantitymap = {
    "NEVENTS" : ("STRING_VALUE","CMS.HCAL%:TRIGGERS"),
    "CONFIG_OLD" : ("STRING_VALUE", "CMS.HCAL%:FM_FULLPATH"),
    "CONFIG_NEW" : ("STRING_VALUE", "CMS.HCAL%:LOCAL_RUN_KEY"),
    "TIME" : ("TIME", "CMS.HCAL%")
}
