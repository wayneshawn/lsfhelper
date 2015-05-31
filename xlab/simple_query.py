from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

query = 'SELECT job_id, exechosts FROM jfinishlog limit 10'

for res in session.execute(query):
    jobid,ehs = res
    #print jobid, ehs
    ehs = str(ehs).split()
    ehs = [ele.strip('"') for ele in ehs]
    ehs = list(set(ehs))
    print jobid, ehs

cluster.shutdown()
