import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(
    filename="data_cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Started Data Cleaning Process.")

# List of raw data files to clean
raw_data_files = [
    "raw_telegram_data/DoctorsET_messages.json",
    "raw_telegram_data/EAHCI_messages.json",
    "raw_telegram_data/lobelia4cosmetics_messages.json",
    "raw_telegram_data/yetenaweg_messages.json"
]

# Output directory for cleaned data
cleaned_data_dir = "cleaned_data"
os.makedirs(cleaned_data_dir, exist_ok=True)

def clean_data(file_path):
    """Clean a single JSON file."""
    try:
        # Load raw data
        df = pd.read_json(file_path)

        # Debug: Print column names to verify structure
        print(f"Processing file: {file_path}")
        print("Columns in the DataFrame:", df.columns)

        # Check if 'id' column exists
        if 'id' not in df.columns:
            raise KeyError(f"The 'id' column is missing from the file: {file_path}")

        # 1. Remove Duplicates
        df_cleaned = df.drop_duplicates(subset=['id'], keep='last')
        logging.info(f"[{file_path}] Removed duplicates. Remaining rows: {len(df_cleaned)}")

        # 2. Handle Missing Values
        df_cleaned = df_cleaned.dropna(subset=['message', 'date'])
        logging.info(f"[{file_path}] Handled missing values. Remaining rows: {len(df_cleaned)}")

        # 3. Standardize Formats
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')
        logging.info(f"[{file_path}] Standardized date formats.")

        # 4. Data Validation
        if df_cleaned['id'].is_unique:
            logging.info(f"[{file_path}] Data validation successful: IDs are unique.")
        else:
            logging.error(f"[{file_path}] Data validation failed: IDs are not unique.")
            raise ValueError(f"Data contains non-unique IDs in file: {file_path}")

        # 5. Storing Cleaned Data
        cleaned_file_name = os.path.splitext(os.path.basename(file_path))[0] + "_cleaned.json"
        cleaned_data_path = os.path.join(cleaned_data_dir, cleaned_file_name)
        df_cleaned.to_json(cleaned_data_path, orient='records', lines=True)
        logging.info(f"[{file_path}] Cleaned data stored at: {cleaned_data_path}")

        print(f"Successfully cleaned data for file: {file_path}")
    
    except KeyError as e:
        logging.error(f"KeyError in file {file_path}: {e}")
        print(f"Error: {e}")

    except ValueError as e:
        logging.error(f"ValueError in file {file_path}: {e}")
        print(f"Error: {e}")

    except Exception as e:
        logging.error(f"An unexpected error occurred in file {file_path}: {e}")
        print(f"An unexpected error occurred in file {file_path}: {e}")

# Process each file
for file in raw_data_files:
    clean_data(file)

logging.info("Data Cleaning Process for all files completed successfully.")
