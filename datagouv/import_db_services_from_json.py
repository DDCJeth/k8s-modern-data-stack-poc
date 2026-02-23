import os
import json
import glob
from dotenv import load_dotenv  
from config import hostPort, TOKEN
from utils import clean_connection_config, inject_secrets
# --- Load Environment Variables ---
load_dotenv()  

from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.api.services.createDatabaseService import CreateDatabaseServiceRequest


# --- 1. Configure OpenMetadata Connection ---
server_config = OpenMetadataConnection(
    hostPort=hostPort, 
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken=os.getenv("OM_JWT_TOKEN", "<FALLBACK_TOKEN_IF_NEEDED>") 
    )
)

metadata = OpenMetadata(server_config)


def process_service_files(directory_path):
    """
    Reads all JSON files, cleans them, injects secrets from .env, 
    and creates services in OpenMetadata.
    """
    search_pattern = os.path.join(directory_path, '*.json')
    json_files = glob.glob(search_pattern)

    if not json_files:
        print(f"No JSON files found in {directory_path}")
        exit(0)

    print(f"Found {len(json_files)} JSON files. Starting import...")

    for file_path in json_files:
        print(f"\nProcessing {file_path}...")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            name = data.get("name")
            service_type = data.get("serviceType")
            description = data.get("description", "")
            connection = data.get("connection", {})

            if not name or not service_type:
                print(f"  [Skipped] Missing required 'name' or 'serviceType' in {file_path}")
                continue

            clean_connection = clean_connection_config(connection)
            secure_connection = inject_secrets(name, clean_connection)

            request = CreateDatabaseServiceRequest(
                name=name,
                serviceType=service_type,
                description=description,
                connection=secure_connection
            )

            service_entity = metadata.create_or_update(request)
            print(f"  [Success] Created/Updated service: {service_entity.fullyQualifiedName.root}")

        except Exception as e:
            print(f"  [Error] Failed to process {file_path}: {e}")


if __name__ == "__main__":
    CONFIG_DIRECTORY = "./service_configs" 
    process_service_files(CONFIG_DIRECTORY)