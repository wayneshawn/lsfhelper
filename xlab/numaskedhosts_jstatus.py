from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

def num_askedhosts():
    query = 'SELECT num_askedhosts, jstatus FROM jfinishlog'
    statment = SimpleStatement(query, fetch_size=5000)

    cnt = 0
    js32_nahs = []
    js64_nahs = []
    for res in session.execute(statment):
	cnt += 1
	nahs, js = res
	if nahs > 0:
	    print res
	if js==32:
	    js32_nahs.append(nahs)	
	else:
	    assert(js==64)
	    js64_nahs.append(nahs)

    print len(js32_nahs)
    print float(sum(js32_nahs))/len(js32_nahs)

    print len(js64_nahs)
    print float(sum(js64_nahs))/len(js64_nahs)

    print cnt

def jnew_rlimit():
    query = 'SELECT job_id, rl_cpu_time, rl_mem_size, rl_run_time FROM jnewlog;'
    statment = SimpleStatement(query, fetch_size=5000)

    cnt = 0
    cnt_rlim = 0
    cnt_rlim_finish = 0
    cnt_rlim_js32 = 0
    cnt_rlim_js64 = 0
    for res in session.execute(statment):
	cnt += 1
	jobid, cputime, memsize, runtime = res
	if cputime==-1 and memsize==-1 and runtime==-1:
	    continue

	cnt_rlim += 1

	query2 = 'SELECT queue, jstatus,exit_info FROM jfinishlog WHERE job_id=%d'
	res2 = session.execute(query2 % jobid)	
	if len(res2)>0:
	    cnt_rlim_finish += 1
	    queue, jstatus,exit_info = res2[0]
	    print jobid, cputime, memsize, runtime, jstatus, exit_info 
	    if jstatus == 32:
		cnt_rlim_js32 += 1
	    else:
		cnt_rlim_js64 += 1

    print 'cnt', cnt
    print 'cnt_rlim', cnt_rlim
    print 'cnt_rlim_finish', cnt_rlim_finish
    print 'cnt_rlim_js32', cnt_rlim_js32
    print 'cnt_rlim_js64', cnt_rlim_js64
	
#num_askedhosts()
jnew_rlimit()
cluster.shutdown()

