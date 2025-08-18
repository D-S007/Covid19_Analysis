import matplotlib.pylab as plt
import seaborn as sns
plt.style.use('ggplot') #using style-sheet for matplotlib and seaborn style plots
pd.set_option('display.max_columns',200) #To "Expand the number of columns" that are shown when we display a different data frame in our notebook

# Always make a copy of the original DataFrame to avoid modifying it directly
df = pd.read_csv('')
df_modified = df.copy()

# Function to load a CSV file and print timing information
import pandas as pd
import time
def load_csv_with_timing(filepath):
    start = time.time()
    df = pd.read_csv(filepath)
    print("FILE LOADED! this operation took", time.time()-start, "seconds")
    print("Data shape: ", df.shape)
    return df

"""
start = time.time()
df = pd.read_csv('')
print("FILE LOADED! this operation took", time.time()-start, "seconds")
print("Data shape: ", df.shape)
"""

# Extracting data from a SQLite database
import pandas as pd
import sqlite3
## Creating database connection
conn = sqlite3.connect('../Data/Database/covid19.db')
## Checking tables present in the database
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
tables

for table in tables['name'] :
    print('-'*50,f'{table}','-'*50)
    print('Count of records: ', pd.read_sql(f"Select count(*) as count from {table}",conn)['count'].values[0])
    display(pd.read_sql(f"Select * from {table} limit 5",conn))


# ydata-profiling
from ydata_profiling import ProfileReport
profile_datasetName = ProfileReport(df_modified, title="Profiling Report [Name of the Dataset]")
## Save the profiling report to an HTML file
profile_datasetName.to_file("DatasetName_profiling_report.html")


#Ingestion script 
import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
logging.basicConfig(
    filename = 'logs/ingestion_db.log',
    level = logging.DEBUG,
    format = '%(asctime)s-%(levelname)s-%(message)s',
    filemode = "a" #append
)

engine = create_engine('sqlite:///data/database/databaseName.db') # Change 'databaseName.db' to your actual database name

def ingest_db(df, table_name, engine):
    '''This function ingests a DataFrame into the database.'''
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f'Table {table_name} ingested successfully.')
    except Exception as e:
        logging.error(f'Error ingesting table {table_name}: {e}')

def load_raw_data():
    '''This function loads the CSVs as dataframe and ingest into db'''
    start_time = time.time()
    try:
        for file in os.listdir('data/raw_data/'):
            if '.csv' in file:
                try:
                    df = pd.read_csv('data/raw_data/' + file)
                    logging.info(f'Ingesting {file} in db')
                    ingest_db(df, file[:-4], engine)  # removing last 4 characters (.csv)
                except Exception as e:
                    logging.error(f'Error processing {file}: {e}')
        end_time = time.time()
        total_time = (end_time - start_time) / 60  # Convert to minutes
        logging.info('All files ingested successfully')
        logging.info(f'Total time taken to ingest all files: {total_time} minutes')
    except Exception as e:
        logging.error(f'Error in load_raw_data: {e}')

if __name__ == "__main__":
    load_raw_data()
    logging.info('Ingestion process completed.')





# Post-installation requirements management
"""
Document the "ALL" installed versions post-installation using `pip freeze > requirements_ALL.txt` 
to lock in the versions for future use OR "ONLY" listed in requirements.txt 
using `pip list --format=freeze | grep -E '^(pandas|numpy|SQLAlchemy|mysql-connector-python|matplotlib|seaborn|jupyter|requests|ydata_profiling|scikit-learn|dash|plotly)==' > requirements_ONLY.txt` 
-> later Rename to `requirements.txt`, hence we get our final clean requirements.txt
"""

