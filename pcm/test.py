#!/usr/bin/python
import intelpcm as pcm 
import random
import time
from cassandra.cluster import Cluster

m = pcm.PCM()
stat = m.program()
print stat
if stat==2:
    m.resetPMU()
    m.cleanup()
    m = pcm.PCM()

print 'core num', m.getNumCores()
print 'socket num', m.getNumSockets()

ss1 = pcm.SystemCounterState()
ss2 = pcm.SystemCounterState()

cs1 = pcm.vec_CoreCounterState()
cs2 = pcm.vec_CoreCounterState()

skts1 = pcm.vec_SocketCounterState()
skts2 = pcm.vec_SocketCounterState()


#while True:
m.getAllCounterStates(ss1, skts1, cs1)

time.sleep(2)

m.getAllCounterStates(ss2, skts2, cs2)

print " Core | EXEC | IPC | FREQ | L3HITS | L3HITR | L2HITS | L2HITR"
for i in range(m.getNumCores()):
    print "  %-4d" % i,
    execusage = pcm.getExecUsage(cs1[i], cs2[i])
    rf = pcm.getRelativeFrequency(cs1[i], cs2[i])
    ipc = pcm.getIPC(cs1[i], cs2[i])
    l2hitr = pcm.getL2CacheHitRatio(cs1[i], cs2[i])
    l2hits = pcm.getL2CacheHits(cs1[i], cs2[i])
    l3hitr = pcm.getL3CacheHitRatio(cs1[i], cs2[i])
    l3hits = pcm.getL3CacheHits(cs1[i], cs2[i])
    print "%6.3f %5.3f %6.3f %8d %8.3f %8d %8.3f" % (execusage, ipc, rf, l3hits, l3hitr, l2hits, l2hitr) 
    
print '---------------------------------------------------'
print " Socket | EXEC | IPC | FREQ | L3HITS | L3HITR | L2HITS | L2HITR"

for i in range(m.getNumSockets()):
    print "  %-6d" % i,
    execusage = pcm.getExecUsage(skts1[i], skts2[i])
    rf = pcm.getRelativeFrequency(skts1[i], skts2[i])
    ipc = pcm.getIPC(skts1[i], skts2[i])
    l2hitr = pcm.getL2CacheHitRatio(skts1[i], skts2[i])
    l2hits = pcm.getL2CacheHits(skts1[i], skts2[i])
    l3hitr = pcm.getL3CacheHitRatio(skts1[i], skts2[i])
    l3hits = pcm.getL3CacheHits(skts1[i], skts2[i])
    print "%6.3f %5.3f %6.3f %8d %8.3f %8d %8.3f" % (execusage, ipc, rf, l3hits, l3hitr, l2hits, l2hitr) 

print '---------------------------------------------------'
execusage = pcm.getExecUsage(ss1, ss2)
rf = pcm.getRelativeFrequency(ss1, ss2)
#cycles = pcm.getCycles(ss1, ss2)
ipc = pcm.getIPC(ss1, ss2)
l2hitr = pcm.getL2CacheHitRatio(ss1, ss2)
l2hits = pcm.getL2CacheHits(ss1, ss2)
l3hitr = pcm.getL3CacheHitRatio(ss1, ss2)
l3hits = pcm.getL3CacheHits(ss1, ss2)

print "  TOTAL  %6.3f %5.3f %6.3f %8d %8.3f %8d %8.3f" % (execusage, ipc, rf, l3hits, l3hitr, l2hits, l2hitr) 

#BytesRead
t_rfmc = 0.0
t_wtmc = 0.0
for i in range(m.getNumSockets()):
    rfmc = pcm.getBytesReadFromMC(skts1[i], skts2[i])
    wtmc = pcm.getBytesWrittenToMC(skts1[i], skts2[i])
    print 'skt %d,\n BytesReadFromMC:%f G,\n BytesWrittemToMC:%f G. ' % (i, rfmc/float(1024**3), wtmc/float(1024**3))
    t_rfmc += rfmc/(float(1024**2))
    t_wtmc += wtmc/(float(1024**2))


pk = 2011011319
tm = int(time.time())
cluster = Cluster()
session = cluster.connect()
session.execute("""INSERT INTO lsflog.pcm(pk, tm, exec, ipc, freq, l2hitr, l3hitr, bytesfmc, bytestmc) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (pk, tm, execusage, ipc, rf, l2hitr, l3hitr, t_rfmc, t_wtmc) )
cluster.shutdown()
#    time.sleep(3)
#    print '\n'

m.cleanup()
