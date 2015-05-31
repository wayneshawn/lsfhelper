from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

res = session.execute('SELECT exechosts FROM jfinishlog LIMIT 100')
for exechosts, in res:
    if exechosts:
	ehs = exechosts.split()
	ehs = [eh.strip('"') for eh in ehs]
	ehs = list(set(ehs))
	print ehs
