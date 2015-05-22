import fnmatch
import os
def r_file(input):
	f = open(input, 'r')
	
	type_strs = {}
	drt_flag = 0
	for line in f.readlines():
		if line.lstrip()[:6] == '------':
			drt_flag = 1
			continue
		
		if drt_flag==1 and line.lstrip()[:6]=='-------':
			drt_flag = 0
			continue
	
		if drt_flag == 1:
			continue
			
		try:
			strs = line.split()
			t = strs[7]
			if t not in type_strs.keys():
				type_strs[t] = line
		except Exception,e:
			print 'file %s' % input, line
			print e
			print '---------------'
	
	f.close()
	#print type_strs
	return type_strs

def r_files(files):
	type_strs = {}
	for infile in files:
		nts = r_file(infile)
		#type_strs = list(set(type_strs).union(set(nts)))
		type_strs.update(nts)
	return type_strs

if __name__=='__main__':
	#files = ['mbschd.log.lsf0']
	files = []
	fdir = '../errorlog'
	for f in os.listdir(fdir):
		if fnmatch.fnmatch(f, 'sbatchd.log.*'):
			files.append(fdir+'/'+f)
	print len(files), 'files'
	#for i in range(10,20):
	#	files.append('lim.log.c02b'+str(i))	
	res = r_files(files[:10])
	print len(res)
	for t in res.keys():
		print t
	for l in res.values():
		print l.rstrip()
