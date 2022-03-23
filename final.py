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


#This is a function I wrote to split up the grouping variable's name into components
def agg_val_to_list(agg_value):
    list = ["", "", ""]
    index = 0
    for char in agg_value:
        if char == '_':
            index += 1
        else:
            list[index] += char
    return list
    

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
        for i in mfStruct.agg_values: #Fill in the results list with 0s, the actual values being iterated through don't matter here
            #NOTE: Could do a conditional for avg that stores two 0s (one for sum and one for length)
            mfStruct.results[attrTuple].append(0)
"""

#Contains all the other loops
"""
for i in range(len(mfStruct.agg_values)): #Need the i to get the appropriate list value of C
    av_list = agg_val_to_list(mfStruct.agg_values[i])
    group_var = av_list[0]
    aggregate_type = av_list[1]
    field_to_aggregate = av_list[2]
    
    #Get all of the conditions for the grouping variable (group_var), probably using an external function on 

    dbCursor.execute("SELECT * FROM sales") #Re-fetch all the data from the database
    for record in dbCursor:

        #Check if the record satisfies all the condiitions listed above, if not, just go to next record
            #If it does match all the conditions (is part of the GV, add the code based on the second_part_of_agg thingy 
            
"""

#Loop for getting aggregate values (Will vary depending on aggregate value), this should be run after fetch has been performed
#TODO

#match second_part_of_agg:
    #case "count": #TODO
        #"""
            #Code that corresponds to count
        #"""
    #case "sum": #TODO
        #"""
            #Code that corresponds to sum
        #"""
    #case "min": #TODO
        #"""
            #Code that corresponds to min
        #"""
    #case "max": #TODO
        #"""
            #Code that corresponds to max
        #"""
    #case "avg": #TODO
        #"""
            #Code that corresponds to avg
        #"""

code.write("print(\"Hello World\")")
code.close()

print("Done")
