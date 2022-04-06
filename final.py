import io

#Basic reading of lines in the text file
#TODO: take text and convert it into forms that can be placed in Python code
input_file = io.open("./input.txt", 'r')
code = io.open("./solution.py", 'w')

input_file.readline()
select_attrs = input_file.readline()

input_file.readline()
num_grouping_vars = input_file.readline()

input_file.readline()
grouping_attrs = input_file.readline()
grouping_attrs = grouping_attrs.split(",")

input_file.readline()
aggregate_vector = input_file.readline()
aggregate_vector = aggregate_vector.split(",")
#aggregate_vector[len(aggregate_vector)-1] = 

input_file.readline()
select_condition_vector = input_file.readline()

input_file.readline()
having_condition = input_file.readline()

#print(select_attrs)
#print(num_grouping_vars)
#print(grouping_attrs)
#print(aggregate_vector)
#print(select_condition_vector)
#print(having_condition)

#Imports needed for the solution
code.writelines("import psycopg2\nimport psycopg2.extras\n\n")

#Writing the aggregate structure
code.writelines("class AggStore:\n\tdef __init__(self):\n")
#Define attributes based on the aggregate_vector
for agg in aggregate_vector:
    code.writelines("\t\tself." + agg + " = None\n") #TODO: Need to remove the line break from the last value

code.writelines("\noutput = {}\n\n")
code.writelines("dbConnection = psycopg2.connect(dbname=\"postgres\", user=\"postgres\", password=\"password\", host=\"localhost\")\n")
code.writelines("dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)\n") #cursor_factory = psycopg2.extras.RealDictCursor allows you to get fields using field name as opposed to index number
code.writelines("dbCursor.execute(\"SELECT * FROM sales\")\n\n") #dbCursor now contains all the data from the table

#First loop
code.writelines("for record in dbCursor:\n")
code.writelines("\tgroupTuple = (")
for i in range(len(grouping_attrs)):
    code.writelines("record[\"" + grouping_attrs[i] + "\"]")
    if i != len(grouping_attrs) - 1:
        code.writelines(", ")
code.writelines(")\n")
code.writelines("\ttestIfThere = output.get(groupTuple)\n")
code.writelines("\tif testIfThere == None:\n")
code.writelines("\t\toutput[groupTuple] = AggStore()\n")


#...
#Close all the files
input_file.close()
code.close()
