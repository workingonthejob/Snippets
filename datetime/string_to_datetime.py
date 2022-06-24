from datetime import datetime

'''
Small snippet to show how to use the datetime library
to convert some datetime string into a datetime object.
'''

MMM_YYYY = 'Jan 2021'
MMM_DD_YYYY = 'Apr 19 1995'
MMM_DD_COMMA_YYYY = 'Jun 1, 2020'

dt = datetime.strptime(MMM_YYYY, '%b %Y')
print(dt)
dt = datetime.strptime(MMM_DD_YYYY, '%b %d %Y')
print(dt)
dt = datetime.strptime(MMM_DD_COMMA_YYYY, '%b %d, %Y')
print(dt)
