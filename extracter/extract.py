import fnmatch
import os
import re
import traceback
import time

re_patterns = []

#@input
#	<log_type>.log.<hostname>
def r_file(input):
	#log_type, none, host_name = tuple(input.split('.'))	
	t_and_h = input.split('.')[::2]
	p = re.compile(r'(\w+)\s+(\d+)\s([\d:]+)\s(\d+)\s(\d+)\s(\d+)\s8.0\s(.*)')
	f = open(input, 'r')
	
	#keyword and num
	kwd_num = {}
	for line in f.readlines():
		m = p.match(line)
		if m:
			strs = list(m.groups())	
			msg = strs[6]
			kwd = msg.split(' ',1)[0]
			if kwd not in kwd_num.keys():
				kwd_num[kwd] = 0
			kwd_num[kwd] += 1
	
			if kwd == 'lsbatchDir():':
				continue
				p_msg = re.compile(r'lsbatchDir\(\): neither <home>/.lsbatch nor spool dir could be used by the job <(\d+)(?:\[(\d+)\])?>, temp dir will be used')
				m_msg = p_msg.match(msg)
				if m_msg:
					pass
					#print 'job<%d[%s]>' % (int(m_msg.groups()[0]), m_msg.groups()[1])
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'postJobSetup:':
				continue
				p_msg = re.compile(r'postJobSetup: Job <(\d+)> failed in initPaths\(\), No such file or directory.')
				m_msg = p_msg.match(msg)
				if m_msg:
					pass
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'Has':
				continue
				p_msg = re.compile(r'Has error to remove buffer file for job<(\d+)>')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'tryStop:':
				continue
				#p_msg = re.compile(r'')
				p_msg = re.compile(r'tryStop: Job <(\d+)> failed in ls_loadofhosts\(\). Communication time out.')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'acctMapTo:':
				continue
				#p_msg = re.compile(r'')
				#acctMapTo: No valid user name found for job <1221914>, userName <2012437>. getpwnam() failed:Success
				p_msg = re.compile(r'acctMapTo: No valid user name found for job <(\d+)>, userName <(\d+)>. getpwnam\(\) failed:Success')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>, username<%d>' % (int(m_msg.groups()[0]), int(m_msg.groups()[1])), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'do_lsbMsg:':
				continue
				#do_lsbMsg: JobId <46867> not found
				p_msg = re.compile(r'do_lsbMsg: JobId <(\d+)> not found')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'status_job:':
				continue
				#status_job: Job <4395238> is forgotten by mbatchd on host <lsf0>, ignored.
				p_msg = re.compile(r'status_job: Job <(\d+)> is forgotten by mbatchd on host <lsf0>, ignored.')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'do_sigjob:':
				continue
				#do_sigjob: Sending jobReply (len=52) to master failed for job <4431621>: Broken pipe
				p_msg = re.compile(r'do_sigjob: Sending jobReply \(len=52\) to master failed for job <(\d+)>: Broken pipe')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
				else:
					print 'msg unmatch'
					print msg
					exit(1)
			elif kwd == 'mykillpg:':
				continue
				#mykillpg: Job <30223> failed in getJInfo_(). Failed in sending/receiving a message: No such process. or job has been killed
				#p_msg = re.compile(r'')
				p_msg = re.compile(r'mykillpg: Job <(\d+)(?:\[(\d+)\])?> failed in getJInfo_\(\). Failed in sending/receiving a message: No such process. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). A connect sys call failed: Connection refused. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). A socket operation has failed: No such process. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). Failed in sending/receiving a message: No such file or directory. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). File operation failed: unknown system error 0. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				#p_msg = re.compile(r'')
				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). File operation failed: No such process. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). A connect sys call failed: No such process. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print m_msg.groups()
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). A connect sys call failed: Interrupted system call. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				#p_msg = re.compile(r'')
				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). End of file. or job has been killed')
				m_msg = p_msg.match(msg)
				if m_msg:
					print 'job<%d>' % int(m_msg.groups()[0]), line
					continue

				#---------------------------------------
				#p_msg = re.compile(r'')
				p_msg = re.compile(r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). (.*)')
				m_msg = p_msg.match(msg)
				if m_msg:
					reg = r'mykillpg: Job <(\d+)> failed in getJInfo_\(\). '+m_msg.groups()[1]
					if reg not in re_patterns:
						print 'got new regex', reg
						re_patterns.append(reg)
						time.sleep(2)
					p_msg = re.compile(reg)
					m_msg = p_msg.match(msg)
					if m_msg:
						print 'job<%d>' % int(m_msg.groups()[0]), line
						continue
				#resutl:
				#1 mykillpg: Job <(\d+)> failed in getJInfo_\(\). Failed in sending/receiving a message: unknown system error 0. or job has been killed
				#2 mykillpg: Job <(\d+)> failed in getJInfo_\(\). A connect sys call failed: No such file or directory. or job has been killed
				#3 mykillpg: Job <(\d+)> failed in getJInfo_\(\). A connect sys call failed: unknown system error 0. or job has been killed
				#4 mykillpg: Job <(\d+)> failed in getJInfo_\(\). Communication time out. or job has been killed
				#5 mykillpg: Job <(\d+)> failed in getJInfo_\(\). Failed in sending/receiving a message: Connection reset by peer. or job has been killed
				#6 mykillpg: Job <(\d+)> failed in getJInfo_\(\). A socket operation has failed: No such file or directory. or job has been killed
				#7 mykillpg: Job <(\d+)> failed in getJInfo_\(\). Failed in sending/receiving a message: Interrupted system call. or job has been killed
				#8 mykillpg: Job <(\d+)> failed in getJInfo_\(\). Internal library error. or job has been killed
				#---------------------------------------

				print 'msg unmatch'
				print msg
				exit(1)

		else:
			strs = line.split()
			if len(strs)>6 and strs[5] == 'Last':
				continue
			elif strs[0]=='Note:' or line[:6]==' -----':
				continue
			print line
			exit(1)

	f.close()
	return kwd_num

def r_files(files):
	tt_kwd_num = {}
	for f in files:
		kwd_num = r_file(f)
		for kwd, num in kwd_num.items():
			if kwd not in tt_kwd_num.keys():
				tt_kwd_num[kwd] = 0
			tt_kwd_num[kwd] += num
	
	tt_num = 0
	for kwd, num in tt_kwd_num.items():
		print kwd, num
		tt_num += num
	print 'total %d records' % tt_num

def	get_type_files(fdir, ftype): 
	files = []
	for f in os.listdir(fdir):
		if fnmatch.fnmatch(f, ftype):
			files.append(fdir+'/'+f)
	return files

if __name__=='__main__':
	#cluster = Cluster(load_balancing_policy=RoundRobinPolicy())

	t1 = time.time()
	res_logs = get_type_files('../errorlog', 'sbatchd.log.*')
	print '%d sbatchd.log.* files' % len(res_logs)
	r_files(res_logs[:10])
	print time.time()-t1

	cnt = 0 
	for e in re_patterns:
		cnt += 1
		print cnt, e
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
