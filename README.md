# aurora-quickbase-integration
This repository contains an object-oriented Python script implementation for automated integration between the Aurora Solar API and the Quickbase API.

# 🌞 Aurora ⇨ Quickbase Integration

## 📘 Project Description
This project automates the transfer of solar design and project data from the Aurora Solar API to the Quickbase API. It is designed to provide a robust and automated solution for synchronizing key information for solar projects.

The integration process begins with a Project ID which can be configured in the config/auth.json file. Each project in Aurora Solar can contain multiple designs, representing different solar system configurations or iterations for a single property. For each of these designs, the system identifies and extracts the most recent and relevant data.

Specifically, for a given Project ID:

* It retrieves all associated designs.
* For each design, it fetches the latest proposal, which contains crucial details like the proposal link.
* It extracts a summary of the design, including technical specifications such as system size, annual energy production, module type, module count, and array azimuth.
* It also retrieves the project's address details (street, city, state, postal code, country).

All this extracted data is then transformed into a Quickbase-compatible format and automatically used to create or update records in a specified Quickbase table, ensuring that your Quickbase database reflects the most current information from Aurora Solar.

## 📦 Repository Structure
```
aurora-quickbase-integration/
├── src/
│ ├── extractor.py
├── config/
│ └── auth.json
├── utils/
│ └── logger
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 How to use
```bash
# Install dependencies
pip install -r requirements.txt

# Run the main script
python main.py
```

## 🔑 Required variables
The config/auth.json file is used to define the project_ids to be processed and also contains tenant_id, bearer_token, auth (Quickbase user token), and table_id.

Configure them in `config/config.json`:
- `tenant_id`
- `bearer_token`
- `project_ids`
- `auth`
- `table_id`

Example config/auth.json structure:


{
  "tenant_id": "your_aurora_tenant_id", 
  "bearer_token": "your_aurora_bearer_token",
  "auth": "your_quickbase_user_token",
  "table_id": "your_quickbase_table_id",
  "project_ids": [
    {"id": "aurora_project_id_1", "label": "Project A"},
    {"id": "aurora_project_id_2", "label": "Project B"}
  ]
}
]

#### Important: If you want to add a new project_id to test, it must be added to the project_ids list within the config/auth.json file.

## 📚 Dependencies
See `requirements.txt`.

## 📄 License
This project is part of a technical evaluation for Better Earth. Internal use only.
