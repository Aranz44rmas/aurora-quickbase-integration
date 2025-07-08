# src/aurora_extractor.py

import pandas as pd
import requests
import json
import logging

# Configuración básica de logging
logger = logging.getLogger(__name__)

class AuroraProjectDataExtractor:
    def __init__(self, tenant_id, project_id, bearer_token):
        self.tenant_id = tenant_id
        self.project_id = project_id
        self.bearer_token = bearer_token
        self.base_url = "https://api-sandbox.aurorasolar.com"

    def get_json_with_bearer(self, url):
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.bearer_token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_designs(self):
        url = f"{self.base_url}/tenants/{self.tenant_id}/projects/{self.project_id}/designs"
        data = self.get_json_with_bearer(url)
        designs = pd.json_normalize(data['designs'])[['id','name', 'system_size_stc']]
        return designs.rename(columns={'id':'design_id', 'name':'6', 'system_size_stc':'7'})

    def get_latest_proposal(self, design_id):
        url = f"{self.base_url}/tenants/{self.tenant_id}/designs/{design_id}/proposals/default"
        data = self.get_json_with_bearer(url)
        proposal = pd.json_normalize(data['proposal'])[['updated_at', 'proposal_link']]
        proposal = proposal.sort_values(by='updated_at', ascending=False).head(1)
        return proposal.rename(columns={'proposal_link':'19'})

    def get_summary(self, design_id):
        url = f"{self.base_url}/tenants/{self.tenant_id}/designs/{design_id}/summary"
        data = self.get_json_with_bearer(url)
        summary = pd.json_normalize(data['design'])[['arrays', 'energy_production.annual']]
        arrays = pd.json_normalize(summary['arrays'])
        summary2 = pd.json_normalize(arrays.iloc[0])[['azimuth', 'module.name', 'module.count']]
        summary = summary.drop(columns='arrays').join(summary2)
        return summary.rename(columns={
            'energy_production.annual': '10',
            'azimuth': '18',
            'module.name': '9',
            'module.count': '8'
        })

    def get_address(self):
        us_states = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'DC': 'District of Columbia',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming'}
        
        url = f"{self.base_url}/tenants/{self.tenant_id}/projects/{self.project_id}"
        data = self.get_json_with_bearer(url)
    
        address_df = pd.json_normalize(data['project'])[
            [
                #'location.property_address',
                'location.property_address_components.street_address',
                'location.property_address_components.city',
                'location.property_address_components.region',
                'location.property_address_components.postal_code',
                'location.property_address_components.country'
            ]
        ].rename(columns={
            #'location.property_address': '11',
            'location.property_address_components.street_address': '12',
            'location.property_address_components.city': '14',
            'location.property_address_components.region': '15',
            'location.property_address_components.postal_code': '16',
            'location.property_address_components.country': '17'
        })
        
        address_df['13'] = '' 
        #address_df['13'] = address_df['12'] #copy the same street
        address_df['15'] = address_df['15'].apply(lambda x: us_states.get(x, x))  # usa abreviatura si existe
        return address_df

    def extract_all_data(self):
        designs = self.get_designs()
        address = self.get_address()
        results = []

        for _, row in designs.iterrows():
            design_id = row['design_id']
            print(f"Design_Id: {design_id}")

            proposal = self.get_latest_proposal(design_id)
            summary = self.get_summary(design_id)

            result = proposal.join(pd.DataFrame([row])).join(summary).join(address)
            result = result.drop(columns=['design_id', 'updated_at'])[['6','7','8','9','10','12','13','14','15','16','17','18','19']]
            results.append(result)

        return pd.concat(results, ignore_index=True)

    def format_for_quickbase(self, df: pd.DataFrame, table_id: str, return_fields: list = None):
        formatted_data = []
    
        for _, row in df.iterrows():
            entry = {}
            for col in df.columns:
                if str(col) == "9":
                    # Valor fijo como texto (no lista)
                    entry[str(col)] = {"value": "Q.PEAK DUO BLK ML-G10+ 400"}
                else:
                    entry[str(col)] = {"value": row[col]}
            formatted_data.append(entry)
    
        payload = {
            "to": table_id,
            "data": formatted_data
        }
    
        if return_fields:
            payload["fieldsToReturn"] = return_fields
    
        return payload


    def post_to_quickbase(self, payload: dict, user_token: str):
        headers = {
            'Content-Type': 'application/json',
            "QB-Realm-Hostname": "betterearthsolar.quickbase.com",
            'Authorization': f'QB-USER-TOKEN {user_token}'
        }
        try:
            response = requests.post(
                'https://api.quickbase.com/v1/records',
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            print("✅ Successful record in Quickbase.")
            #print(json.dumps(response.json(), indent=4))
            return response.json()
        except requests.RequestException as e:
            print("❌ Error posting on Quickbase:")
            print(e)
            if response.content:
                print("Server Answer:")
                #print(response.text)
            return None
