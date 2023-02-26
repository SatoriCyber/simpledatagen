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
		is_deleted = c.handlerMap("is_deleted")

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
		# 5 isDeleted flag, to emulate salesforce or other systems that mark records as deleted
		newrow += str(is_deleted) + c.comma
		
		# 6 for any extra columns you have defined, call their handler in helpers.py
		for idx, item in enumerate(extraColumns):					
			newrow += c.quote + h.extraHandlerMap(item) + c.quote
			newrow += c.comma if idx+1 != len(extraColumns) else ""
		#7 add a newline if not last line
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



#the main function
def createJsonData(headers: bool, rows: int, buildtransactions: bool, *args) -> str:

	#our three csv output variables. note: these are just big strings
	#this was the purpose of the exercise for this entire solution :)

	listOfNewRows = ""
	listOfNewTransactions = ""
	listOfNewSocialInteractions = ""

	#json array, so start with an open bracket
	listOfNewRows += c.openBracket + c.newline

	# done with people.csv headers, now start the main iter
	rowcount = 0
	for newrow in range(rows):
		newrow = ""
		identity_bundle = c.handlerMap("identity_bundle")
		geolocation_bundle = c.handlerMap("geolocation_bundle")
		newid = c.handlerMap("customer_id")
		birthdate = str(c.handlerMap("birth_dt"))
		is_deleted = c.handlerMap("is_deleted")


		newrow += c.openCurly + c.newline
		
		# 1 the ID and identity bundle
		newrow += c.quote + "customer_id" + c.quote + c.colon	+ c.quote + newid + c.quote	+ c.comma + c.newline
		newrow += c.quote + "gender" + c.quote + c.colon	+ c.quote + identity_bundle[0] + c.quote + c.comma + c.newline
		newrow += c.quote + "name_prefix" + c.quote + c.colon	+ c.quote + identity_bundle[1] + c.quote + c.comma + c.newline
		newrow += c.quote + "name_first" + c.quote + c.colon	+ c.quote + identity_bundle[2] + c.quote + c.comma + c.newline
		newrow += c.quote + "name_last" + c.quote + c.colon	+ c.quote + identity_bundle[3] + c.quote + c.comma + c.newline
		newrow += c.quote + "email" + c.quote + c.colon	+ c.quote + identity_bundle[4] + c.quote + c.comma + c.newline
		newrow += c.quote + "employment" + c.quote + c.colon	+ c.quote + identity_bundle[5] + c.quote + c.comma + c.newline

		#geo info
		newrow += c.quote + "address" + c.quote + c.colon	+ c.quote + geolocation_bundle[0] + c.quote + c.comma + c.newline
		newrow += c.quote + "city" + c.quote + c.colon	+ c.quote + geolocation_bundle[1] + c.quote + c.comma + c.newline
		newrow += c.quote + "county" + c.quote + c.colon	+ c.quote + geolocation_bundle[2] + c.quote + c.comma + c.newline
		newrow += c.quote + "state" + c.quote + c.colon	+ c.quote + geolocation_bundle[3] + c.quote + c.comma + c.newline
		newrow += c.quote + "postal_code" + c.quote + c.colon	+ c.quote + geolocation_bundle[4] + c.quote + c.comma + c.newline

		newrow += c.quote + "birth_dt" + c.quote + c.colon	+ c.quote + birthdate + c.quote + c.comma + c.newline

		#extra info
		for idx, item in enumerate(extraColumns):					
			newrow += c.quote + extraColumns[idx] + c.quote + c.colon + c.quote + h.extraHandlerMap(item) + c.quote + c.comma + c.newline

		newrow += c.quote + "is_deleted" + c.quote + c.colon + str(is_deleted) + c.newline




		#final row? ...For comma or no comma
		if rowcount == rows-1:
			newrow += c.closeCurly + c.newline
		else:
			newrow += c.closeCurly + c.comma + c.newline


		listOfNewRows+= newrow




		rowcount+=1

	listOfNewRows += c.closeBracket

	return listOfNewRows, listOfNewTransactions, listOfNewSocialInteractions