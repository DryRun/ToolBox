"""
Description of all the variables used to monitor the state of the HCAL detector.
All the descriptions are generated on the per-variable basis
"""

from layout import Group

#
#	Descriptions
#
summarydesconline = """Summary. Anything that is not either WHITE or GREEN or Gray is BAD.<br> Color Scheme:<br><font color='green'>GOOD</font> for GOOD<br><font color='yellow'>PROBLEMATIC</font> for Problematic<br><font color='red'>BAD</font> for BAD<br><font color='black'>RESERVED</font> Not used at the moment <br><font color='gray'>NCDAQ with Gray Font</font> FED is excluded from cDAQ<br>WHITE color stands for INAPPLICABLE flag<br>FED(Y) vs LS(X). All the Monitoring Tasks are summarized. For details... """
summarydescoffline = """Summary. Anything that is not either WHITE or GREEN or Gray is BAD.<br> Color Scheme:<br><font color='green'>GOOD</font> for GOOD<br><font color='yellow'>PROBLEMATIC</font> for Problematic<br><font color='red'>BAD</font> for BAD<br><font color='black'>RESERVED</font> Not used at the moment <br>WHITE color stands for INAPPLICABLE flag<br>Flag(Y) vs FED(X). All the Monitoring Tasks are summarized. For details... """

calibhelpdescfullst = "Statistics over the whole Run is combined. Either all LSs up to the current one or up to end of the Run"
calibhelpdesc1LS = "Statistics over 1LS only is combined"

corrRatioDef = " Correlation Ratio is defined as min(Et_d,Et_e)/max(Et_d, Et_e) - namely, as the min/max between emulator and data Et."

