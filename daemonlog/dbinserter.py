from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from mytime import to_time_stamp
import time

class inserter():
	cluster = None
	session = None
	stmt_jnew = None
	stmt_jstart = None
	stmt_jstart_ac = None
	stmt_jexec = None
	stmt_jstatus = None
	stmt_jsignal = None
	stmt_jmove = None
	stmt_jclean = None		
	stmt_jfinish = None
	batch = None
	batch_cnt = 0

	def __init__(self):
		self.cluster = Cluster()
		self.session = self.cluster.connect()
		self.session.set_keyspace('lsflog2')
		self.stmt_jnew = self.session.prepare('INSERT INTO jnewlog(event_time, job_id, user_id, num_processors, submit_time, begin_time, term_time, user_name, rl_cpu_time, rl_file_size, rl_dseg_size, rl_sseg_size, rl_cfile_size, rl_mem_size, rl_run_time, queue, num_askedhosts, askedhosts, command) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jstart = self.session.prepare('INSERT INTO jstartlog(event_time, job_id, jstatus, job_pid, job_pgid, host_factor, num_exechosts, exechosts, jflags, user_group, idx, add_info) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jstart_ac = self.session.prepare('INSERT INTO jstartaclog(event_time, job_id, job_pid, job_pgid, idx) VALUES(?, ?, ?, ?, ?)')
		self.stmt_jexec = self.session.prepare('INSERT INTO jexeclog(event_time, job_id, jstatus, job_pid, job_pgid, idx, sla_run_limit, dura4bkill) VALUES(?, ?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jstatus = self.session.prepare('INSERT INTO jstatuslog(event_time, job_id, jstatus, reason, subreasons, cpu_time, end_time, ru, lsfRusage, exit_status, idx, exit_info, dura4bkill) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jsignal = self.session.prepare('INSERT INTO jsignallog(event_time, job_id, user_id, run_count, signal_simb, idx, user_name) VALUES(?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jmove = self.session.prepare('INSERT INTO jmovelog(event_time, user_id, job_id, position, base, idx, user_name) VALUES(?, ?, ?, ?, ?, ?, ?)')
		self.stmt_jclean = self.session.prepare('INSERT INTO jcleanlog(event_time, job_id, idx) VALUES(?, ?, ?)')
		self.stmt_jfinish = self.session.prepare('INSERT INTO jfinishlog(event_time, job_id, user_id, num_processors, submit_time, begin_time, term_time, start_time, user_name, queue, num_askedhosts, askedhosts, num_exechosts, exechosts, jstatus, host_factor, lsfrusage, exit_status, max_num_processors, exit_info) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
		self.batch = BatchStatement()
		batch_cnt = 0
	#map_event_type_num = {jnew:0, jstart:1, jstartac:2, jexec:3,
	#   jstatus:4, jmove:5, jsignal:6, jclean:7, jfinish:8}
	def batch_add(self, event_type, strs):
		if event_type == 0:
			event_time = int(strs[0])
			job_id = int(strs[1])
			user_id = int(strs[2])
			num_processors = int(strs[4])	
			submit_time = int(strs[5])	
			begin_time = int(strs[6])	
			term_time = int(strs[7])	
			user_name = strs[11]	
			rl_cpu_time = int(strs[12])	
			rl_file_size = int(strs[13])	
			rl_dseg_size = int(strs[14])	
			rl_sseg_size = int(strs[15])	
			rl_cfile_size = int(strs[16])	
			rl_mem_size = int(strs[17])	
			rl_run_time = int(strs[21])	
			queue = strs[26]	
			num_askedhosts = eval(strs[36])	
			askedhosts = strs[37]	
			command = strs[41]	
			self.batch.add(self.stmt_jnew, (event_time, job_id, user_id, num_processors, submit_time, begin_time, term_time, user_name, rl_cpu_time, rl_file_size, rl_dseg_size, rl_sseg_size, rl_cfile_size, rl_mem_size, rl_run_time, queue, num_askedhosts, askedhosts, command))
		elif event_type == 1:
			event_time = eval(strs[0])
			job_id = int(strs[1])
			jstatus = int(strs[2])
			job_pid = int(strs[3])
			job_pgid = int(strs[4])
			host_factor = float(strs[5])
			num_exechosts = int(strs[6])
			exechosts = strs[7]
			jflags = int(strs[10])
			user_group = strs[11]
			idx = int(strs[12])
			add_info = strs[13]
			self.batch.add(self.stmt_jstart, (event_time, job_id, jstatus, job_pid, job_pgid, host_factor, num_exechosts, exechosts, jflags, user_group, idx, add_info))
		elif event_type == 2:
			event_time = int(strs[0])
			job_id = int(strs[1])
			job_pid = int(strs[2])
			job_pgid = int(strs[3])
			idx = int(strs[4])
			self.batch.add(self.stmt_jstart_ac, (event_time, job_id, job_pid, job_pgid, idx))
		elif event_type == 3:
			event_time = int(strs[0])
			job_id = int(strs[1])
			jstatus = int(strs[2])
			job_pgid = int(strs[3])
			job_pid = int(strs[7])
			idx = int(strs[8])
			sla_run_limit = int(strs[10])
			dura4bkill = int(strs[11])
			self.batch.add(self.stmt_jexec, (event_time, job_id, jstatus, job_pid, job_pgid, idx, sla_run_limit, dura4bkill))
		elif event_type == 4:
			event_time = int(strs[0])
			job_id = int(strs[1])
			jstatus = int(strs[2])
			reason = int(strs[3])
			subreasons = int(strs[4])
			cpu_time = float(strs[5])
			end_time = int(strs[6])
			ru = int(strs[7])
			if strs[8] != None:
				lsfRusage = [float(us) for us in strs[8].split()]
			else:
				lsfRusage = []
			exit_status = int(strs[9])
			idx = int(strs[10])
			exit_info = int(strs[11])
			dura4bkill = int(strs[12])
			self.batch.add(self.stmt_jstatus, (event_time, job_id, jstatus, reason, subreasons, cpu_time, end_time, ru, lsfRusage, exit_status, idx, exit_info, dura4bkill))
		elif event_type == 5:
			event_time = int(strs[0])
			user_id = int(strs[1])
			job_id = int(strs[2])
			position = int(strs[3])
			base = int(strs[4])
			idx = int(strs[5])
			user_name = strs[6]
			self.batch.add(self.stmt_jmove, (event_time, user_id, job_id, position, base, idx, user_name))
		elif event_type == 6:
			event_time = int(strs[0])
			job_id = int(strs[1])
			user_id = int(strs[2])
			run_count = int(strs[3])
			signal_simb = strs[4]
			idx = int(strs[5])
			user_name = strs[6]
			self.batch.add(self.stmt_jsignal, (event_time, job_id, user_id, run_count, signal_simb, idx, user_name))
		elif event_type == 7:
			event_time = int(strs[0])
			job_id = int(strs[1])
			idx = int(strs[2])
			self.batch.add(self.stmt_jclean, (event_time, job_id, idx))
		elif event_type == 8:
			event_time = int(strs[0])
			job_id = int(strs[1])
			user_id = int(strs[2])
			num_processors = int(strs[4])
			submit_time = int(strs[5])
			begin_time = int(strs[6])
			term_time = int(strs[7])
			start_time = int(strs[8])
			user_name = strs[9]
			queue = strs[10]
			num_askedhosts = int(strs[20])
			askedhosts = strs[21]
			num_exechosts = int(strs[22])
			exechosts = strs[23]
			jstatus = int(strs[24])
			host_factor = float(strs[25])
			lsfrusage = [float(us) for us in strs[28].split()]
			exit_status = int(strs[31])
			max_num_processors = int(strs[32])
			exit_info = int(strs[44])
			
			self.batch.add(self.stmt_jfinish, (event_time, job_id, user_id, num_processors, submit_time, begin_time, term_time, start_time, user_name, queue, num_askedhosts, askedhosts, num_exechosts, exechosts, jstatus, host_factor, lsfrusage, exit_status, max_num_processors, exit_info))

		self.batch_cnt += 1
		if self.batch_cnt == 500:
			print 'batch_insert 500' 
			try:
				self.session.execute(self.batch)
			except Exception, e:
				print 'execute batch error'
				print e
				self.session.execute(self.batch)

			self.batch = BatchStatement()
			self.batch_cnt = 0
	def close(self):
		if self.batch_cnt > 0:
			try:
				self.session.execute(self.batch)
			except Exception, e:
				print 'execute batch error'
				print e
				self.session.execute(self.batch)

class errlogInserter():
	cluster = None
	session = None
	stmt = None
	batch = None
	batch_cnt = 0

	def __init__(self):
		self.cluster = Cluster()
		self.session = self.cluster.connect()
		self.session.set_keyspace('lsflog2')
		self.stmt = self.session.prepare('INSERT INTO daemonerrlog(log_type, host_name, log_time, field4, field5, msg) VALUES(?, ?, ?, ?, ?, ?)')
		self.batch = BatchStatement()
		batch_cnt = 0

	def batch_add(self, strs):
		#log_type = strs[7]
		#host_name = strs[8]
		#print strs[:4]
		log_time = to_time_stamp(strs[:4])	
		field4 = int(strs[4])
		field5 = int(strs[5])
		#msg = strs[6]
		self.batch.add(self.stmt, (strs[7], strs[8], log_time, field4, field5, strs[6]))

		self.batch_cnt += 1

		if self.batch_cnt == 500:
			print 'batch_insert 500' 
			try:
				self.session.execute(self.batch)
			except Exception, e:
				print 'execute batch error'
				print e
				self.session.execute(self.batch)
			self.batch = BatchStatement()
			self.batch_cnt = 0

	def close(self):
		if self.batch_cnt > 0:
			try:
				self.session.execute(self.batch)
			except Exception, e:
				print 'execute batch error'
				print e
				self.session.execute(self.batch)

