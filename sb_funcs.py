# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import subprocess

#get a fortune cookie... the function assumes you have the comand fortune installed.
#TODO: change the hardcoded fortune path to a variable
def getFortuneCookie ( debugflg = False, max_len = 270 ):
    for tries in range(5):
        fortune = subprocess.check_output(["/usr/games/fortune", "-s"]).decode() + " #fortune"
        if( len(fortune) < max_len ):
            break
        else:
            fortune = ''
    return fortune


# temp func... will add mode features later as I get more ideas...
def getSysInfo( debugflg = False, max_len = 270 ):
    #Get uptime info
    output = (subprocess.check_output(["uptime"])).decode()
    uptime = output.split(',')[0].split('up')[1]
    loadavg = output.split('load average')[1].split()
    uptime_loadavg = 'Uptime: %s; Load average: %s, %s, %s' % (uptime, loadavg[-3].strip(","),loadavg[-2].strip(","),loadavg[-1].strip(",") )
    #Get available memory info
    output = (subprocess.check_output(["free", "-h"])).decode().split()
    availablemem = 'Available memory: %s' % (output[12])
    #Concatenate the output
    sysinfo_text = 'Some non-sense info: \n[%s] \n[%s]\n' % (uptime_loadavg, availablemem)
    if( len(sysinfo_text) > max_len ):
        sysinfo_text = sysinfo_text[0:max_len]

    return sysinfo_text

    
# === END === 
