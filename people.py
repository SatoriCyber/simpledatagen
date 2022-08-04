import core as c
import helpers as h
import transactions
import social

#if you append new columns, you need to ensure you have defined a handler for each of these in helpers.py
#we have provided a few as examples

#these are in addition to the core columns found in core.py
#their handlers are found in helpers.py
extraColumns = [ 
"job_type",
"account_type",
"phone_number",
"ssn",
"allergies",
"blood_type",
"last_ipaddress"
]

#the main function
def createData(headers: bool, rows: int, buildtransactions: bool, *args) -> str:

	#our three csv output variables. note: these are just big strings
	#this was the purpose of the exercise for this entire solution :)

	listOfNewRows = ""
	listOfNewTransactions = ""
	listOfNewSocialInteractions = ""

	# if asked for headers, first we print out the core headers, followed by the extra ones
	if headers:
		#core columns
		for idx, item in enumerate(c.coreColumns):
			listOfNewRows += c.quote + item + c.quote
			if idx+1 != len(c.coreColumns):
				listOfNewRows += c.comma
		#extra columns
		if len(extraColumns) > 0:
			listOfNewRows += c.comma
		for idx, item in enumerate(extraColumns):
			listOfNewRows +=c.quote + item + c.quote
			if idx+1 != len(extraColumns):
				listOfNewRows += c.comma
		listOfNewRows += c.newline

	# if asked for transaction and social data (related child records) we print out their headers first, if headers is True, 
	if buildtransactions & headers:
		for idx, item in enumerate(transactions.columnData):
			listOfNewTransactions += c.quote + item + c.quote
			if idx+1 != len(transactions.columnData):
				listOfNewTransactions += c.comma
		listOfNewTransactions += c.newline

		for idx, item in enumerate(social.columnData):
			listOfNewSocialInteractions += c.quote + item + c.quote
			if idx+1 != len(social.columnData):
				listOfNewSocialInteractions += c.comma
		listOfNewSocialInteractions += c.newline

	# done with people.csv headers, now start the main iter
	rowcount = 0
	for newrow in range(rows):
		newrow = ""
		identity_bundle = c.handlerMap("identity_bundle")
		geolocation_bundle = c.handlerMap("geolocation_bundle")
		newid = c.handlerMap("customer_id")
		birthdate = str(c.handlerMap("birth_dt"))

		# 1 the ID
		newrow += c.quote + newid + c.quotecomma								
		# 2 the identity info
		for item in range(len(identity_bundle)):						
			newrow += c.quote + identity_bundle[item] + c.quotecomma
		# 3 the geo info
		for item in range(len(geolocation_bundle)):						
			newrow += c.quote + geolocation_bundle[item] + c.quotecomma
		# 4 birthdate
		newrow += c.quote + birthdate + c.quotecomma	

		# 5 for any extra columns you have defined, call their handler in helpers.py
		for idx, item in enumerate(extraColumns):					
			newrow += c.quote + h.extraHandlerMap(item) + c.quote
			newrow += c.comma if idx+1 != len(extraColumns) else ""
		#6 add a newline if not last line
		if rowcount != rows:														
			newrow += c.newline
		
		listOfNewRows+= newrow



		if buildtransactions:
			maxrows = int(args[0])
			
			#generate transaction data
			listOfNewTransactions += transactions.generateTransactions(newid, maxrows)

			#generate social data
			#in the next line, identity_bundle[4] is the email address, we are sending it into the social data
			listOfNewSocialInteractions += social.generateSocialInteractions(newid, maxrows, identity_bundle[4])

		rowcount+=1

	return listOfNewRows, listOfNewTransactions, listOfNewSocialInteractions
