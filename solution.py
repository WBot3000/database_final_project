import psycopg2
import psycopg2.extras

class AggStore:
	def __init__(self):
		self.sum_1_quant = None
		self.avg_1_quant = None
		self.sum_2_quant = None
		self.sum_3_quant = None
		self.avg_3_quant = None

output = {}

dbConnection = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="localhost")
dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
dbCursor.execute("SELECT * FROM sales")

for record in dbCursor:
	groupTuple = (record["cust"])
	testIfThere = output.get(groupTuple)
	if testIfThere == None:
		output[groupTuple] = AggStore()

dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (1.cust=cust and 1.state='NY'):
		groupTuple = (record["cust"])
		group = output.get(groupTuple)
		if group.sum_1_quant == None:
			group.sum_1_quant = record["quant"]
		else:
			group.sum_1_quant += record["quant"]
		if group.avg_1_quant == None:
			group.avg_1_quant = [record["quant"], 1]
		else:
			group.avg_1_quant[0] += record["quant"]
			group.avg_1_quant[1] += 1

dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (2.cust=cust and 2.state='NJ'):
		groupTuple = (record["cust"])
		group = output.get(groupTuple)
		if group.sum_2_quant == None:
			group.sum_2_quant = record["quant"]
		else:
			group.sum_2_quant += record["quant"]

dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (3.cust=cust and 3.state='CT'):
		groupTuple = (record["cust"])
		group = output.get(groupTuple)
		if group.sum_3_quant == None:
			group.sum_3_quant = record["quant"]
		else:
			group.sum_3_quant += record["quant"]
		if group.avg_3_quant == None:
			group.avg_3_quant = [record["quant"], 1]
		else:
			group.avg_3_quant[0] += record["quant"]
			group.avg_3_quant[1] += 1

