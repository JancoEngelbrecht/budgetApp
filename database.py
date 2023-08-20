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



# READ Excel Sheet. Each sheet will be a dic item.
excel_file = pd.read_excel('budgetApp\static\XLS230701143346.xls', sheet_name=None)

# REPLACE THE TEMP TABLE IN SQL SERVER
# LOOP through Dic. Use .items() to select all the items in the Dic.(Sheet_name = Key , df_data = Value)
for sheet_name, df_exceldata in excel_file.items():
    print(f'Loading worksheet {sheet_name}...')
    df_exceldata = pd.DataFrame(df_exceldata)
    df_exceldata.rename(columns = {'mutationcode':'currancy','description':'descrip'}, inplace =True) # Rename Column
    df_exceldata.to_sql('temporary_table', engine, if_exists='replace', index=False) # Replace Temp Table in DB


# Engine.begin() run and commit an transaction - "Begin transaction immediately"
with engine.begin() as connection:  # Add Temp Table Data to Main Table
    connection.execute(text(f"""INSERT INTO {TABLE_NAME} 
                            SELECT * FROM temporary_table 
                            WHERE NOT EXISTS (SELECT 1 FROM {TABLE_NAME} 
                                              WHERE temporary_table.descrip = {TABLE_NAME}.descrip)""")) 
    


df_main = pd.read_sql(f'SELECT * FROM {TABLE_NAME}', engine)
df_main['valuedate'] = pd.to_datetime(df_main['valuedate'], format ='%Y%m%d')
df_main['transactiondate'] = pd.to_datetime(df_main['transactiondate'], format ='%Y%m%d')

df_shops = pd.read_sql_table('shop', engine)


for row in df_shops['desc_contains']:
    df_main.loc[df_main['descrip'].str.contains(row), 'descrip'] = row


df_main.to_csv('BudgetApp/data/export.csv')

print(df_main)

# albertheijn_df = df[df['descrip'].str.contains('|'.join(['ALBERT','AH to go']))]

# Engine.connect() pull data from the database - "Wait until statement is executed before beginning the transaction"
# with engine.connect() as connection:
#     table = connection.execute(text(f"SELECT * FROM {TABLE_NAME}"))
#     for row in table:
#         print(row.descrip)


