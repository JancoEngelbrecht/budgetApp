from sqlalchemy import create_engine # Connection Bridge with SQL server
from sqlalchemy.engine import URL # Construct a connection string
import pypyodbc # connect to SQL server
import pandas as pd

SERVER_NAME = 'DESKTOP-MBKO1DV'
DATABASE_NAME = 'budgetappdb'
TABLE_NAME = 'transactions'

connection_string = f"""
    DRIVER={{SQL Server}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""
# CONNECT to MicrosoftSQL Server Management Studio (mssql). 
connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
engine = create_engine(connection_url, module=pypyodbc)

# READ Excel Sheet. Each sheet will be a dictionary item.
excel_file = pd.read_excel('budgetApp\static\XLS230701143346.xls', sheet_name=None)


# LOOP through Dic. So we use .items() to select all the items in the Dic.
# sheet_name = Key , df_data = Value
for sheet_name, df_data in excel_file.items():
    print(f'Loading worksheet {sheet_name}...')
    df_data = pd.DataFrame(df_data)
    df_data.rename(columns = {'mutationcode':'currancy','description':'descrip'}, inplace =True)
    df_data.to_sql('temporary_table', engine, if_exists='replace', index=False)




conn = pypyodbc.connect (f"""
    DRIVER={{SQL Server}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;""")

df = pd.read_sql_query(f'''
                    UPDATE {TABLE_NAME} 
                    SET {TABLE_NAME}.
                    WHERE ''', conn)
print(df)



