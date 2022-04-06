import psycopg2
import psycopg2.extras

class AggStore:
	def __init__(self):
		self.sum_1_quant = None
		self.avg_1_quant = None
		self.sum_2_quant = None
		self.sum_3_quant = None
		self.avg_3_quant
 = None

output = {}

dbConnection = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="localhost")
dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
dbCursor.execute("SELECT * FROM sales")

for record in dbCursor:
	groupTuple = (record["cust"], record["prod
"])
	testIfThere = output.get(groupTuple)
	if testIfThere == None:
		output[groupTuple] = AggStore()
