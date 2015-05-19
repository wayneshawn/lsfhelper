from cassandra.cluster import Cluster
import os

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')


outfile = 'result.out'
if os.path.exists(outfile):
    print 'delete existing old', outfile
    os.remove(outfile)
f = open(outfile, 'w')

jobid_start = 4744111
#jobid_start = 4748100
jobid_end = 4755291

cql_jnew = 'select event_time, submit_time, begin_time, term_time from jnewlog where job_id=%s'
cql_jstart = 'select event_time from jstartlog where job_id=%s'
cql_jclean = 'select event_time from jcleanlog where job_id=%s'

id_cnt = 0
jnew_cnt = 0
jclean_cnt = 0
for i in range(jobid_start, jobid_end):
    id_cnt += 1
    if i%100==0:
	print i
    res_jnew = session.execute(cql_jnew % str(i))
    if res_jnew:
	jnew_cnt += 1
    else:
	res_jclean = session.execute(cql_jclean % str(i))
	if res_jclean:
	    print 'id no jnew but has jclean' % i
	    exit(1)
	continue

    #res_jstart = session.execute(cql_jstart % str(i))
    res_jclean = session.execute(cql_jclean % str(i))

    if res_jclean:
	jclean_cnt += 1
    else:
	continue
    
    et, st, bt, tt  = res_jnew[0] 
    et_jc, = res_jclean[0]
    f.write("%d\t%d\t%d\t%d\t%d\t%d\n" % (et, st, bt, tt, et_jc, et_jc-et))
    
f.close()

print id_cnt, jnew_cnt, jclean_cnt
