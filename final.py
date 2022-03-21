import io

code = io.open("./solution.py", 'w')

#This is the code that will go into every solution, no matter what the input
"""
import psycopg2

class MFStructure:
    def __init__(self, 
"""

code.write("print(\"Hello World\")")
code.close()
print("Done")
