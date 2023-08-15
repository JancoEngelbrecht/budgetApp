from sqlalchemy import create_engine # Connection Bridge with SQL server
from sqlalchemy.engine import URL # Construct a connection string
from sqlalchemy import text 
import pypyodbc # connect to SQL server
import pandas as pd
import numpy as np

SERVER_NAME = 'DESKTOP-MBKO1DV'
DATABASE_NAME = 'budgetappdb'
TABLE_NAME = 'transactions'

connection_string = f"""
    DRIVER={{SQL Server}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""
 

connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string}) # query={'odbc_connect': connection_string} = A PyODBC connection string can also be sent in pyodbc's format directly 
engine = create_engine(connection_url, module=pypyodbc)  # module=pypyodbc keyword argument unique to dialect
connection = engine.connect()

# Connecting with SQLAlchemy Engin
query = (f"SELECT * FROM {TABLE_NAME}")
dataframe = pd.read_sql(query, engine)
print(dataframe)





# READ Excel Sheet. Each sheet will be a dictionary item.
# excel_file = pd.read_excel('budgetApp\static\XLS230701143346.xls', sheet_name=None)

# # REPLACE THE TEMP TABLE IN SQL SERVER
# # LOOP through Dic. Use .items() to select all the items in the Dic.(Sheet_name = Key , df_data = Value)
# for sheet_name, df_data in excel_file.items():
#     print(f'Loading worksheet {sheet_name}...')
#     df_data = pd.DataFrame(df_data)
#     df_data.rename(columns = {'mutationcode':'currancy','description':'descrip'}, inplace =True)
#     df_data.to_sql('temporary_table', engine, if_exists='replace', index=False)

# # INITIALIZE a Cursor
# cursor = con.cursor()

# # INSERT temp data into main table, with no duplicates
# cursor.execute(f""
#                INSERT INTO {TABLE_NAME}
#                 SELECT * FROM temporary_table
#                 WHERE NOT EXISTS (SELECT 1 FROM {TABLE_NAME}
#                 WHERE temporary_table.descrip = {TABLE_NAME}.descrip) "")

# cursor.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()

# # APPLY Modifications in SQL Server - Commit
# con.commit()

# # CLOSE the connection
# del con 

