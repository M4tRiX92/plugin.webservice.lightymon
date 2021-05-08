import xbmc
import os
import sys
import xbmcaddon
import xbmcgui
import time
import subprocess
import urllib2
from flask import Flask, request, render_template

app = Flask(__name__)
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path'))
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )


import AddonGithubUpdater

try:
    updater=AddonGithubUpdater.AddonGithubUpdater(addon_dir,"M4tRiX92","plugin.webservice.lightymon")
    if updater.isUpdateAvailable():
        #if xbmcgui.Dialog().yesno(addonname, "Plugin update is available. Do you want to install new version?"):
        updater.installUpdate()
            #xbmcgui.Dialog().ok(addonname, "Update installed. Please restart plugin")
        sys.exit()
except Exception as e:
       xbmcgui.Dialog().ok(addonname, repr(e),"Please report an error at github issue list")
   # xbmcgui.Dialog().ok(addonname, "Failed to check the update. Maybe your Pi is not connected to the Internet")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setleds')
def my_form():
    return render_template('setleds.html')

@app.route('/setleds', methods=['GET', 'POST'])
def my_form_post():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        ledv = request.form['ledv']
        ledh = request.form['ledh']
        direction = request.form['direction']
        device = request.form['device']
        center_corner = request.form['center_corner']
        processed_text = "ledv " + ledv + " - ledh " + ledh + " - direction " + direction + " - device " + device + " - center_corner " + center_corner
        #setEverything(ledh, ledv, options)
        return processed_text

    # show the form, it wasn't submitted
    return render_template('setleds.html')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)