import fnmatch
import os
import re
from mytime import to_time_stamp
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra.policies import *
import traceback
import time
from dbinserter

'''
Logs:
mbatchd.log
mbschd.log
sbatchd.log
res.log

columns:
CREATE TABLE daemonerrlog{
	log_type text,
	host_name text,
	log_time bigint,
	field4 int,
	field5 int,
	msg text,
PRIMARY KEY(host_name, log_time)
}

args:
@strs
	['Mar', '14', '22:52:22', '2015', '6024', '3', 'doProbeReply: Exception bit of <63> is set for host <c37b10>']+[log_type, host_name]
@session
	database session
'''
def insert_err_log(strs, session):
	#print strs
	#log_type = strs[7]
	#host_name = strs[8]
	#print strs[:4]
	log_time = to_time_stamp(strs[:4])	
	field4 = eval(strs[4])
	field5 = eval(strs[5])
	#msg = strs[6]
	try:	
		session.execute('INSERT INTO daemonerrlog(log_type, host_name, log_time, field4, field5, msg) VALUES(%s, %s, %s, %s, %s, %s)', (strs[7], strs[8], log_time, field4, field5, strs[6]))

		#for debug
		#r = session.execute('select count(*) from daemonerrlog')
		#print	r 
	except Exception, e:
		print strs
		print e
		print traceback.format_exc()
		print '\n'

#@input
#	<log_type>.log.<hostname>
def r_file(input, session):
	#log_type, none, host_name = tuple(input.split('.'))	
	t_and_h = input.split('.')[::2]
	p = re.compile(r'(\w+)\s+(\d+)\s([\d:]+)\s(\d+)\s(\d+)\s(\d+)\s8.0\s(.*)')
	f = open(input, 'r')
	cnt = 0
	for line in f.readlines():
		m = p.match(line)
		if m:
			strs = list(m.groups())	
			cnt += 1
			#insert_err_log(strs + t_and_h, session)
		else:
			continue
			strs = line.split()
			if len(strs)>6 and strs[5] == 'Last':
				continue
			elif strs[0]=='Note:' or line[:6]==' -----':
				continue
			#print input, cnt, line
		#print strs
		#if cnt<100:
		#	print cnt
	f.close()
	print input, cnt
	return cnt

def r_files(files, session):
	rdnum = 0
	for f in files:
		rdnum += r_file(f, session)
	print rdnum
def	get_type_files(fdir, ftype): 
	files = []
	for f in os.listdir(fdir):
		if fnmatch.fnmatch(f, ftype):
			files.append(f)
	return files

if __name__=='__main__':
	cluster = Cluster(load_balancing_policy=RoundRobinPolicy())
	session = cluster.connect()
	session.set_keyspace('lsflog2')

	t1 = time.time()
	res_logs = get_type_files('./', 'res.log.*')
	r_files(res_logs[:10], session)
	print time.time()-t1

	'''
	t1 = time.time()
	mbd_logs = get_type_files('./', 'mbatchd.log.*')
	r_files(mbd_logs, session)
	print time.time()-t1

	t1 = time.time()
	mbschd_logs = get_type_files('./', 'mbschd.log.*')
	r_files(mbschd_logs, session)
	print time.time()-t1
	

	sbd_logs = get_type_files('./', 'sbatchd.log.*')
	r_files(sbd_logs, session)
	'''
