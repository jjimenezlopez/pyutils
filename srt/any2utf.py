#!/usr/bin/env python
from subprocess import Popen, PIPE
from sys import argv

__autor__ = "Jose Jiménez"
__email__ = "jjimenezlopez@gmail.com"
__date__ = "2012/05/03"

if len(argv) == 1 or len(argv) > 2:
    print 'Wrong execution format.'
    print 'Correct format: any2utf /path/to/the/files'
    exit(0)

path = argv[1]
if not path.endswith('/'):
    path = path + '/'

path = path.replace(' ', '\ ')
proc = Popen('ls ' + path + '*.srt', stdout=PIPE, stderr=PIPE, shell=True)
result = proc.communicate()

if proc.returncode == 2:
    print 'SRT files not found in path \'' + path + '\''

list = result[0].splitlines()

for f in list:
    aux_f = f
    aux_f.replace(' ', '\ ')
     
    # file --mime /path/to/file.srt
    #print 'file --mime \"' + aux_f + '\"' 
    proc = Popen('file --mime \"' + aux_f + '\"', stdout=PIPE, shell=True)
    result = proc.communicate()[0]
    charset = result.split('charset=')[1]
    charset = charset.replace('\n', '')
    if charset == 'unknown-8bit':
        charset = 'iso-8859-15'

    if charset != 'utf-8' and charset != 'binary':
        # print 'iconv -f ' + charset + ' -t utf-8 ' + aux_f + ' > ' + aux_f + '.utf' 
        proc = Popen('iconv -f ' + charset + ' -t utf-8 \"' + aux_f + '\" > \"' + aux_f + '.utf\"', stdout=PIPE, shell=True)
        result = proc.communicate()[0]
        if proc.returncode == 0:
            #proc = Popen('rm ' + aux_f, stdout=PIPE, shell=True)
            proc = Popen('mv \"' + aux_f + '.utf\"  \"' + aux_f + '\"', stdout=PIPE, shell=True)
            proc.wait()
            proc = Popen('file --mime \"' + aux_f + '\"', stdout=PIPE, shell=True)
            text = proc.communicate()[0]
            print f.split('/')[-1] + ' | ' + charset + ' --> ' + text.split('charset=')[1].replace('\n', '')
        else:
            proc = Popen('file --mime \"' + aux_f + '\"', stdout=PIPE, shell=True)
            text = proc.communicate()[0]
            print f + ' --> conversion ERROR: ' + text.split('charset=')[1].replace('\n', '')

