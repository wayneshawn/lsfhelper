import web
from cassandra.cluster import Cluster
from cassandra.query import *
from mytime import *

try:
    cluster = Cluster()
    session = cluster.connect()
    session.set_keyspace('lsflog')
except Exception,e:
    print e

render = web.template.render('templates/')
cql = 'SELECT tm, bytesfmc, bytestmc FROM pcm LIMIT 1'
#cql7min = 'SELECT tm, bytesfmc, bytestmc FROM pcm LIMIT 7'
cql7min = 'SELECT tm, bytesfmc, bytestmc FROM pcm'
cqljfinish = 'SELECT job_id, event_time, jstatus, exit_info FROM jfinishlog LIMIT 20;'

urls = (
    '/hello/(.*)', 'hello',
    '/pcm', 'pcm',
    '/pcm7min', 'pcm7min',
    '/jfinish', 'jfinish',
    '/jobbyqueue', 'jobByQueue',
    '/jobfinisheventriver', 'jobFinishEventRiver', 
    '/jobid/(.*)', 'jobid' 
)

app = web.application(urls, globals())

class hello:
    def GET(self, name):
	if not name:
	    name = 'World'
	return render.index(name)
class pcm:
    def GET(self):
	res = session.execute(cql)
	row = [round(res[0][1],2),round(res[0][2],2)]
	return render.pcm(row)
class pcm7min:
    def GET(self):
	try:
	    res = session.execute(cql7min)
	except Exception,e:
	    print e
	tms = []
	bfmcs = []
	btmcs = []
	for tm, bf, bt in res:
	    tms.append(str(stamp_to_time(tm)))
	    bfmcs.append(round(bf,2))
	    btmcs.append(round(bt,2))
	    #bfmcs.append(int(bf))
	    #btmcs.append(int(bt))
	
	data = {'tms':tms, 'bfmcs':bfmcs, 'btmcs':btmcs}
	#print tms

	return render.pcm7min(data)

class jfinish:
    def GET(self):
	try:
	    res = session.execute(cqljfinish)
	except Exception,e:
	    print e

	#cqljfinish = 'SELECT job_id, event_time, jstatus, exit_info FROM jfinishlog LIMIT 20;'
	j32 = []
	j64 = []
	
	data = []
	#data = {'tms':tms, 'bfmcs':bfmcs, 'btmcs':btmcs}
	#print tms

	return render.pcm7min(data)
class jobByQueue:
    def getQueueJobNum(self):
	query_template = 'SELECT COUNT(*) FROM job_exitinfo WHERE queue=\'%s\''
	defined_queues = ['normal', 'hpc_linux', 'priority', 'short', 'ycy', 'yanning']
	queue_jobnum = {}
	for q in defined_queues:
	    try:
		print query_template % q
		res = session.execute(query_template % q)
		cnt, = res[0]
		if cnt>0:
		    queue_jobnum[q] = cnt
	    except Exception,e:
		print e
	    #queue_jobnum.append(cnt)
	return queue_jobnum
    def getQueueJstatus(self):
	query_template = 'SELECT COUNT(*) FROM job_exitinfo WHERE queue=\'%s\' and jstatus=%d'
	defined_queues = ['normal', 'hpc_linux', 'priority', 'short', 'ycy', 'yanning']
	queue_js32 = []
	queue_js64 = []
	queue_num = []
	for q in defined_queues:
	    try:
		res = session.execute(query_template % (q,32))
		cnt32, = res[0]
		res = session.execute(query_template % (q,64))
		cnt64, = res[0]

		queue_js32.append(cnt32)
		queue_js64.append(cnt64)
		queue_num.append(cnt32+cnt64)
	    except Exception,e:
		print e
	result = {'queues':defined_queues, 'js32':queue_js32, 'js64':queue_js64, 'queuenum':queue_num}
	return result
    def getQueueDataFromDB(self):
	query = 'SELECT queue, jobnum, jstatus32num, jstatus64num, exit0, exit5, exit8, exit14, exit15, exit17 FROM jfinishdata'
	res = session.execute(query)

	queue_js32 = []
	queue_js64 = []
	queue_num = []
	qs = []
	lexit0 = []
	lexit5 = []
	lexit8 = []
	lexit14 = []
	lexit15 = []
	lexit17 = []
	
	for queue, jobnum, jstatus32, jstatus64, exit0, exit5, exit8, exit14, exit15, exit17 in res: 
	    qs.append(str(queue))
	    queue_js32.append(jstatus32)
	    queue_js64.append(jstatus64)
	    queue_num.append(jobnum)
	    lexit0.append(exit0) 
	    lexit5.append(exit5)
	    lexit8.append(exit8)
	    lexit14.append(exit14)
	    lexit15.append(exit15)
	    lexit17.append(exit17)

	result = {'queues':qs, 'js32':queue_js32, 'js64':queue_js64, 'queuenum':queue_num, 'exit0':lexit0, 'exit5':lexit5, 'exit8':lexit8, 'exit14':lexit14, 'exit15':lexit15, 'exit17':lexit17}
	return result
	

    def GET(self):
	#queue_jobnum = self.getQueueJobNum()
#	result = self.getQueueJstatus()
	result = self.getQueueDataFromDB()
	print result
	return render.queuejobnum(result)
#	return 'hello'
class jobFinishEventRiver:
    def GET(self):
	query = 'SELECT job_id, jstatus, event_time FROM jfinishlog LIMIT 50'
	res = session.execute(query)
	jobids_32 = []
	finishtime_32 = []
	jobids_64 = []
	finishtime_64 = []
	for jobid, jstatus, etime in res:
	    if jstatus==32:
		jobids_32.append(jobid)
		finishtime_32.append(str(stamp_to_time(etime)))
	    else:
		jobids_64.append(jobid)
		finishtime_64.append(str(stamp_to_time(etime)))
	
	data = {'url':'jobbyqueue'}
	data['job_exit'] = {'jobids':jobids_32, 'etimes':finishtime_32} 
	data['job_done'] = {'jobids':jobids_64, 'etimes':finishtime_64} 
	return render.jobfinisheventriver(data)
	
class jobid:
    def GET(self, jobid):
	query = 'SELECT * FROM jfinishlog LIMIT 50'
	session.row_factory = dict_factory
	res = session.execute(query)
	#d = dict(res[0])
	print res[0]
#	d = {'key1':'va1', 'k2':2, 3:4, 5:6}
	return render.jobid(res[0])
	    
if __name__ == '__main__':
    app.run()
