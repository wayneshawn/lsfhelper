import time
'''
transfer time list
['Mar', '31', '20:51:03', '2014']
to timstamp

'''
month_map = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
def to_time_stamp(strs):
	tmp = strs[3]+'-'+month_map[strs[0]]+'-'+strs[1]+' '+strs[2]
	tstamp = int(time.mktime(time.strptime(tmp, '%Y-%m-%d %H:%M:%S')))
	return tstamp

def stamp_to_time(stamp):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

if __name__ == '__main__':
	e = ['Mar', '31', '20:51:03', '2014']
	print '-'.join(e) 
	print to_time_stamp(e)
	
	e = ['Apr', '17', '19:00:00', '2015']
	print '-'.join(e) 
	print to_time_stamp(e)
 	
	print 1431912603, stamp_to_time(1431912603)
	print 1431883033, stamp_to_time(1431883033)
	print 1431877718, stamp_to_time(1431877718)
	print 1431838118, stamp_to_time(1431838118)
	int_max = 2**31-1
	print int_max, stamp_to_time(int_max)

	e = ['May', '18', '9:00:00', '2015']
	print '-'.join(e) 
	print to_time_stamp(e)
	e = ['May', '18', '9:05:00', '2015']
	print '-'.join(e) 
	print to_time_stamp(e)

	
