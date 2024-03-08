import argparse
import os

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
)
from azure.identity import DefaultAzureCredential

def main():
    # read params
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--subscription-id", type=str, help="Subscription ID")
    parser.add_argument("--resource-group", type=str, help="Resource Group")
    parser.add_argument("--workspace-name", type=str, help="Workspace Name")
    parser.add_argument("--deployment-name", type=str, help="Deployment Name")
    parser.add_argument("--endpoint-name", type=str, help="Endpoint Name")
    parser.add_argument("--instance-type", type=str, help="Instace Type", default="Standard_DS2_v2")
    parser.add_argument("--instance-count", type=int, help="Instace Type", default=1)

    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    print("Subscription ID:", subscription_id)

    args = parser.parse_args()

    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=args.subscription_id,
        resource_group_name=args.resource_group,
        workspace_name=args.workspace_name,
    )

    latest_model_version = max(
        [int(m.version) for m in ml_client.models.list(name=args.model)]
    )
    model = ml_client.models.get(name=args.model, version=latest_model_version)

    print(f"Deploying version {latest_model_version}")

    endpoint = ManagedOnlineEndpoint(
        name=args.endpoint_name,
        description="Online endpoint",
        auth_mode="key",
    )

    endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint).result()

    print(f"Endpoint {endpoint.name} provisioning state: {endpoint.provisioning_state}")

    deployment = ManagedOnlineDeployment(
        name=args.deployment_name,
        endpoint_name=args.endpoint_name,
        model=model,
        instance_type=args.instance_type,
        instance_count=args.instance_count,
    )

    deployment = ml_client.begin_create_or_update(deployment).result()


if __name__ == "__main__":
    main()