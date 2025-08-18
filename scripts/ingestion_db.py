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

engine = create_engine('sqlite:///data/database/covid.db') # Change 'databaseName.db' to your actual database name

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

