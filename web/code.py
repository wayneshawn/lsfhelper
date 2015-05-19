import web
from cassandra.cluster import Cluster
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
    '/jfinish', 'jfinish'
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

if __name__ == '__main__':
    app.run()
