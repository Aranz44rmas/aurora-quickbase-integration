# aurora-quickbase-integration
This repository contains an object-oriented Python script implementation for automated integration between the Aurora Solar API and the Quickbase API.

# 🌞 Aurora ⇨ Quickbase Integration

## 📘 Project Description
This project automates the transfer of solar design data from Aurora Solar to Quickbase.
It extracts the most recent design from a project in Aurora, takes key data (address, system size, production, etc.),
and automatically creates a new record in a Quickbase table.

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
Configure them in `config/config.json`:
- `tenant_id`
- `bearer_token`
- `project_ids`
- `auth`
- `table_id`

### Important: If you want to add a new project_id to test it, it must be added in the src/config/auth.json file 

## 📚 Dependencies
See `requirements.txt`.

## 📄 License
This project is part of a technical evaluation for Better Earth. Internal use only.
