from cassandra.cluster import Cluster
import os

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')


outfile = 'jfinish_term_reason.out'
if os.path.exists(outfile):
    print 'delete existing old', outfile
    os.remove(outfile)
f = open(outfile, 'w')

cql_count = 'select count(*) from jfinishlog where jstatus=32 and exit_info=%d limit 100000 allow filtering'
cql_jobid = 'select job_id from jfinishlog where jstatus=32 and exit_info=%d limit 100000 allow filtering'
for i in range(1,30):
    res = session.execute(cql_count % i)
    cnt, = res[0]
    if cnt > 0:
	print i, cnt
	f.write("TERM_REASON %d, COUNT=%d\n" % (i, cnt))
	res = session.execute(cql_jobid % i)
	for jobid, in res:
	    f.write("%d\t%d\n" % (i, jobid) )

f.close()