#
#   All the variables are specified per each Analysis Module.
#   The idea is very simple - relink all the histograms first as single plot layouts
#   then we go and group them to produce group-like layouts.
#
variables= {
	'PEDESTAL' : {
		"Mean" : "Pedestal Mean Distributions " + calibhelpdescfullst,
		"RMS" : "Pedestal RMS Distributions " + calibhelpdescfullst,
		"MeanDBRef" : "Comparison of Pedestal Mean with CondBD" + calibhelpdescfullst,
		"RMSDBRef" : "Comparison of Pedestal RMS with the CondDB " + calibhelpdescfullst,
		"Missing" : "Missing channels w.r.t. CondDB. "+ calibhelpdescfullst,
		"MeanBad" : "Bad Pedestal Means w.r.t. CondDB. " + calibhelpdescfullst,
		"RMSBad" : "Bad Pedestal RMS w.r.t. CondDB. " + calibhelpdescfullst,
	
		"Mean1LS" : "Pedestal Mean Distributions " + calibhelpdesc1LS,
		"RMS1LS" : "Pedestal RMS Distributions " + calibhelpdesc1LS,
		"MeanDBRef1LS" : "Comparison of Pedestal Mean with CondBD" + calibhelpdesc1LS,
		"RMSDBRef1LS" : "Comparison of Pedestal RMS with the CondDB " + calibhelpdesc1LS,
		"Missing1LS" : "Missing channels w.r.t. CondDB. "+ calibhelpdesc1LS,
		"MeanBad1LS" : "Bad Pedestal Means w.r.t. CondDB. " + calibhelpdesc1LS,
		"RMSBad1LS" : "Bad Pedestal RMS w.r.t. CondDB. " + calibhelpdesc1LS,

		"MissingvsLS" : "Missing channels vs LS",
		"OccupancyvsLS" : "Occupancy vs LS (Number of unique channels read out per LS)",
		"NBadMeanvsLS" : "Number of channels with Bad Mean w.r.t. CondDB vs LS",
		"NBadRMSvsLS" : "Number of channels with bad RMSs w.r.t. CondDB vs LS",
		"OccupancyEAvsLS" : "Occupancy vs LS. Averaged over all events per LS",
		"SummaryvsLS" : "Calibration "+summarydesconline,
	},

	'RAW' : {
		"BadQuality" : "Channels that were marked as Bad Quality by Unpacker. It includes, but not limited to, CapId nonrotation, validity bits checks, etc..."+calibhelpdescfullst,
		"BadQualityvsBX" :  "Distribution of Bad Channels vs Bunch Crossing",
		"BadQualityvsLS" : "Distribution of Bad Channels vs Lumi Section",
		"BcnMsm" : "BX Mismatches between individual uHTR and AMC13",
		"EvnMsm" : "Event Number mismatches between individual uHTR and AMC13",
                "OrnMsm" : "Orbit Number Mismatches between uHTR and AMC13",
		"SummaryvsLS" : "RAW Summary "+summarydesconline,
	},

	'DIGI' : {
		"SummaryvsLS" : "DIGI Summary "+summarydesconline,
		"ADC" : "ADC Distributions per 1 TS. ",
		"DigiSize" : "Digi Size Distributions. ",
		"DigiSizevsLS" : "Digi Size vs LS",
		"Missing1LS" : "Channels missing per 1LS. Reset every 10LSs. ",
		"Occupancy" : "Occupancy. ",
		"OccupancyCut" : "Occupancy after a cut. ",
		"OccupancyvsLS" : "Occupancy vs LS. ",
		"OccupancyCutvsBX" : "Occupancy vs BX",
		"OccupancyCutvsLS" : "Occupancy Cut vs LS",
		"OccupancyCutvsieta" : "Occupancy vs ieta (Cut is applied)",
		"OccupancyCutvsiphi" : "Occupancy vs iphi (Cut is applied)",
		"OccupancyCutvsiphivsLS" : "Occupancy Distribution iphi vs LS (Cut is applied)",
		"Occupancyvsieta" : "Occupancy vs ieta (No cuts)", 
		"Occupancyvsiphi" : "Occupancy vs iphi (no cuts)",
		"Q2Q12vsLS" : "Charge in TS2 over the sum of charges in TS1 and TS2 vs LS. ",
		"Shape" : "Signal Shape. ",
		"SumQ" : "Signal Amplitude ",
		"SumQvsLS" : "Signal Amplitude vs LS (cut is applied). ",
		"SumQvsBX" : "Signal Amplitude vs BX (cut is applied). ",
		'TimingCut' : "Charge Weighted DIGI Timing (Cut on the signal amplitude is applied). ",
		"TimingCutvsieta" : "Charge weighted DIGI Timing vs ieta (Cut on the signal amplitude is applied). ",
		"TimingCutvsiphi" : "Charge weighted DIGI Timing vs iphi (Cut on the signal amplitude is applied). ",
		"TimingvsLS" : "Timing either @DIGI level vs LS. ",
		"fC" : "fC per TS distributions. ",
                "Dead" : "Dead Cells over a period of 1 Run"
	},

	'RECO' : {
		'SummaryvsLS' : "RECO Summary. " + summarydesconline,
                "Summary" : "RECO Summary. " + summarydescoffline,
		"Energy" : "Energy Distributions. ",
		"EnergyvsBX" : "Energy vs BX (Cut is applied) ",
		"EnergyvsLS" : "Energy vs LS (Cut is applied) ",
		"Energyvsieta" : "Energy vs ieta (Cut is applied) ",
		"Energyvsiphi" : "Energy vs iphi (Cut is applied) ",
		'Occupancy' : "Occupancy Distribution ",
		"OccupancyCut" : "Occupancy Distribution (cut is applied on energy) ",
		'OccupancyCutvsBX' : "Occupancy vs BX (cut is applied) ",
		'OccupancyCutvsLS' : "Occupancy vs LS (cut is applied) ",
		"OccupancyCutvsieta" : "Occupancy Distribution vs ieta (cut is applied)",
		"OccupancyCutvsiphi" : "Occupancy Distribution vs iphi (cut is applied)",
		"OccupancyCutvsiphivsLS" : "Occupancy Distribution iphi vs LS (cut is applied)",
		"OccupancyvsLS" : "Occupancy vs LS (no cuts applied) ",
		"Occupancyvsieta" : "Occupancy vs ieta (no cuts applied) ",
		'Occupancyvsiphi' : "Occupancy vs iphi (no cuts applied) ",
		"TimingCut" : "Timing @RECO (cut is applied) ",
		"TimingCutvsLS" : "Timing @RECO vs LS (cut is applied) ",
		"TimingvsEnergy" : "Timing @RECO vs Energy Distributions. ",
		"TimingCutvsBX" : "Timing $RECO vs BX (Cut is  applied)",
		"TimingCutvsieta" : "Timing @RECO vs ieta (cut is applied)",
		"TimingCutvsiphi" : "Timing @RECO vs iphi (cut is applied)",
	},

	'TP' : {
		'SummaryvsLS' : "Trigger Primitives Summary. " + summarydesconline,
                "Summary" : "Trigger Primitives Summary. " + summarydescoffline,
		"EtCorr" : "Et Correlation Distributions. Emulator(Y) vs Data(X). Channels not present in respective Collections are plotted as Et=-2. 1x1 for HF is used ",
		"EtCorr2x3" : "HF 2x3 Correlation", 
		"EtCorrRatio" : "Et Correlation Ratio. It is always min(etd, ete)/max(etd, ete). "+corrRatioDef,
		"EtCorrRatiovsBX" : "Et Correlation Ratio vs BX"+corrRatioDef,
		"EtCorrRatiovsLS" : "Et Correlation Ratio vs LS"+corrRatioDef,
		"EtData" : "Et Data Distributions. ",
		"EtEmul" : "Et Emulator Distributions. ",
		"EtCutDatavsBX" : "Et Data vs BX (cut is applied)",
		"EtCutDatavsLS" : "Et Data vs LS (cut is applied)",
		"EtCutEmulvsBX" : "Et Emulator vs BX (cut is applied)",
		"EtCutEmulvsLS" : "Et Emulator vs LS (cut is applied)",
		"EtMsm" : "Distribution of channels with mismatched Et ",
		"FGCorr" : "Correction of Fine Grain Bit",
		"FGMsm" : "Distribution of channels with mismatched Fine Grain Bit",
		"MsnData" : "Distribution of channels missing from Data w.r.t. Emulator",
		"MsnEmul" : "Distribution of channels missing from Emulator w.r.t. Data",
		'MsnCutDatavsBX' : "Number of Channels missing from Data w.r.t. Emulator vs BX. (cut is applied)",
		'MsnCutDatavsLS' : "Number of Channels missing from Data w.r.t. Emulator vs LS. (cut is applied)",
		'MsnCutEmulvsBX' : "Number of Channels missing from Emulator w.r.t. Data vs BX. (cut is applied) ",
		'MsnCutEmulvsLS' : "Number of Channels missing from Emulator w.r.t. Data vs LS. (cut is applied)",
	
		"OccupancyCutData" : "Occupancy Distributions for Data with a cut on Et",
		"OccupancyCutEmul" : "Occupancy Distributions for Emulator with a cut on Et",
		'EtMsmRatiovsBX' : "Rate of the Et Mismatches vs BX. ",
		"EtMsmRatiovsLS" : "Rate of the Et Mismatches vs LS. ",
		"OccupancyData" : "Occupancy Distributions for Data",
		"OccupancyEmul" : "Occupancy Distributions for Emulator",
		'OccupancyCutDatavsBX' : 'Data Occupancy vs BX (cut applied)',
		'OccupancyCutDatavsLS' : 'Data Occupancy vs LS (cut applied)',
		'OccupancyCutEmulvsBX' : 'Emul Occupancy vs BX (cut applied)',
		'OccupancyCutEmulvsLS' : 'Emul Occupancy vs LS (cut applied)',
		'OccupancyData2x3' : "Data Occupancy for 2x3 TPs for HF",
		"OccupancyEmul2x3" : "Emulator Occupancy for 2x3 TPs for HF",
		'OccupancyDatavsBX' : 'Data Occupancy vs BX (no cuts applied)',
		'OccupancyDatavsLS' : 'Data Occupancy vs LS (no cuts applied)',
		'OccupancyEmulvsBX' : 'Emul Occupancy vs BX (no cuts applied)',
		'OccupancyEmulvsLS' : 'Emul Occupancy vs LS (no cuts applied)',
	},

	'DIGI_VMEvsuTCA' : {
		"ADCMsnVME" : "ADC Distribution for Missing VME Digis",
		"ADCMsnuTCA" : "ADC Distribution for Missing uTCA Digis",
		"ADC" : "ADC Correlation for all Time Slices VME(Y) vs uTCA(X)",
		"ADC_TS0" : "ADC Correlation for TS0. VME(Y) vs uTCA(X)",
		"ADC_TS1" : "ADC Correlation for TS1. VME(Y) vs uTCA(X)",
		"ADC_TS2" : "ADC Correlation for TS2. VME(Y) vs uTCA(X)",
		"ADC_TS3" : "ADC Correlation for TS3. VME(Y) vs uTCA(X)",
		"ADC_TS4" : "ADC Correlation for TS4. VME(Y) vs uTCA(X)",
		"ADC_TS5" : "ADC Correlation for TS5. VME(Y) vs uTCA(X)",
		"ADC_TS6" : "ADC Correlation for TS6. VME(Y) vs uTCA(X)",
		"ADC_TS7" : "ADC Correlation for TS7. VME(Y) vs uTCA(X)",
		"ADC_TS8" : "ADC Correlation for TS8. VME(Y) vs uTCA(X)",
		"ADC_TS9" : "ADC Correlation for TS9. VME(Y) vs uTCA(X)",
		'Missing' : "Channels missing from one ELECTRONICS UNIT and present in the other! Note, every plot designates 1 FED, therfore if uHBHE FED shows up that means that this channel is present in VME but absent in uHBHE",
		"Missing_VME" : "Digis missing from VME collection and present in uTCA",
		"Missing_uTCA" : "Digis missing from uTCA collection and present in VME",
		"Mismatched" : "Digis for which ADCs are mismatched",
	},

	'TP_VMEvsuTCA' : {
		"Et" : "Et Correlation over all TS. VME(Y) vs uTCA(X)",
		"Et_TS0" : "Et Correlation for TS0. VME(Y) vs uTCA(X)",
		"Et_TS1" : "Et Correlation for TS1. VME(Y) vs uTCA(X)",
		"Et_TS2" : "Et Correlation for TS2. VME(Y) vs uTCA(X)",
		"Et_TS3" : "Et Correlation for TS3. VME(Y) vs uTCA(X)",
		"FG_TS0" : "FG Correlation for TS0. VME(Y) vs uTCA(X)",
		"FG_TS1" : "FG Correlation for TS1. VME(Y) vs uTCA(X)",
		"FG_TS2" : "FG Correlation for TS2. VME(Y) vs uTCA(X)",
		"FG_TS3" : "FG Correlation for TS3. VME(Y) vs uTCA(X)",
		"EtMsm" : "Distrubution of channels that have Et mismatched",
		"FGMsm" : "Distribution of channels that have FG bit mismatched",
		"Missing" : "Distribution of channels missing from 1 ELECTRONICS UNIT and present in the other"
	},

	"QIE10" : {
		"ADC" : "QIE10 ADC Distribution",
		"LETDC" : "QIE10 Leading Edge TDC Distribution",
		"LETDCvsADC" : "QIE10 Leading Edge TDC vs ADC Distribution",
		"TETDCvsADC" : "QIE10 Trailing Edge TDC vs ADC Distribution"
	},

	"RunInfo" : {
		"KnownBadChannels" : "Channels that come from Hcal Channel Quality Object from Conditions."
	}
}

