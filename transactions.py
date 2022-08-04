import random
import datetime 

import core as c

columnData = [
'customer_id',
'orderid',
'purchasedatetime',
'transactiontotal',
'numberofitems',
'productcode',
'productcategory',
'cc_number']

def generateTransactions(customerid: str, maxtrans: int):

	rowcount = 0
	transactions = ""

	for newrow in range(random.randint(1,maxtrans)):   # for each customer we gen 1-N transactions, change as desired
		newrow = ""
		transtotal = round(random.triangular(100, 2000),2) # triangular is awesome and creates a nice normal distro of values
		numitems = random.randint(1,15)

		newrow += c.quote + customerid + c.quotecomma
		newrow += c.quote + c.nextId() + c.quotecomma
		random_datetime = c.trans_start_date + datetime.timedelta(seconds=random.randint(1,c.max_seconds))	
		newrow += c.quote + str(random_datetime.replace(microsecond=0)) + c.quotecomma
		newrow += c.quote + str(transtotal) + c.quotecomma
		newrow += c.quote + str(numitems) + c.quotecomma		

		prodcode = random.randint(700000000,900000000)

		#product codes
		newrow += c.quote + str(prodcode) + c.quotecomma		
		newrow += c.quote + ("PR" + str(prodcode)[:3]) + c.quotecomma

		# CC number
		newrow += c.quote + str(random.randint(1000,9999)) + " "  \
						+ str(random.randint(1000,9999)) + " "  \
						+ str(random.randint(1000,9999)) + " "  \
						+ str(random.randint(1000,9999)) + c.quote

		if rowcount != maxtrans:			
			newrow += c.newline

		transactions += newrow
		rowcount+=1

	return(transactions)
