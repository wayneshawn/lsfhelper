f = open('jruntime.out','r')
tms = []
for line in f.readlines():
    strs = line.split()

    #sec
    runtime = int(strs[3])
    tms.append(runtime)

print 'job_num ', len(tms)
print 'mean_time', sum(tms)/len(tms)

tms_u10 = [e for e in tms if e<10]
print '\njob_num_u10 ', len(tms_u10), float(len(tms_u10))/len(tms) 
print 'mean_time_u10', sum(tms_u10)/len(tms_u10)

tms_u100 = [e for e in tms if e>=10 and e<100]
print '\njob_num_u100 ', len(tms_u100), float(len(tms_u100))/len(tms)
print 'mean_time_u100', sum(tms_u100)/len(tms_u100)

tms_u1000 = [e for e in tms if e>=100 and e<1000]
print '\njob_num_u1000 ', len(tms_u1000), float(len(tms_u1000))/len(tms)
print 'mean_time_u1000', sum(tms_u1000)/len(tms_u1000)

tms_a1000 = [e for e in tms if e>=1000 and e<10000]
print '\njob_num_u10000 ', len(tms_a1000), float(len(tms_a1000))/len(tms)
print 'mean_time_u10000', sum(tms_a1000)/len(tms_a1000)

tms_a10000 = [e for e in tms if e>=10000]
print '\njob_num_a10000 ', len(tms_a10000), float(len(tms_a10000))/len(tms)
print 'mean_time_a10000', sum(tms_a10000)/len(tms_a10000)
