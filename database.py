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
excel_file = pd.read_excel('budgetApp\data\input_transactions.xls', sheet_name=None)

# REPLACE THE TEMP TABLE IN SQL SERVER
# LOOP through Dic. Use .items() to select all the items in the Dic.(Sheet_name = Key , df_data = Value)
for sheet_name, df_exceldata in excel_file.items():
    print(f'Loading transactions {sheet_name}...')
    df_exceldata = pd.DataFrame(df_exceldata)
    df_exceldata.rename(columns = {'mutationcode':'currancy','description':'descrip'}, inplace =True) # Rename Columns
    df_exceldata.to_sql('temporary_table', engine, if_exists='replace', index=False) # Replace Temp Table in DB

shops_excel = pd.read_excel('budgetApp\data\shops.xls', sheet_name=None)

# APPEND DATA TO SHOPS TABLE IN SQL SERVER
# Clear the shops table in SQL server before running this code. 
# for sheet_name, df_shopdata in shops_excel.items():
#     print(f'Loading shops {sheet_name}...')
#     shops_excel = pd.DataFrame(df_shopdata)
#     df_shopdata.to_sql('shops', engine, if_exists='append', index=False)


# MERGE TEMP DATA WITH MAIN DATA TO ENSURE NO DUPLICATES
# Engine.begin() run and commit an transaction - "Begin transaction immediately"
with engine.begin() as connection: 
    connection.execute(text(f"""INSERT INTO {TABLE_NAME} 
                            SELECT * FROM temporary_table 
                            WHERE NOT EXISTS (SELECT 1 FROM {TABLE_NAME} 
                                              WHERE temporary_table.descrip = {TABLE_NAME}.descrip)""")) 
    

# CREATE PANDAS DATAFRAME OF MAIN TABLE AND FORMAT THE DATE COLUMNS
df_main = pd.read_sql(f'SELECT * FROM {TABLE_NAME}', engine)
df_main['valuedate'] = pd.to_datetime(df_main['valuedate'], format ='%Y%m%d')
df_main['transactiondate'] = pd.to_datetime(df_main['transactiondate'], format ='%Y%m%d')

# CREATE PANDAS DATAFRAME OF SHOPS TABLE AND CLEAN THE MAIN TABLE DESCRIPTIONS 
df_shops = pd.read_sql_table('shops', engine)
for row in df_shops['ID']:
    df_main.loc[df_main['descrip'].str.contains(row), 'descrip'] = row

# CREATE MAIN TABLE IN SQL
df_main.to_sql('main_table', engine, if_exists='replace', index=False)

# SELECT JOINED MAIN AND SHOP TABLE FOR EXPORT    
df_main = pd.read_sql(""" SELECT main_table.valuedate,main_table.amount, shops.Name ,shops.Category
                                FROM main_table
                                INNER JOIN shops
                                ON main_table.descrip = shops.ID""", engine)

# EXPORT JOINED MAIN AND SHOP TABLE
df_main.to_csv('budgetApp/data/export.csv')

print(df_main)


#empty the transactions table too, before executing the code.