#
#	All the links to twiki descriptions of each analysis module
#
links = {
		"RAW":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Raw_Task_Description",
		"DIGI":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Digi_Task_Description",
		"RECO":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#RecHit_Task_Description",
		"TP":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#TP_Task_Description",
		"Summary":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Summary_Generation_Description",
		"PEDESTAL":"https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Pedestal_Task_Description",
		"DIGI_VMEvsuTCA" : "https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Digi_Comparison_Task_VME_vs_uTCA",
		"TP_VMEvsuTCA" : "https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Trigger_Primitives_Comparison_Ta",
		"QIE10" : "https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#QIE10_Task",
		"RunInfo" : "https://twiki.cern.ch/twiki/bin/view/CMS/HcalDQMRun2TaskDescription#Run_Info"
}

#
#	Attach all the twiki links to all the variables!
#
for module in variables.keys():
	for var in variables[module].keys():
		variables[module][var] += " <a href='%s'>Details...</a>" % links[module]

analysis_tasks = {
	"RawTask" : "RAW", "DigiTask" : "DIGI", "RecHitTask" : "RECO", 
	"TPTask" : "TP",
	"DigiComparisonTask" : "DIGI_VMEvsuTCA", 
	"TPComparisonTask" : "TP_VMEvsuTCA",
	"PedestalTask" : "PEDESTAL", "QIE10Task" : "QIE10",
	"RunInfo" : "RunInfo",
        "DigiRunHarvesting" : "DIGI", "RawRunHarvesting" : "RAW", "RecoRunHarvesting" : "RECO", "TPRunHarvesting" : "TP"};

