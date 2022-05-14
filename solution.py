import psycopg2
import psycopg2.extras

class AggStore:
	def __init__(self):
		self.avg_1_quant = None
		self.avg_2_quant = None
		self.avg_3_quant = None

output = {}

dbConnection = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="localhost")
dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
dbCursor.execute("SELECT * FROM sales")

for record in dbCursor:
	groupTuple = (record["cust"], )
	testIfThere = output.get(groupTuple)
	if testIfThere == None:
		output[groupTuple] = AggStore()

dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (record["state"]=='NY'):
		groupTuple = (record["cust"], )
		group = output.get(groupTuple)
		if group.avg_1_quant == None:
			group.avg_1_quant = [record["quant"], 1]
		else:
			group.avg_1_quant[0] += record["quant"]
			group.avg_1_quant[1] += 1


dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (record["state"]=='NJ'):
		groupTuple = (record["cust"], )
		group = output.get(groupTuple)
		if group.avg_2_quant == None:
			group.avg_2_quant = [record["quant"], 1]
		else:
			group.avg_2_quant[0] += record["quant"]
			group.avg_2_quant[1] += 1


dbCursor.execute("SELECT * FROM sales")
for record in dbCursor:
	if (record["state"]=='CT'):
		groupTuple = (record["cust"], )
		group = output.get(groupTuple)
		if group.avg_3_quant == None:
			group.avg_3_quant = [record["quant"], 1]
		else:
			group.avg_3_quant[0] += record["quant"]
			group.avg_3_quant[1] += 1


for group_attrs, aggs in output.items():
	if(aggs.avg_1_quant[0]/aggs.avg_1_quant[1] > aggs.avg_2_quant[0]/aggs.avg_2_quant[1] and aggs.avg_1_quant[0]/aggs.avg_1_quant[1] > aggs.avg_3_quant[0]/aggs.avg_3_quant[1]):
		print('--------------------')
		print('cust: ', group_attrs[0])
		print('avg_1_quant: ', aggs.avg_1_quant[0]/aggs.avg_1_quant[1])
		print('avg_2_quant: ', aggs.avg_2_quant[0]/aggs.avg_2_quant[1])
		print('avg_3_quant: ', aggs.avg_3_quant[0]/aggs.avg_3_quant[1])
		print('--------------------')
