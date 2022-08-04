import time

import people

# let's use a low tech timer to see how long the data gen takes
t_start = time.time()

# args: (user csv headers?, how many people?, create transactions?, how many transactions?)
args = (True, 10000, True, 10)

newdata = people.createData(*args)

# just to remind, people.createData returns two elements in an array,
# one for customers and one for their transactions

with open('output_people.csv', 'w') as f:
	f.write(newdata[0])
	print("finished writing people data")

with open('output_transactions.csv', 'w') as f:
	f.write(newdata[1])
	print("finished writing transaction data")

with open('output_social.csv', 'w') as f:
	f.write(newdata[2])
	print("finished writing social interaction data")

t_end = time.time()
totaltime = t_end-t_start
print(str(totaltime) + " seconds")