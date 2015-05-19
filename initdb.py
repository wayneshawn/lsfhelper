from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect()

f = open('db.conf','r')
stat = ''
for line in f:
	line = line.strip()
	if len(line) == 0:
		continue
	stat += line
	if line[-1] == ';':
		print stat
		session.execute(stat)
		print '---------------------'
		stat = ''
