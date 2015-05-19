#~/usr/bin/python
import time
from cassandra.cluster import Cluster
cluster  = Cluster()
session = cluster.connect()

session.execute('USE testspace')

cql  = "SELECT * FROM test_timestamp WHERE date > '2015-05-17 20:45:00+0800' AND date < '2015-05-17 20:50:00+0800' ALLOW FILTERING"
print cql

res = session.execute(cql)
print res
for idx, date in res:
    print idx, date
    print idx, int(time.mktime(date.timetuple()))
    print type(idx), type(date)
