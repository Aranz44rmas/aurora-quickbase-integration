import json
import logging
import os
from dotenv import load_dotenv
from src.aurora_extractor import AuroraProjectDataExtractor
from src.utils.logger import setup_logging # Importar la función de configuración de logging

# Configurar logging al inicio de la aplicación
setup_logging()
logger = logging.getLogger(__name__)

base_src_path = os.path.dirname(__file__) # Esto es 'src/'
auth_json_file_path = os.path.join(base_src_path, 'config', 'auth.json')
try:
  with open(auth_json_file_path, 'r', encoding='utf-8') as f_auth_json:
    config_data = json.load(f_auth_json)
    logger.info(f"✅ Datos de autenticación cargados exitosamente desde src/config/auth.json: {auth_data}")
except FileNotFoundError:
  logger.warning(f"⚠️ El archivo de autenticación no se encontró en: {auth_json_file_path}")
except json.JSONDecodeError:
  logger.error(f"❌ El archivo '{auth_json_file_path}' no es un JSON válido.")
except Exception as e:
  logger.error(f"❌ Error al cargar el archivo de autenticación: {e}")


tenant_id = config_data['tenant_id']
bearer_token = config_data['bearer_token']
auth = config_data['auth']
table_id = config_data['table_id']
project_ids = config_data['project_ids']

fields_to_return = [6,7,8,9,10,12,13,14,15,16,17,18,19]

# Ejecutar publicación para cada proyecto
for project in project_ids:
    project_id = project['id']
    label = project.get('label', project_id)
    print(f"\n🔄 Procesando {label} ({project_id})")

    try:
        extractor = AuroraProjectDataExtractor(tenant_id, project_id, bearer_token)
        final_df = extractor.extract_all_data()

        if final_df.empty:
            print(f"⚠️ No data extracted for {label}. Skipping.")
            continue

        payload = extractor.format_for_quickbase(final_df, table_id, return_fields=fields_to_return)
        result = extractor.post_to_quickbase(payload, user_token=auth)

        if result:
            print(f"✅ Record updated for {label}")
            print(json.dumps(result, indent=4))
        else:
            print(f"❌ Quickbase Post Failed for {label}")

    except Exception as e:
        print(f"❌ Error handling {label}: {e}")
