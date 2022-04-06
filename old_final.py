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
    resultList = mfStruct.results.get(attrTuple)
    if(resultList == None): #Group is not in the results set yet, add it
        mfStruct.results[attrTuple] = []
        for i in mfStruct.agg_values: #Fill in the results list with Nones, the actual values being iterated through don't matter here
            mfStruct.results[attrTuple].append(None)
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

        #Check if the record satisfies all the condiitions listed above, if not, just go to next record (this is where group_var comes into play
            #If it does match all the conditions (is part of the GV, add the code based on the second_part_of_agg thingy
                attrList = []
                for field in mfStruct.group_fields:
                    attrList.append(record[field]) #Append the record to the list
                attrTuple = tuple(attrList) #Turn list into tupple
                resultList = mfStruct.results.get(attrTuple)
            
"""

#Loop for getting aggregate values (Will vary depending on aggregate value), this should be run after fetch has been performed
#TODO

#match aggregate_type:
    #case "count": #TODO
        #Code that corresponds to count
        """
        if resultList[i] == None:
            resultList[i] = 1
        else:
            resultList[i] += 1
        """
    #case "sum": #TODO
        #Code that corresponds to sum
        """
        if resultList[i] == None:
            resultList[i] = record[field_to_aggregate]
        else:
            resultList[i] += record[field_to_aggregate]
        """
    #case "min": #TODO
        #Code that corresponds to min
        """
        if resultList[i] == None:
            resultList[i] = record[field_to_aggregate]
        else:
            if resultList[i] > record[field_to_aggregate]:
                resultList[i] = record[field_to_aggregate]
        """
    #case "max": #TODO
        #Code that corresponds to max
        """
        if resultList[i] == None:
            resultList[i] = record[field_to_aggregate]
        else:
            if resultList[i] < record[field_to_aggregate]:
                resultList[i] = record[field_to_aggregate]
        """
    #case "avg": #TODO
        #Code that corresponds to avg
        """
        if resultList[i] == None: #Store two values, sum and length, do the calculation when it's printing
            resultList[i] = [record[field_to_aggregate], 1]
        else:
            resultList[i][0] += record[field_to_aggregate]
            resultList[i][1] += 1
        """

code.write("print(\"Hello World\")")
code.close()

print("Done")
