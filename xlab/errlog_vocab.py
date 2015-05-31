import os
import fnmatch

fdir = '../../daemon_errlog'

ftypes = ['res.log.*', 'sbatchd.log.*', 'mbatchd.log.*']

files = []
for f in os.listdir(fdir):
   for ftype in ftypes:
    if fnmatch.fnmatch(f, ftype):
	files.append(fdir+'/'+f)

print len(files)
