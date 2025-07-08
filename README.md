# aurora-quickbase-integration
This repository contains an object-oriented Python script implementation for automated integration between the Aurora Solar API and the Quickbase API. 

# 🌞 Aurora ⇨ Quickbase Integration

## 📘 Descripción del proyecto
Este proyecto automatiza la transferencia de datos de diseños solares desde Aurora Solar a Quickbase.
Extrae el diseño más reciente de un proyecto en Aurora, toma datos clave (dirección, tamaño del sistema, producción, etc.)
y crea un nuevo registro automáticamente en una tabla de Quickbase.

## 📦 Estructura del repositorio
```
aurora-quickbase-integration/
├── src/
│   ├── extractor.py
│   └── config_loader.py
├── config/
│   └── config.json
├── logs/
│   └── aurora_quickbase.log
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Cómo usar
```bash
# Instala dependencias
pip install -r requirements.txt

# Ejecuta el script principal
python main.py
```

## 🔑 Variables necesarias
Configúralas en `config/config.json`:
- `tenant_id`
- `bearer_token`
- `project_ids`
- `auth`
- `table_id`

## 📚 Dependencias
Ver `requirements.txt`.

## 📄 Licencia
Este proyecto es parte de una evaluación técnica para Better Earth. Uso interno solamente.
"""

REQUIREMENTS_TXT = """
pandas
requests
"""

MAIN_PY = """
from src.extractor import AuroraProjectDataExtractor
from src.config_loader import load_config
import json

def main():
    config = load_config("config/config.json")
    tenant_id = config['tenant_id']
    bearer_token = config['bearer_token']
    auth = config['auth']
    table_id = config['table_id']
    project_ids = config['project_ids']
    fields_to_return = [6,7,8,9,10,12,13,14,15,16,17,18,19]

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

if __name__ == "__main__":
    main()
"""

files = {
  "README.md": README_CONTENT,
  "requirements.txt": REQUIREMENTS_TXT,
  "main.py": MAIN_PY
}

output = "\n\n".join([f"# {filename}\n\n{content}" for filename, content in files.items()])
print(output)
