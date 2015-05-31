#!/usr/bin/python
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

query = 'SELECT queue, jstatus, exit_info FROM job_exitinfo'
statment = SimpleStatement(query, fetch_size=5000)

qs = {}
for res in session.execute(statment):
    queue, jstatus, exit_info = res
    if queue not in qs:
	qs[queue] = {
	    'jobnum':0,
	    'jstatus32':0,
	    'jstatus64':0,
	    'exit0':0,
	    'exit5':0,
	    'exit8':0,
	    'exit14':0,
	    'exit15':0,
	    'exit17':0,
	    'exitothers':0
	}
    qs[queue]['jobnum'] += 1
    if jstatus==32:
	qs[queue]['jstatus32'] += 1

	#if jstatus==32, exit_info represent TERM_REASON
	#0-TERM_UNKNOWN 5-TERM_RUNLIMIT 8-TERM_FORCE_OWNER
	#14-TERM_OWNER 15-TERM_ADMIN 16-TERM_ETERNAL_SIGNAL
	term_r = 'exit'+str(exit_info)
	if term_r not in qs[queue]:
	    qs[queue]['exitothers'] += 1
	else:
	    qs[queue][term_r] += 1

    else:
	qs[queue]['jstatus64'] += 1


stmt = session.prepare('INSERT INTO jfinishdata(queue, jobnum, jstatus32num, jstatus64num, exit0, exit5, exit8, exit14, exit15, exit17) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
for q in qs:
    print qs[q]
    session.execute(stmt, (q, qs[q]['jobnum'], qs[q]['jstatus32'], qs[q]['jstatus64'], qs[q]['exit0'], qs[q]['exit5'], qs[q]['exit8'], qs[q]['exit14'], qs[q]['exit15'], qs[q]['exit17']))
    

cluster.shutdown()
