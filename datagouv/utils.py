from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.api.services.createDatabaseService import CreateDatabaseServiceRequest

import os

def clean_connection_config(connection_dict):
    """
    Removes read-only 'supports...' flags from the connection config 
    that the API rejects during service creation.
    """
    if "config" in connection_dict:
        config = connection_dict["config"]
        keys_to_remove = [k for k in config.keys() if k.startswith("supports")]
        for key in keys_to_remove:
            config.pop(key, None)
    return connection_dict



def inject_secrets(service_name, connection_dict):
    """
    Replaces masked passwords with real secrets from the .env file.
    Expects environment variables formatted as: <SERVICE_NAME_UPPERCASE>_PASSWORD
    """
    if "config" in connection_dict and "authType" in connection_dict["config"]:
        auth_type = connection_dict["config"]["authType"]
        
        # Check if a password field exists and needs replacing
        if "password" in auth_type:
            # Clean up the service name (e.g., replace spaces/hyphens if needed)
            safe_name = service_name.replace("-", "_").replace(" ", "_").upper()
            env_var_name = f"{safe_name}_PASSWORD"
            
            real_password = os.getenv(env_var_name)
            
            if real_password:
                auth_type["password"] = real_password
                print(f"  [Info] Successfully injected secret from '{env_var_name}'")
            else:
                print(f"  [Warning] No secret found for '{env_var_name}' in .env file. Masked password sent.")
                
    return connection_dict



