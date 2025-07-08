# src/main.py

# Import necessary libraries
import json
import logging
import os
from dotenv import load_dotenv

# Import custom modules from the project structure
from src.aurora_extractor import AuroraProjectDataExtractor
from src.utils.logger import setup_logging # Importar la función de configuración de logging

# Configure logging at the application start
setup_logging()
logger = logging.getLogger(__name__)

 # Open the auth.json file in read mode with UTF-8 encoding and load the JSON content into a Python dictionary
base_src_path = os.path.dirname(__file__) 
auth_json_file_path = os.path.join(base_src_path, 'config', 'auth.json')

try:
  with open(auth_json_file_path, 'r', encoding='utf-8') as f_auth_json:
    config_data = json.load(f_auth_json)
    logger.info(f"✅ Auth data successfully loaded from src/config/auth.json: {auth_data}")
except FileNotFoundError:
  logger.warning(f"⚠️ Auth file not found at: {auth_json_file_path}")
except json.JSONDecodeError:
  logger.error(f"❌ File '{auth_json_file_path}' is not a valid JSON .")
except Exception as e:
  logger.error(f"❌ Error loading auth file: {e}")

# Set Authentication and Project Variables
tenant_id = config_data['tenant_id']
bearer_token = config_data['bearer_token']
auth = config_data['auth']
table_id = config_data['table_id']
project_ids = config_data['project_ids']

fields_to_return = [6,7,8,9,10,12,13,14,15,16,17,18,19]

# Execute post for every JSON project_id's

# Process each projectr project in project_ids:
for project in project_ids:
    project_id = project['id']
    label = project.get('label', project_id)
    print(f"\n🔄 Procesando {label} ({project_id})")

    # Initialize the extractor for the current project
    try:
        extractor = AuroraProjectDataExtractor(tenant_id, project_id, bearer_token)
        final_df = extractor.extract_all_data()

        if final_df.empty:
            print(f"⚠️ No data extracted for {label}. Skipping.")
            continue

        # Format and publish in Quickbase
        payload = extractor.format_for_quickbase(final_df, table_id, return_fields=fields_to_return)
        result = extractor.post_to_quickbase(payload, user_token=auth)

        if result:
            print(f"✅ Record updated for {label}")
            print(json.dumps(result, indent=4))
        else:
            print(f"❌ Quickbase Post Failed for {label}")

    except Exception as e:
        print(f"❌ Error handling {label}: {e}")
