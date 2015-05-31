from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

signals = []
query = 'SELECT job_id,signal_simb FROM jsignallog'
q2 = 'SELECT jstatus,exit_info from jfinishlog where job_id=%d'
res = session.execute(query)
for jobid, ss in res:
    signals.append(ss)
    if ss=='CONT':
	print session.execute(q2 % jobid) 

signals = set(signals)
print signals
