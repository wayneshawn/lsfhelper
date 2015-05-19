from cassandra.cluster import Cluster
from mytime import stamp_to_time

cluster = Cluster()
session = cluster.connect()
session.set_keyspace('lsflog')

cql5min = 'SELECT tm, bytesfmc, bytestmc FROM pcm LIMIT 7'
res = session.execute(cql5min)
print type(res)

tms = []
bfmcs = []
btmcs = []
for tm, bf, bt in res:
    tms.append(stamp_to_time(tm))
    bfmcs.append(round(bf,2))
    btmcs.append(round(bt,2))

print tms
print bfmcs
print btmcs
