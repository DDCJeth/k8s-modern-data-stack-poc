import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from metadata.generated.schema.entity.services.databaseService import DatabaseService
from metadata.generated.schema.api.services.ingestionPipelines.createIngestionPipeline import CreateIngestionPipelineRequest
from metadata.generated.schema.entity.services.ingestionPipelines.ingestionPipeline import PipelineType, AirflowConfig
from metadata.generated.schema.metadataIngestion.workflow import SourceConfig
from metadata.generated.schema.metadataIngestion.databaseServiceMetadataPipeline import DatabaseServiceMetadataPipeline
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import OpenMetadataConnection
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig
from metadata.ingestion.ometa.ometa_api import OpenMetadata

from config import hostPort, TOKEN

# --- 1. Configure OpenMetadata Connection ---
server_config = OpenMetadataConnection(
    hostPort=hostPort, 
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken=os.getenv("OM_JWT_TOKEN", "<YOUR_TOKEN_HERE>") 
    )
)
metadata = OpenMetadata(server_config)

def create_metadata_pipeline(service_name: str, schedule_interval: str = "0 0 * * *"):
    """
    Creates a metadata ingestion pipeline for a specific Database Service.
    """
    print(f"Fetching service '{service_name}' from OpenMetadata...")
    
    # 2. Fetch the existing Database Service
    service_entity = metadata.get_by_name(entity=DatabaseService, fqn=service_name)
    
    if not service_entity:
        print(f"  [Error] Could not find a Database Service named '{service_name}'")
        return

    # 3. Create the Service Reference
    service_ref = EntityReference(
        id=service_entity.id,
        type="databaseService",
        name=service_entity.name.root if hasattr(service_entity.name, 'root') else service_entity.name
    )

    # 4. Define the Extraction Configuration
    # This dictates what the ingestion agent will actually do
    source_config = SourceConfig(
        config=DatabaseServiceMetadataPipeline(
            markDeletedTables=True,
            includeViews=True,
            includeTags=True,
            includeStoredProcedures=True
        )
    )

    # 5. Build the Pipeline Request
    pipeline_name = f"{service_name}_metadata_extraction"
    
    request = CreateIngestionPipelineRequest(
        name=pipeline_name,
        displayName=f"{service_name.capitalize()} Metadata Extraction",
        description=f"Automated metadata extraction pipeline for {service_name}",
        pipelineType=PipelineType.metadata,
        sourceConfig=source_config,
        airflowConfig=AirflowConfig(scheduleInterval=schedule_interval),
        service=service_ref
    )

    # 6. Push to OpenMetadata
    try:
        pipeline_entity = metadata.create_or_update(request)
        print(f"  [Success] Created ingestion pipeline: {pipeline_entity.fullyQualifiedName.root}")
        
    except Exception as e:
        print(f"  [Error] Failed to create ingestion pipeline: {e}")

if __name__ == "__main__":
    # Replace "iceberg" with the Fully Qualified Name (FQN) of your service
    TARGET_SERVICE = "iceberg"
    
    # "0 0 * * *" runs the pipeline daily at midnight via cron syntax
    create_metadata_pipeline(TARGET_SERVICE, schedule_interval="0 0 * * *")