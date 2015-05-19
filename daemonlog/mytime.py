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

if __name__ == '__main__':
	e = ['Mar', '31', '20:51:03', '2014']
	print to_time_stamp(e)
	
	e = ['Apr', '17', '19:00:00', '2015']
	print to_time_stamp(e)
 	
