#!/usr/bin/python

#
#	ROOT DQM File Parser Class
#	Returns 
#

import sys, os, glob
import ROOT as R

#	to import utilities module
pathToUtilities = os.environ["HCALDQMTOOLBOX"]
sys.path.append(pathToUtilities)
import utilities.re_functions as res
import utilities.shell_functions as shell
import logging

#	define the Parser class
class Parser:
	"""
        Parser Class. Parses all the TH1 derivables and returns a dictionary
        where:
        - keys represent the full path to the object as it appears in the ROOT 
        - values represent the TObject
	"""
	def __init__(self, pathfile, isDQMFormat=True, convention="Online", 
            subsystem="Hcal"):
		"""
		Get the Run Number. Open the file and cd to the Run Summary Directory
		Initialize whatever is needed
		"""
                logging.debug("Parsing the file")                
                path, filename = shell.split(pathfile)
                if isDQMFormat:
                    tokens = res.match_filename(filename=filename, convention=convention)
        	    self.__rootFileName = pathfile
    		    self.__runNumber = tokens["run"]
		    self.__rootFile = R.TFile(self.__rootFileName, "r")
		    self.__rsDir = self.__rootFile.GetDirectory(
		        "DQMData/Run %d/%s/Run summary/" % (self.__runNumber, 
                        tokens["subsystem"] if convention=="Online" else subsystem))
                else:
                    self.__rootFileName = pathfile
                    self.__rootFile = R.TFile(self.__rootFileName, "r")
                    self.__rsDir = R.gDirectory
	
	def traverse(self):
		"""
		Traverse the ROOT Folder Tree
		"""

		#	get into the Run Summary Directory
		#	each Task Folder is sitting there
		objDict = {}
		for dirKey in self.__rsDir.GetListOfKeys():
			dirName = dirKey.GetName()
			#	launch the traversing of each task directory
			self.traverseDir(self.__rsDir.GetDirectory(dirName), objDict)
		
		return objDict

	def traverseDir(self, cDir, objDict, topPath=""):
		"""
		TopPath - path to the current Directory not including it
		"""
		for key in cDir.GetListOfKeys():
			obj = key.ReadObj()
			#	if it is a folder, traverse recursively
			if obj.InheritsFrom("TDirectoryFile"):
				self.traverseDir(obj, objDict, 
					topPath=topPath+"/"+cDir.GetName())
			else:
				path = topPath+"/"+cDir.GetName()
				if path in objDict.keys():
					objDict[path][len(objDict[path]):] = [obj]
				else:
					objDict[path] = [obj]

if __name__=="__main__":
	print "Hello"
	fileName = "/Users/vk/software/HCALDQM/tmp/DQM_V0001_R000165121__Global__CMSSW_X_Y_Z__RECO.root"
	parser = Parser(pathfile=fileName, convention="Offline")
	d = parser.traverse()
	print d

