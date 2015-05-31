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

def stamp_round_day(stamp):
  datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))
  return


if __name__ == '__main__':
	e = ['Apr', '1', '0:0:0', '2015']
	print '%-25s' % '-'.join(e), 
	print to_time_stamp(e)
	
	e = ['May', '1', '0:0:0', '2015']
	print '%-25s' % '-'.join(e), 
	print to_time_stamp(e)
 	

	#lsb.events.123
	t = 1427817369
	print '%-25d' % t, stamp_to_time(t)
	#lsb.events.35
	t = 1430536956
	print '%-25d' % t, stamp_to_time(t)