#
#	Physics Stream
#
physgroups = [
	Group("00 Run Summary", False, var="SummaryvsLS",
		hasher="NOHASHER"),
        Group("00 Run Summary", False, var="Summary", hasher="NOHASHER"),

	#
	#	RAW groups
	#
	Group("01 RAW Bad Quality", False, var="BadQualityvsBX"),
	Group("01 RAW Bad Quality", False, var="BadQualityvsLS"),

	Group("02 RAW Bad Quality depth", True, var="BadQuality", hasher="depth"),
	Group("03 RAW Bcn(Evn) Mismatches", False, var="BcnMsm", hasher="Electronics"),
	Group("03 RAW Bcn(Evn) Mismatches", False, var="EvnMsm", hasher="Electronics"),

	#
	#	DIGI
	#
	Group("04 DIGI Occupancy", True, var="Occupancy", hasher="depth", task="DIGI"),
	Group("05 DIGI Occupancy vs LS", False, var="OccupancyvsLS", 
		hasher="Subdet", task="DIGI"),
	Group("06 DIGI Occupancy Cut", True, var="OccupancyCut", hasher="depth",
		task="DIGI"),
	Group("07 DIGI Occupancy Cut vs BX", True, var="OccupancyCutvsBX", 
		hasher="Subdet", task="DIGI"),
	Group("08 DIGI Occupancy Cut vs LS", True, var="OccupancyCutvsLS", 
		hasher="Subdet", task="DIGI"),
	Group('09 DIGI Occupancy Cut vs iphi', True, var="OccupancyCutvsiphi",
		hasher="SubdetPM", task="DIGI"),
	Group("10 DIGI Occupancy Cut vs ieta", True, var="OccupancyCutvsieta",
		hasher="Subdet", task="DIGI"),
	Group("11 DIGI Amplitude vs LS", True, var="SumQvsLS",
		hasher="SubdetPM", task="DIGI"),
	Group("12 DIGI Amplitude vs BX", True, var="SumQvsBX",
		hasher="SubdetPM", task="DIGI"),

	Group("13 DIGI Timing", True, var="TimingCut", hasher="depth", task="DIGI"),
	Group("14 DIGI Timing", True, var="TimingCut", hasher="SubdetPM",
		task="DIGI"),
	Group("15 DIGI Timing vs iphi", True, var="TimingCutvsiphi", 
		hasher="SubdetPM", task="DIGI"),
	Group("16 DIGI Timing vs ieta", True, var="TimingCutvsieta",
		hasher="Subdet", task="DIGI"),
	Group("17 DIGI Timing vs LS", True, var="TimingvsLS",
		hasher="FED", task="DIGI"),

	#
	#	RECO groups: 
	#
	Group("18 RECO Energy", True, var="Energy", hasher="Subdet", task="RECO"),
	Group("19 RECO Energy", True, var="Energy", hasher="depth",
		task="RECO"),
	Group("20 RECO Energy vs LS", True, var="EnergyvsLS", 
		hasher="SubdetPM", task="RECO"),
	Group("21 RECO Energy vs ieta", True, var="Energyvsieta", 
		hasher="Subdet", task="RECO"),
	Group("22 RECO Energy vs iphi", True, var="Energyvsiphi", 
		hasher="SubdetPM", task="RECO"),
	Group("23 RECO Occupancy", True, var="Occupancy", hasher="depth",
		task="RECO"),
	Group("24 RECO Occupancy vs LS", True, var="Occupancy", hasher="Subdet",
		task="RECO"),
	Group("25 RECO Occupancy Cut", True, var="OccupancyCut", hasher="depth",
		task="RECO"),
	Group("26 RECO Occupancy Cut vs LS", True, 
		var="OccupancyCutvsLS", hasher="Subdet", task="RECO"),
	Group("27 RECO Occupancy Cut vs ieta", True, 
		var="OccupancyCutvsieta", hasher="Subdet", task="RECO"),
	Group("28 RECO Occupancy Cut vs iphi", True, 
		var="OccupancyCutvsiphi", hasher="SubdetPM", task="RECO"),


	Group("29 RECO Timing", True, var="TimingCut", hasher="depth",
		task="RECO"),
	Group("30 RECO Timing", True, var="TimingCut", hasher="SubdetPM",
		task="RECO"),
	Group("31 RECO Timing vs LS", True, var="TimingCutvsLS", hasher="FED",
		task="RECO"),
	Group("32 RECO Timing vs ieta", True, var="TimingCutvsieta",
		hasher="Subdet", task="RECO"),
	Group("33 RECO Timing vs iphi", True, var="TimingCutvsiphi",
		hasher="SubdetPM", task="RECO"),
	Group("34 RECO HBHEabc Timing", False, 
		var="TimingCut", hasher="HBHEPartition",task="RECO"),
	Group("35 RECO Timing vs Energy", True, var="TimingvsEnergy", 
		hasher="SubdetPM", task="RECO"),

	#
	#	Trigger Primitives
	#
	Group("36 TP Et Correlation", False, var="EtCorr", hasher="TTSubdet",
		task="TP"),
	Group("37 TP Et Correlation Ratio", True, var="EtCorrRatio", task="TP",
		hasher="NOHASHER"),
	Group("38 TP Et Correlation Ratio vs LS", True, var="EtCorrRatiovsLS",
		task="TP", hasher="TTSubdet"),
	Group("39 TP Et Cut Distributions", True, var="EtCutData",
		task="TP", hasher="NOHASHER"),
	Group("39 TP Et Cut Distributions", True, var="EtCutEmul",
		task="TP", hasher="NOHASHER"),
	Group("40 TP Et Distributions", True, var="EtData",
		task="TP", hasher="NOHASHER"),
	Group("40 TP Et Distributions", True, var="EtEmul",
		task="TP", hasher="NOHASHER"),
	Group("41 TP Et Distributions", True, var="EtData",
		task="TP", hasher="TTSubdet"),
	Group("41 TP Et Distributions", True, var="EtEmul",
		task="TP", hasher="TTSubdet"),
	Group("42 TP Et(FG) Mismatches", True, var="EtMsm",
		task="TP", hasher="NOHASHER"),
	Group("42 TP Et(FG) Mismatches", True, var="FGMsm",
		task="TP", hasher="NOHASHER"),
	Group("43 TP Et Mismatches Rate vs LS", True, var="EtMsmRatiovsLS",
		task="TP", hasher="TTSubdet"),
	Group("44 TP Occupancy", True, var="OccupancyData",
		task="TP", hasher="NOHASHER"),
	Group("44 TP Occupancy", True, var="OccupancyEmul",
		task="TP", hasher="NOHASHER"),
	Group("45 TP Occupancy Cut", True, var="OccupancyCutData",
		task="TP", hasher="NOHASHER"),
	Group("45 TP Occupancy Cut", True, var="OccupancyCutEmul",
		task="TP", hasher="NOHASHER"),
	Group("46 TP Occupancy vs BX", True, var="OccupancyDatavsBX",
		task="TP", hasher="TTSubdet"),
	Group("46 TP Occupancy vs BX", True, var="OccupancyEmulvsBX",
		task="TP", hasher="TTSubdet"),
	Group("47 TP Occupancy vs LS", True, var="OccupancyDatavsLS",
		task="TP", hasher="TTSubdet"),
	Group("47 TP Occupancy vs LS", True, var="OccupancyEmulvsLS",
		task="TP", hasher="TTSubdet"),
	Group("48 TP Occupancy Cut vs BX", True, var="OccupancyCutDatavsBX",
		task="TP", hasher="TTSubdet"),
	Group("48 TP Occupancy Cut vs BX", True, var="OccupancyCutEmulvsBX",
		task="TP", hasher="TTSubdet"),
	Group("49 TP Occupancy Cut vs LS", True, var="OccupancyCutDatavsLS",
		task="TP", hasher="TTSubdet"),
	Group("49 TP Occupancy Cut vs LS", True, var="OccupancyCutEmulvsLS",
		task="TP", hasher="TTSubdet"),
	Group("50 TP Et Data vs BX(LS)", True, var="EtCutDatavsBX",
		task="TP", hasher="TTSubdet"),
	Group("50 TP Et Data vs BX(LS)", True, var="EtCutDatavsLS",
		task="TP", hasher="TTSubdet"),
	Group("51 TP Et Emul vs BX(LS)", True, var="EtCutEmulvsBX",
		task="TP", hasher="TTSubdet"),
	Group("51 TP Et Emul vs BX(LS)", True, var="EtCutEmulvsLS",
		task="TP", hasher="TTSubdet"),

#
#	DIGI(TP) Comparison of VME vs uTCA
#
	Group("52 DIGI VME vs uTCA ADC", True, var="ADC", hasher="Subdet",
		task="DIGI_VMEvsuTCA"),
	Group("53 DIGI VME vs uTCA ADC(uTCA) Missing VME", True, var="ADCMsnVME",
		hasher="Subdet", task="DIGI_VMEvsuTCA"),
	Group("54 DIGI VME vs uTCA ADC(VME) Missing uTCA", True, var="ADCMsnuTCA",
		hasher="Subdet", task="DIGI_VMEvsuTCA"),
	Group("55 DIGI VME vs uTCA Mismatched", True, var="Mismatched",
		hasher="depth", task="DIGI_VMEvsuTCA"),
	Group("56 DIGI VME vs uTCA Missing", True, var="Missing_VME",
		hasher="depth",  task="DIGI_VMEvsuTCA"),
	Group("56 DIGI VME vs uTCA Missing", True, var="Missing_uTCA",
		hasher="depth",  task="DIGI_VMEvsuTCA"),

	Group("57 TP VME vs uTCA Et", True, var="Et",
		task="TP_VMEvsuTCA"),
	Group("58 TP VME vs uTCA Et Mismatched", True, var="EtMsm", task="TP_VMEvsuTCA", hasher="NOHASHER"),
	Group("59 TP VME vs uTCA FG Mismatched", True, var="FGMsm", task="TP_VMEvsuTCA", hasher="NOHASHER"),
	Group("60 TP VME vs uTCA Missing", True, var="Missing", task="TP_VMEvsuTCA",
		hasher="NOHASHER"),

	#
	#	QIE10
	#
	Group("61 QIE10 ADC", True, var="ADC",
		task="QIE10", hasher="NOHASHER"),
	Group("62 QIE10 LETDC", True, var="LETDC",
		task="QIE10", hasher="NOHASHER"),
	Group("63 QIE10 LETDC vs ADC", True, var="LETDCvsADC",
		task="QIE10", hasher="NOHASHER"),
	Group("64 QIE10 TETDC vs ADC", True, var="TETDCvsADC",
		task="QIE10", hasher="NOHASHER"),

]

