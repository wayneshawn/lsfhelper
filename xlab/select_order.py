from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

query = 'SELECT * FROM job_exitinfo'
statment = SimpleStatement(query, fetch_size=5000)

cnt = 0
for res in session.execute(statment):
    cnt += 1
    jobid, event_time, submit_time, queue, jstatus, exit_info = res
    print jobid, event_time, submit_time, queue, jstatus, exit_info
print cnt

cluster.shutdown()
