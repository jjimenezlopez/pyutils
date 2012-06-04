#!/usr/bin/env python                                                                                                                                                    
from subprocess import Popen, PIPE
from sys import argv
import os
import re

__autor__ = "Jose Jiménez"
__email__ = "jjimenezlopez@gmail.com"
__date__ = "2012/05/03"

if len(argv) == 1 or len(argv) > 2:
    print 'Wrong execution format.'
    print 'Correct format: renamesrt /path/to/the/files'
    exit(0)

path = argv[1]
if not path.endswith('/'):
    path = path + '/'


# Get the SRT files list
path = path.replace(' ', '\ ')
proc = Popen('ls ' + path + '*.srt', stdout=PIPE, stderr=PIPE, shell=True)
result = proc.communicate()

if proc.returncode == 2:
    print 'SRT files not found in path \'' + path + '\''

srt_list = result[0].splitlines()

# Get the MKV files list
ls_command = 'ls ' + path + '*.mkv ' + path + '*.avi ' + path + '*.mp4'
proc = Popen(ls_command, stdout=PIPE, stderr=PIPE, shell=True)
result = proc.communicate()

if proc.returncode == 2:
    print 'MKV files not found in path \'' + path + '\''

mkv_list = result[0].splitlines()

for v in mkv_list:
    videoname = os.path.basename(v)
    info_found = False
    if re.search('[0-9]x[0-9][0-9]', videoname):
        season = re.findall('[0-9]x[0-9][0-9]', videoname)[0].strip().split('x')[0]
        chapter = re.findall('[0-9]x[0-9][0-9]', videoname)[0].strip().split('x')[1]
        info_found = True
    
    if re.search('[Ss][0-9][0-9][Ee][0-9][0-9]', videoname):
        season = re.findall('[Ss][0-9][0-9][Ee][0-9][0-9]', videoname)[0].strip().split('E')[0].replace('S','')
        if 'e' in season: # in case s02e01 for example
            season = re.findall('[Ss][0-9][0-9][Ee][0-9][0-9]', videoname)[0].strip().split('e')[0].replace('s','')

        try:
            chapter = re.findall('[Ss][0-9][0-9][Ee][0-9][0-9]', videoname)[0].strip().split('E')[1]
        except IndexError:
            chapter = re.findall('[Ss][0-9][0-9][Ee][0-9][0-9]', videoname)[0].strip().split('e')[1]

        info_found = True

    if info_found:
        found = False
        for s in srt_list:
            srtname = os.path.basename(s)
            cad0 = '[Ss]%s[Ee]%s' % (season, chapter)
            cad1 = '[Ss]0%s[Ee]%s' % (season, chapter)
            cad2 = '%sx%s' % (season, chapter)
            cad3 = '%sx%s' % (season.replace('0', ''), chapter)
            if re.search(cad0, srtname) or re.search(cad1, srtname) or re.search(cad2, srtname) or re.search(cad3, srtname):
		if '.mkv' in v:
	            videoname_dot_srt = v.replace('.mkv', '.es.srt')
		elif '.avi' in v:
                    videoname_dot_srt = v.replace('.avi', '.es.srt')
                elif '.mp4' in v:
                    videoname_dot_srt = v.replace('.mp4', '.es.srt') 	

                if s != videoname_dot_srt:
                    if '\'' in s:
                        new_s = s.replace('\'', '')
                        proc = Popen('mv \"' + s + '\" \'' + new_s + '\'', stdout=PIPE, shell=True)
                        proc.wait()
                        s = new_s 

                    proc = Popen('mv \'' + s + '\' \'' + videoname_dot_srt + '\'', stdout=PIPE, shell=True)
                    proc.wait()
                    print '[R] SRT found for ' + videoname + ' and renamed.'
                else:
                    print '[F] SRT found for ' + videoname
                found = True

        if not found:
            print '[N] SRT file NOT found for ' + videoname
 
