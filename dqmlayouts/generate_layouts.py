#!/usr/bin/python

import sys,os, re, glob
pathToUtilities = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToUtilities)

from rootio.parser import Parser
from layout import *
import logging

import utilities.shell_functions as shell
import utilities.re_functions as res
from monitorables import allgroups, analysis_tasks, variables 

#   skip list - whatever you would like to skip
skip_list = [("DigiTask", "Occupancy", "depth"), ("RawTask", "BadQuality", "depth"),
    ("RawTask", "BcnMsm", "Electronics"),
    ("RawTask", "OrnMsm", "Electronics"),
    ("RawTask", "EvnMsm", "Electronics")]

def relink(subsystem, layoutbase, objs, out, agroups, detail):
        logging.debug("Starting the Relinking and Grouping")
	for path in objs.keys():
		logging.debug(subsystem+path)
		d = res.match_path(path)
		task = d["module"]
		if task not in analysis_tasks.keys() or d["variable"]==None<2:
			#	if not one of my tasks or if it's a xml object
			continue

		module = analysis_tasks[task]
		var = d["variable"]
		if var not in variables[module].keys():
			#	if this variable is not in the list of monitorables
			#	for this task continue
			logging.debug("Missing Monitorable for path %s" % path)
			continue

                #   apply skip list
                qqq = False
                for sk in skip_list:
                    if task==sk[0] and var==sk[1] and d["hasher"]==sk[2]:
                        qqq = True
                        break
                if qqq: continue

		#	first relink all the MEs
                logging.debug("Relinking")
		if d["variable"]!=None and d["hasher"]=="NOHASHER":
			#	if it's a single ME
			for i in range(len(objs[path])):
				name = objs[path][i].GetName()
				p = Plot(subsystem+path+"/%s" % name,
					variables[module][var])
				newpath = "%s/%s" % (var, module)
				l = Layout(newpath, layoutbase, [[p]])
				if detail:out.write("\n%s\n" % l)

				#	grouping
				for g in agroups:
					info = {"task" : module,
							"var" : var, "hasher" : "NOHASHER"}
					nskipped=0; nms = 0;
					"""
					grouping is based on 2 things:
					1 - variable name
					2 - task name
					"""
					for key in g.tokens.keys():
						if g.tokens[key]==0:
							nskipped+=1
						elif g.tokens[key]==info[key]:
							nms+=1
					if nms+nskipped==len(g.tokens.keys()):
						g.add(p)
		else:
			hasher = d["hasher"]
			for o in objs[path]:
				p = Plot(subsystem+path+"/%s" % o.GetName(),
					variables[module][var])
				newpath = "%s/%s/%s/%s" % (
					var, module, hasher, o.GetName())
				l = Layout(newpath, layoutbase, [[p]])
				if detail:out.write("\n%s\n" % l)

				#	grouping
				for g in agroups:
					info = {"task" : module,
						"var" : var, "hasher" : hasher}
					nskipped=0; nms = 0;
					"""
					grouping is based on 2 things:
					1 - variable name
					2 - task name
					3 - hasher
					"""
					for key in g.tokens.keys():
						if g.tokens[key]==0:
							nskipped+=1
						elif g.tokens[key]==info[key]:
							nms+=1
					if nms+nskipped==len(g.tokens.keys()):
						g.add(p)


def group(layoutbase, out, detail, groups):
        logging.debug("### Generating Groups!")
	skipList = []
	for g in groups:
		#	this is for uniting groups or skipping the empty groups
		if g in skipList or g.empty():
			continue
		for g2 in groups:
			if g2 is not g and g.name==g2.name:
				g.l.extend(g2.l)
				skipList.append(g2)
		#	create a layout out of a group...
		if not g.include(detail): continue
		l = Layout(g.name, layoutbase, g.dump())
		logging.debug(g.name)
		out.write("\n%s\n" % l)

def main():
	logging.debug("Starting Layout Generation...")

        #
        #   Set up some variable strings......
        #   Set up soem settings
        #
	filelist = [
            "/Users/vk/software/HCALDQM/tmp/DQM_V0001_R000281613__StreamExpress__Run2016H-Express-v2__DQMIO.root"]
	outname = "/Users/vk/software/HCALDQM/tmp/hcal_T0_layouts.py"
	physcalib = "physics"
	detail = 1
	layoutbase = "hcallayout"
        convention = "Offline"
	out = open(outname, "w")
	out.write(
"""if __name__=="__main__":
	class DQMItem:
		def __init__(self,layout):
			print layout
	dqmitems={}""")
	out.write("\n\n")
	users = "Hcal"
	if detail==0:
		users="00 Shift"
		if physcalib=="calibration":
			mainsubsystem = "HcalCalib"
		else:
			mainsubsystem = "Hcal"
	elif physcalib=="calibration":
		users="HcalCalib"
		mainsubsystem = "Layouts"
	else:
		users="Hcal"
		mainsubsystem="Layouts"
	out.write("def %s(i, p, *rows): i['%s/%s/' + p] = DQMItem(layout=rows)\n\n" % (layoutbase, users, mainsubsystem))

        #
        #   Parse all the histgorams
        #   Group them for layouts
        #   Create sym links to individual histos as well
        #
	objs = {}
	for f in filelist:
		path, filename = shell.split(f)
                if convention=="Online":
		    subsystem = match_filename(filename, convention).groups()[1]
		    subsystem = subsystem[1:len(subsystem)]
                else:
                    subsystem = "Hcal"
		logging.debug("Will parse ROOT file: %s, subsystem %s" % (filename, subsystem))
		parser = Parser(pathfile=f, subsystem=subsystem, convention=convention)
		os = parser.traverse()
		relink(subsystem, layoutbase, os, out, allgroups[physcalib],detail)
		objs.update(os)
	group(layoutbase, out, detail, allgroups[physcalib])

	# close the output file
	out.close()

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
