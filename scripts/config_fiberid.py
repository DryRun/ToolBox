min_runnumber_to_process = 270688
ptype="local"
poolsource = "/hcaldepot1/data"
pattern = "*.root"
process_lock = "process_fiberid.lock"
output = "./"
executable = "echo"
dbpathname = "./fiberidruns.db"
table_name = "FiberIdRuns"
runinfo_db_name = "cms_hcl_runinfo/run2009info"
sql_template = "/data/hcaldqm/HCALDQM/ToolBox/db/wbm/query.sql"
quantitymap = {
    "NEVENTS" : ("STRING_VALUE","CMS.HCAL%:TRIGGERS"),
    "CONFIG_OLD" : ("STRING_VALUE", "CMS.HCAL%:FM_FULLPATH"),
    "CONFIG_NEW" : ("STRING_VALUE", "CMS.HCAL%:LOCAL_RUN_KEY"),
    "TIME" : ("TIME", "CMS.HCAL%")
}
