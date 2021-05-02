import urllib2
import subprocess
import xbmcgui
import os

class AddonGithubUpdater:
	def __init__(self, addonFolderName, githubOrg, githubRepo):
		self.githubOrg=githubOrg
		self.githubRepo=githubRepo
		self.addonParentFolder=os.path.split(addonFolderName)[0]
		self.addonFolderName=os.path.split(addonFolderName)[1]
		self.addonFullPath=addonFolderName

	
	def isUpdateAvailable(self):
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('Updater..', 'Please wait... Checking for updates...')		
		f=open(self.addonFullPath+"/changelog.txt")
		local=f.readlines()[-1]
		f.close()
		try:
			remote=urllib2.urlopen("https://raw.githubusercontent.com/"+self.githubOrg+"/"+self.githubRepo+"/main/changelog.txt").readlines()[-1]
		except Exception as e:
			pDialog.close()
			return False
		pDialog.close()
		if remote!=local:
			#xbmcgui.Dialog().ok("Lightymon", "New version found!", "Remote: " + remote, "Local: " + local)
			return True
		else:
			#xbmcgui.Dialog().ok("Lightymon", "No new version found!", "Remote: " + remote, "Local: " + local)
			return False
		#return local!=remote
		
	def installUpdate(self):
		download_path=os.path.expanduser("~/update_plugin_webservice.zip")
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('Updater..', 'Please wait... Installing update...')
		f=open(download_path,"w")
		f.write(urllib2.urlopen("https://github.com/"+self.githubOrg+"/"+self.githubRepo+"/archive/main.zip").read())
		f.close()
		subprocess.call(["unzip","-o",download_path,"-d",self.addonParentFolder])
		#Debug
		#xbmcgui.Dialog().ok("Lightymon", self.addonParentFolder)
		pDialog.close()