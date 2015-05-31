from cassandra.cluster import Cluster
import os

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

outfile = 'jruntime.out'
if os.path.exists(outfile):
    print 'delete existing old', outfile
    os.remove(outfile)
f = open(outfile, 'w')

res = session.execute('SELECT job_id, submit_time, event_time FROM jfinishlog')

for jobid, st, et in res:
    if st<1:
	runtime = -1
    else:
	runtime = et-st
    f.write("%d\t%d\t%d\t%d\n" % (jobid, st, et, runtime))

f.close()
