import re
import os
class formatter():
	p_jnew = re.compile(r'\"JOB_NEW\"\s\"8.0\"\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s\"([^\s]+)\" ([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s\"([^\s]*)\"\s+([\d\.]+)\s(\d+)\s\"(?P<queue>[\w_]+)\"\s\"([^\"]*)\"\s\"(\w+)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]+)\"\s\"(?P<jobFile>[\d\.]+)\"\s(\d+)\s((?:\"c\d\db\d\d\"\s)*)\"(.*)\"\s\"(.*)\"\s"(.*)\"\s"(.*)\"\s0')

	p_jstart = re.compile(r'\"JOB_START\"\s\"8.0\"\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s([^\s]+)\s((?:\"c\d\db\d\d\"\s)*)\"(.*)\"\s\"(.*)\"\s(\d+)\s\"(.*)\"\s(\d+)\s\"(.*)\"\s\d+\s\d+')
	p_jstartac = re.compile(r'\"JOB_START_ACCEPT\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)')   
	#0-eventtime 1-job_id 2-execUid 3-jobpgid 4-execcwd-s 5-execHome-s
	#6-execUsername-s 7-jobpid 8-idx 9-addinfo 10-sla 11-dura4bkill
	p_jexec = re.compile(r'\"JOB_EXECUTE\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s\"(.*)\"\s\"(.*)\"\s\"([^\s]+)\"\s(\d+)\s(\d+)\s\"(.*)\"\s([^\s]+)\s\".*\"\s[^\s]+\s(\d+)')
	p_jstatus = re.compile(r'\"JOB_STATUS\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(?P<subreasons>\d+)\s([\d\.]+)\s(\d+)\s(\d)\s((?:(?:[\d\.\-]+\s){19}))?(\d+)\s(\d+)\s(\d+)\s(\d+)')
	p_jmove = re.compile(r'\"JOB_MOVE\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s\"([^\s]+)\"')
	#0-eventtime 1-job_id 2-user_id 3-runCount 4-sigSymbol-s 5-idx 6-username-s 
	p_jsignal = re.compile(r'\"JOB_SIGNAL\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s\"([^\s]+)\"\s(\d+)\s\"([^\s]+)\"')
	p_jclean = re.compile(r'\"JOB_CLEAN\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)')
	#p = re.compile(r'\"(HOST_CTRL)\"\s\"(8.0)\"\s(\d+)\s(\d+)\s\"([^\s]+)\s(\d+)\s\"(.*)\"\s\"(.*)\"')
	#0-eventtime 1-jobid 2-userid 3-options 4-numProcessors 5-submittime 6-begintime 7-termtime 8-starttime
	#9-username-s 10-queue-s 11-resReq-s 12-dependCond-s 13-preExecCmd-s 14-fromHost-s 15-cwd-s 16-infile-s 
	#17-outfile-s 18-errfile-s 19-jobfile 20-numAskedHosts 21-askedHosts-s 22-numExhosts 23-execHosts-s 
	#24-jstatus 25-hostfactor-f 26-jobname-s 27-cmd-s 28-lsfusage-list<float> 29-mailUser-s 30-projectName-s 
	#31-exitStatus 32-maxNumProcessors 33-loginshell-s 34-timeEvent-s 35-idx 36-maxrmem 37-maxrswap 
	#38-infilespool-s 39-cmdspool-s 40-rsvid-s 41-sla-s 42-exceptMask 43-addinfo-s 44-exitinfo
	p_jfinish = re.compile(r'\"JOB_FINISH\"\s\"8.0\"\s(\d+)\s(\d+)\s(\d+)\s([\d\-]+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s\"([^\s]+)\"\s\"([^\s]+)\"\s\"([^\"]*)\"\s\"(.*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"(?P<jobFile>[^\"]*)\"\s(\d+)\s((?:\"[^\"]+\"\s)*)(\d+)\s((?:\"c\d\db\d\d\"\s)*)(\d+)\s([\d\.]+)\s\"([^\"]*)\"\s\"(.*)\"\s((?:[\d\.-]+\s){19})\"([^\"]*)\"\s\"([^\"]*)\"\s([\d\-]+)\s([\d]+)\s\"([^\"]*)\"\s\"([^\"]*)\"\s([\d\-]+)\s([\d\-]+)\s([\d\-]+)\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s\"([^\"]*)\"\s([\d\-]+)\s\"([^\"]*)\"\s(?P<exitInfo>\d+)')

	#map_event_type_num = {jnew:0, jstart:1, jstartac:2, jexec:3,
	#   jstatus:4, jmove:5, jsignal:6, jclean:7, jfinish:8}
	def split(self, event_type, line):
		if event_type == 0:
			m = self.p_jnew.match(line)
		elif event_type == 1:
			m = self.p_jstart.match(line)
		elif event_type == 2:
			m = self.p_jstartac.match(line)
		elif event_type == 3:
			m = self.p_jexec.match(line)
		elif event_type == 4:
			m = self.p_jstatus.match(line)
		elif event_type == 5:
			m = self.p_jmove.match(line)
		elif event_type == 6:
			m = self.p_jsignal.match(line)
		elif event_type == 7:
			m = self.p_jclean.match(line)
		elif event_type == 8:
			m = self.p_jfinish.match(line)

		if m:
			strs = m.groups()
		else:
			strs = None
		return strs
