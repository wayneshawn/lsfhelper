import formatter
import dbinserter
import fnmatch
import os
import traceback
import time

etype_to_num = {'"JOB_NEW"':0, '"JOB_START"':1, '"JOB_START_ACCEPT"':2, '"JOB_EXECUTE"':3,
'"JOB_STATUS"':4, '"JOB_MOVE"':5, '"JOB_SIGNAL"':6, '"JOB_CLEAN"':7, '"JOB_FINISH"':8}

def r_events_file(infile, fmt, db): 
	f = open(infile, 'r')
	print infile
	dict_type_num = {}
	for line in f.readlines():
		event_type = line.split(' ', 1)[0]
		if event_type == '"JOB_NEW"':
			#continue
			strs = fmt.split(0, line)
		elif event_type == '"JOB_START"':
			#continue
			strs = fmt.split(1, line)
		elif event_type == '"JOB_START_ACCEPT"':
			#continue
			strs = fmt.split(2, line)
		elif event_type == '"JOB_EXECUTE"':
			#continue
			strs = fmt.split(3, line)
		elif event_type == '"JOB_STATUS"':
			#continue
			strs = fmt.split(4, line)
		elif event_type == '"JOB_MOVE"':
			#continue
			strs = fmt.split(5, line)
		elif event_type == '"JOB_SIGNAL"':
			#continue
			strs = fmt.split(6, line)
		elif event_type == '"JOB_CLEAN"':
			#continue
			strs = fmt.split(7, line)
		elif event_type == '"JOB_FINISH"':
			#continue
			strs = fmt.split(8, line)
		else:
			continue

		if strs == None:
			print line
			exit(0)

		try:
			db.batch_add(etype_to_num[event_type], strs)
		except Exception, e:
			traceback.print_exc()  
			print event_type, strs
			print line
			exit(1)

		if event_type not in dict_type_num.keys():
			dict_type_num[event_type] = 0
		dict_type_num[event_type] += 1

	return dict_type_num

def r_events_files(infiles):
	fmt = formatter.formatter()
	db = dbinserter.inserter()

	tt_dict_type_num = {}

	for f in infiles:
		d_t_n = r_events_file(f, fmt, db)
		for etype, num in d_t_n.items():
			#print etype, num
			if etype not in tt_dict_type_num.keys():
				tt_dict_type_num[etype] = 0
			tt_dict_type_num[etype] += num

	db.close()

	return tt_dict_type_num


if __name__ == '__main__':
	files = []
	'''
	fdir = './logsample/logdir'
	for f in os.listdir(fdir):
	if fnmatch.fnmatch(f, 'lsb.events.*'):
	files.append(fdir+'/'+f)
	'''
	#for i in range(1,10):
	#	files.append('./logdir/lsb.events.'+str(i))
	files.append('./logdir/lsb.acct')

	t1 = time.time()

	tt_type_num = r_events_files(files)

	t2 = time.time()
	print (t2-t1)

	tt_num = 0
	for etype, num in tt_type_num.items():
		print etype, num
		tt_num += num
	print 'fmt lines ', tt_num
