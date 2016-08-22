#!/usr/bin/python

#
#	ROOT DQM File Parser Class
#	Returns 
#

import sys, os
import ROOT as R

#	to import utilities module
pathToUtilities = os.environ["HCALDQMUTILITIES"]
sys.path.append(pathToUtilities)
import Utils.Shell as Shell
import Utils.IO as IO
import Utils.RE as RE

#	define the Parser class
class Parser:
	"""
        Parser Class. Parses all the TH1 derivables and returns a dictionary
        where:
        - keys represent the full path to the object as it appears in the ROOT 
        - values represent the TObject
	"""
	def __init__(self, pathfile, isDQMFormat=True):
		"""
		Get the Run Number. Open the file and cd to the Run Summary Directory
		Initialize whatever is needed
		"""
                
                path, filename = Shell.split(pathfile)
                if isDQMFormat:
                    tokens = RE.match_filename(filename)
        	    self.__rootFileName = pathfile
    		    self.__runNumber = tokens["run"]
		    self.__rootFile = R.TFile(self.__rootFileName, "r")
		    self.__rsDir = self.__rootFile.GetDirectory(
		        "DQMData/Run %d/%s/Run summary/" % (self.__runNumber, 
                        tokens["subsystem"]))
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
	fileName = "/Users/vk/research/tmptmp/DQM_V0001_Hcal_R000262548.root"
	parser = Parser(fileName)
	d = parser.traverse()
	print d

