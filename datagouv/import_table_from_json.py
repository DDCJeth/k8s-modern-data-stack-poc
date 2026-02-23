import json
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.entity.data.table import Column, TableType
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from config import hostPort, TOKEN
# --- Configuration ---
server_config = OpenMetadataConnection(
    hostPort=hostPort,
    authProvider="openmetadata", # Change if using SSO (google, okta, etc.)
    securityConfig={"jwtToken": TOKEN}
)

metadata = OpenMetadata(server_config)

def create_table_from_json(json_path):
    # 1. Load the raw JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 2. Build Column Objects
    columns = []
    for col in data["columns"]:
        columns.append(
            Column(
                name=col["name"],
                dataType=col["dataType"],
                dataLength=col.get("dataLength"),
                dataTypeDisplay=col["dataTypeDisplay"],
                description=col.get("description"),
                tags=col.get("tags"),
                # Handle decimal precision/scale
                precision=col.get("precision"),
                scale=col.get("scale")
            )
        )

    # 3. Define the CreateTableRequest
    # Note: databaseSchema must be the Fully Qualified Name (FQN)
    table_request = CreateTableRequest(
        name=data["name"],
        displayName=data.get("displayName", data["name"]),
        description=data.get("description"),
        tableType=TableType.Regular,
        columns=columns,
        databaseSchema=data["databaseSchema"]["fullyQualifiedName"]
    )

    # 4. Create or Update the table
    created_table = metadata.create_or_update(table_request)
    
    if created_table:
        print(f"Table '{created_table.fullyQualifiedName}' successfully created/updated.")
    else:
        print("Failed to create table.")

if __name__ == "__main__":
    CONFIG_DIRECTORY = "datagouv/tables"
    TABLE_NAME = "iceberg_iceberg_gold_data_daily_tower_kpis.json"
    create_table_from_json(f"{CONFIG_DIRECTORY}/{TABLE_NAME}")
    # Alternatively, to process all JSON files in the directory:
    # for filename in os.listdir(CONFIG_DIRECTORY):
    #     if filename.endswith(".json"):
    #         create_table_from_json(os.path.join(CONFIG_DIRECTORY, filename))
