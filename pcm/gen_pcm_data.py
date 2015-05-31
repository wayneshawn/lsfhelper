import intelpcm as pcm 
import random
import time
from cassandra.cluster import Cluster


def create_node_table():
    cluster = Cluster()
    session = cluster.connect()
    session.set_keyspace('lsflog')
    
    cql = """CREATE TABLE IF NOT EXISTS perf(
	node text, tm int, exec float, ipc float, freq float, l2hitr float, l3hitr float, bytesfmc float, bytestmc float, PRIMARY KEY(node, tm))"""

    try:
	session.execute(cql)
    except Exception,e:
	print e
    finally:
	cluster.shutdown()

def gen_node_list():
    nodes = []
    for c in range(1,38):
	if c<10:
	    c_part = 'c0'+str(c)
	else:
	    c_part = 'c'+str(c)
	for b in range(1,21):
	    if b<10:
		b_part = 'b0'+str(b)
	    else:
		b_part = 'b'+str(b)
	    nodes.append(c_part+b_part)
    return nodes
    
def gen_data(nodes, start_time, end_time, interval):
    

if __name__=='__main__':
    nodes = gen_node_list()
