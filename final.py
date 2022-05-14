import io

#Converts an aggregate string (ex. sum_1_quant), into a list with 3 parts (ex. [sum, 1, quant])
def agg_val_to_list(agg_value):
    list = ["", "", ""]
    index = 0
    for char in agg_value:
        if char == '_':
            index += 1
        else:
            list[index] += char
    return list

#Basic reading of lines in the text file
with open("./input.txt", 'r') as inputFile:
    # Select Attributes will be stored in select_attrs as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    select_attrs = inputFile.readline()
    select_attrs = select_attrs.replace(' ', '')
    select_attrs = select_attrs.replace('\n', '')
    select_attrs = select_attrs.split(',')

    # Number of grouping variables will be stored in num_grouping_vars as an int
    num_grouping_vars = inputFile.readline()
    num_grouping_vars = int(num_grouping_vars)

    # Grouping Variables will be stored in grouping_attrs as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    grouping_attrs = inputFile.readline()
    grouping_attrs = grouping_attrs.replace(' ', '')
    grouping_attrs = grouping_attrs.replace('\n', '')
    grouping_attrs = grouping_attrs.split(',')

    # F-Vects will be stored in aggregate_vector as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    # When these need to be converted into arrays, can iterate through list

    #FTemp is a 1-D array of all the aggregates
    FTemp = inputFile.readline()
    FTemp = FTemp.replace(' ', '')
    FTemp = FTemp.replace('\n', '')
    FTemp = FTemp.split(',')

    #aggregate_vector is a 2-D array, index i corresponds to gv i
    aggregate_vector = []
    for i in range(num_grouping_vars+1): #Needs to be +1 to account for gv 0
        aggregate_vector.append([])
    for agg in FTemp:
        agg_type, gv, agg_attribute = agg_val_to_list(agg)
        #Turn gv into integer to be used as index
        gv = int(gv)
        aggregate_vector[gv].append(agg)
        
    # Select Condition Vects will be stored in select_condition_vector as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    select_condition_vector = inputFile.readline()
    select_condition_vector = select_condition_vector.replace(' and ', '@@')
    select_condition_vector = select_condition_vector.replace(' or ', '||')
    select_condition_vector = select_condition_vector.replace(' ', '')
    select_condition_vector = select_condition_vector.replace('@@', ' and ')
    select_condition_vector = select_condition_vector.replace('||', ' or ')
    select_condition_vector = select_condition_vector.replace('\n', '')
    select_condition_vector = select_condition_vector.split(',')
    #Selection condition for g.v. 0
    select_condition_vector = ["True"] + select_condition_vector

    # Having Conditions will be stored in G as a string
    # Newline will be removed
    having_condition = inputFile.readline()
    having_condition = having_condition.replace('\n', '')

#Write to solution file
with open("./solution.py", 'w') as code:

    #Function for getting grouping tuple based on grouping_attrs
    def get_grouping_tuple():
        code.writelines("groupTuple = (")
        for i in range(len(grouping_attrs)):
            code.writelines("record[\"" + grouping_attrs[i] + "\"]")
            code.writelines(", ")
        code.writelines(")\n")

    #Function to see if select attribute is a grouping attribute or aggregate for printing
    #Returns index value of grouping attribute if grouping attribute, returns -1 if it's an aggregate
    def is_grouping_attr(attr):
        for i in range(len(grouping_attrs)):
            if(attr == grouping_attrs[i]):
                return i
        return -1
    
    #Imports needed for the solution
    #psycopg2 is the module that the solution needs to communicate with the database
    #psycopg2.extras is the module that lets us reference database fields by name in the solution
    code.writelines("import psycopg2\nimport psycopg2.extras\n\n")

    #Writing the aggregate structure
    code.writelines("class AggStore:\n\tdef __init__(self):\n")
    #Define attributes based on the aggregate_vector
    for agg in FTemp: #Uses FTemp for convenience since it's one dimensional
        code.writelines("\t\tself." + agg + " = None\n")
        
    #Establish connection with the database and fetch the records for the first time
    code.writelines("\noutput = {}\n\n")
    code.writelines("dbConnection = psycopg2.connect(dbname=\"postgres\", user=\"postgres\", password=\"password\", host=\"localhost\")\n")
    code.writelines("dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)\n") #cursor_factory = psycopg2.extras.RealDictCursor allows you to get fields using field name as opposed to index number
    code.writelines("dbCursor.execute(\"SELECT * FROM sales\")\n\n") #dbCursor now contains all the data from the table

    #First loop that gets all of the groups
    code.writelines("for record in dbCursor:\n")
    code.writelines("\t")
    get_grouping_tuple()
    code.writelines("\ttestIfThere = output.get(groupTuple)\n")
    code.writelines("\tif testIfThere == None:\n")
    code.writelines("\t\toutput[groupTuple] = AggStore()\n")

    code.writelines("\n")

    for gv_idx in range(num_grouping_vars+1):
        aggregates = aggregate_vector[gv_idx]
        selection_conditions = select_condition_vector[gv_idx]
        if len(aggregates) > 0: #Don't do a loop if there's no aggregates
            code.writelines("dbCursor.execute(\"SELECT * FROM sales\")\n")
            code.writelines("for record in dbCursor:\n")
            code.writelines("\tif (" + selection_conditions + "):\n") #If selection conditions apply, do these things
            code.writelines("\t\t")
            get_grouping_tuple()
            code.writelines("\t\tgroup = output.get(groupTuple)\n")
            for agg in aggregates:
                agg_type, gv, agg_attribute = agg_val_to_list(agg)
                code.writelines("\t\tif group." + agg + " == None:\n")
                #Different code for different aggregate functions
                if agg_type == "count":
                    code.writelines("\t\t\tgroup." + agg + " = 1\n") #If value hasn't been set properly yet
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " += 1\n") #Add +1 to count if it has been set
                elif agg_type == "sum":
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n") #If value hasn't been set properly yet
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " += record[\"" + agg_attribute + "\"]\n") #Add +1 to count if it has been set
                elif agg_type == "max":
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " = min(group." + agg + ", record[\"" + agg_attribute + "\"])\n")
                elif agg_type == "min":
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " = min(group." + agg + ", record[\"" + agg_attribute + "\"])\n")
                elif agg_type == "avg": #Average is stored as two index array, first index is sum, second is count. Average is then computed by dividing during printing
                    code.writelines("\t\t\tgroup." + agg + " = [record[\"" + agg_attribute + "\"], 1]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + "[0] += record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\t\tgroup." + agg + "[1] += 1\n")
            code.writelines("\n\n")
                
    



#Having loop, where the output will be filtered
    code.writelines("for group_attrs, aggs in output.items():\n")
    code.writelines("\tif(" + having_condition + "):\n")
    code.writelines("\t\tprint('--------------------')\n")
    for attr in select_attrs:
        code.writelines("\t\tprint('" + attr + ": ', ")
        restOfLine = ""
        grIdx = is_grouping_attr(attr)
        if grIdx == -1:
            agg_type, gv, agg_attribute = agg_val_to_list(attr)
            if agg_type == "avg": #Special case for average, since it's stored as two values instead of one
                restOfLine = "aggs." + attr + "[0]/aggs." + attr + "[1]"
            else:
                restOfLine = "aggs." + attr
        else:
            restOfLine = "group_attrs[" + str(grIdx) + "]"
        code.writelines(restOfLine + ")\n")
    code.writelines("\t\tprint('--------------------')\n")
    
