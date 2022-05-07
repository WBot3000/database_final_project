import io

#Functions used within this program
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
    # Select Attributes will be stored in S as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    select_attrs = inputFile.readline()
    select_attrs = select_attrs.replace(' ', '')
    select_attrs = select_attrs.replace('\n', '')
    select_attrs = select_attrs.split(',')

    # Number of grouping variables will be stored in n as an int
    num_grouping_vars = inputFile.readline()
    num_grouping_vars = int(num_grouping_vars)

    # Grouping Variables will be stored in V as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    grouping_attrs = inputFile.readline()
    grouping_attrs = grouping_attrs.replace(' ', '')
    grouping_attrs = grouping_attrs.replace('\n', '')
    grouping_attrs = grouping_attrs.split(',')

    # F-Vects will be stored in F as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    # When these need to be converted into arrays, can iterate through list
    FTemp = inputFile.readline()
    FTemp = FTemp.replace(' ', '')
    FTemp = FTemp.replace('\n', '')
    FTemp = FTemp.split(',')

    aggregate_vector = []
    for i in range(num_grouping_vars+1): #Needs to be +1 to account for gv 0
        aggregate_vector.append([])
    for agg in FTemp:
        agg_type, gv, agg_attribute = agg_val_to_list(agg)
        gv = int(gv) #Turn gv into integer to be used as index
        aggregate_vector[gv].append(agg)
        
    # Select Condition Vects will be stored in th as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    # Within these conditions, AND and OR statements are replaced with @@ or ||, respectively
    select_condition_vector = inputFile.readline()
    select_condition_vector = select_condition_vector.replace(' and ', '@@')
    select_condition_vector = select_condition_vector.replace(' or ', '||')
    select_condition_vector = select_condition_vector.replace(' ', '')
    select_condition_vector = select_condition_vector.replace('@@', ' and ')
    select_condition_vector = select_condition_vector.replace('||', ' or ')
    select_condition_vector = select_condition_vector.replace('\n', '')
    select_condition_vector = select_condition_vector.split(',')
    select_condition_vector = ["True"] + select_condition_vector #Selection condition for g.v. 0

    # Having Conditions will be stored in G as a list of strings
    # Commas will separate them, spaces and newlines will be removed
    # Within these conditions, AND and OR statements are replaced with @@ or ||, respectively
    having_condition = inputFile.readline()
    having_condition = having_condition.replace(' and ', '@@')
    having_condition = having_condition.replace(' or ', '||')
    having_condition = having_condition.replace(' ', '')
    having_condition = having_condition.replace('@@', ' and ')
    having_condition = having_condition.replace('||', ' or ')
    having_condition = having_condition.replace('\n', '')
    having_condition = having_condition.split(',')

#Write to solution file
with open("./solution.py", 'w') as code:

    #Function for getting grouping tuple
    def get_grouping_tuple():
        code.writelines("groupTuple = (")
        for i in range(len(grouping_attrs)):
            code.writelines("record[\"" + grouping_attrs[i] + "\"]")
            if i != len(grouping_attrs) - 1:
                code.writelines(", ")
        code.writelines(")\n")
    
    #Imports needed for the solution
    code.writelines("import psycopg2\nimport psycopg2.extras\n\n")

    #Writing the aggregate structure
    code.writelines("class AggStore:\n\tdef __init__(self):\n")
    #Define attributes based on the aggregate_vector
    for agg in FTemp: #Uses FTemp for convenience since it's one dimensional
        code.writelines("\t\tself." + agg + " = None\n")
        

    code.writelines("\noutput = {}\n\n")
    code.writelines("dbConnection = psycopg2.connect(dbname=\"postgres\", user=\"postgres\", password=\"password\", host=\"localhost\")\n")
    code.writelines("dbCursor = dbConnection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)\n") #cursor_factory = psycopg2.extras.RealDictCursor allows you to get fields using field name as opposed to index number
    code.writelines("dbCursor.execute(\"SELECT * FROM sales\")\n\n") #dbCursor now contains all the data from the table

    #First loop
    code.writelines("for record in dbCursor:\n")
    code.writelines("\t")
    get_grouping_tuple()
    code.writelines("\ttestIfThere = output.get(groupTuple)\n")
    code.writelines("\tif testIfThere == None:\n")
    code.writelines("\t\toutput[groupTuple] = AggStore()\n")

    code.writelines("\n")

    var = 0

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
                if agg_type == "count":
                    #var = 1
                    #code.writelines("\t\t'Count Code'\n")
                    code.writelines("\t\t\tgroup." + agg + " = 1\n") #If value hasn't been set properly yet
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " += 1\n") #Add +1 to count if it has been set
                    #TODO: Count code goes here
                elif agg_type == "sum":
                    #var = 1
                    #code.writelines("\t\t'Sum Code'\n")
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n") #If value hasn't been set properly yet
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " += record[\"" + agg_attribute + "\"]\n") #Add +1 to count if it has been set
                    #TODO
                elif agg_type == "max":
                    #var = 1
                    #code.writelines("\t\t'Max Code'\n")
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " = min(group." + agg + ", record[\"" + agg_attribute + "\"])\n")
                    #TODO
                elif agg_type == "min":
                    #var = 1
                    #code.writelines("\t\t'Min Code'\n")
                    code.writelines("\t\t\tgroup." + agg + " = record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + " = min(group." + agg + ", record[\"" + agg_attribute + "\"])\n")
                    #TODO
                elif agg_type == "avg": #Average is stored as two index array, first index is sum, second is count. Average is then computed by dividing during printing
                    #var = 1
                    #code.writelines("\t\t'Avg Code'\n")
                    code.writelines("\t\t\tgroup." + agg + " = [record[\"" + agg_attribute + "\"], 1]\n")
                    code.writelines("\t\telse:\n")
                    code.writelines("\t\t\tgroup." + agg + "[0] += record[\"" + agg_attribute + "\"]\n")
                    code.writelines("\t\t\tgroup." + agg + "[1] += 1\n")
                    #TODO
            code.writelines("\n")
                
    



#Having loop, where the output will be filtered
#TODO