#
#	Calibration Stream Groups 
#
calibgroups = [
	Group("00 Run Summary", False, var="SummaryvsLS", hasher="NOHASHER"),

	Group("01 Pedestal Mean vs CondDB", False, var="MeanDBRef", hasher="Subdet",
		task="PEDESTAL"),
	
	Group("02 Pedestal Mean vs CondDB", False, var="MeanDBRef", hasher="depth",
		task="PEDESTAL"),
	
	Group("03 Pedestal RMS vs CondDB", False, var="RMSDBRef", hasher="Subdet",
		task="PEDESTAL"),
	
	Group("04 Pedestal RMS vs CondDB", False, var="RMSDBRef", hasher="depth",
		task="PEDESTAL"),

	Group("05 Pedestal Missing vs LS", False, var="MissingvsLS", hasher="Subdet",
		task="PEDESTAL"),

	Group("06 Pedestal Occupancy vs LS", True, var="OccupancyvsLS", hasher="Subdet",
		task="PEDESTAL"),
	
	Group("07 Pedestal #Bad Mean Chs vs LS", True, var="NBadMeanvsLS", 
		hasher="Subdet", task="PEDESTAL"),
	
	Group("08 Pedestal #Bad RMS Chs vs LS", True, var="NBadRMSvsLS", 
		hasher="Subdet", task="PEDESTAL"),
	Group("09 Pedestal Occupancy EA vs LS ", True, var="OccupancyEAvsLS",
		hasher='Subdet', task="PEDESTAL"),

	Group("10 RAW BadQuality vs BX (LS)", True, var="BadQualityvsBX",
		hasher="NOHASHER", task="RAW"),
	Group("10 RAW BadQuality vs BX (LS)", True, var="BadQualityvsLS",
		hasher="NOHASHER", task="RAW"),

	Group("11 RAW Bcn(Evn) Mismatches", True, var="BcnMsm", hasher="Electronics",
		task="RAW"),
	Group("11 RAW Bcn(Evn) Mismatches", True, var="EvnMsm", hasher="Electronics",
		task="RAW"),
]

allgroups = {"physics" : physgroups, "calibration" : calibgroups}

if __name__=="__main__":
	print analysis_tasks
	print variables
	print physgroups
	print calibgroups
