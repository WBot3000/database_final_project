import io

code = io.open("./solution.py", 'w')

#This is the code that will go into every solution, no matter what the input
"""
import psycopg2

class MFStructure:
    def __init__(self, group_fields, agg_values):
        self.group_fields = group_fields
        self.agg_values = agg_values
        self.results = {}

# More code for the structure here...

#Declare the structure based on the input
mfStruct = MFStructure(A, B, C) #A, B, and C should be based on the input

dbConnection = psycopg2.connect(dbname="postgres",
                                user="postgres",
                                password="password",
                                host="localhost")

dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) #cursor_factory = psycopg2.extras.RealDictCursor allows you to get fields using field name as opposed to index number

dbCursor.execute("SELECT * FROM sales") #dbCursor now contains all the data from the table
"""

#First loop (The loop that gathers all the attribute)
"""
for record in dbCursor: #Get the grouping tuple
    attrList = []
    for field in mfStruct.group_fields:
        attrList.append(record[field]) #Append the record to the list
    attrTuple = tuple(attrList) #Turn list into tupple
    record = mfStruct.results.get(attrTuple)
    if(record == None): #Group is not in the results set yet, add it
        mfStruct.results[attrTuple] = []
        for i in mfStruct.agg_values: #Fill in the results list with 0s
            mfStruct.results[attrTuple].append(0)
"""

#Loop for getting aggregate values (Will vary depending on aggregate value)
#TODO

code.write("print(\"Hello World\")")
code.close()

print("Done")
