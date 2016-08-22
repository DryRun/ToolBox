poolsource = "."
pattern = "USC_*.root"
process_lock = "process.lock"
upload_lock = "upload.lock"

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
