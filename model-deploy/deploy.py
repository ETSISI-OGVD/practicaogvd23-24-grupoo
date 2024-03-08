import argparse
import os
import json

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


    args = parser.parse_args()

    credentials = os.environ.get("credentials")
    if credentials is None:
        raise ValueError("Please set the credentials environment variable")
    credentials = json.loads(credentials)

    tenant_id = credentials["tenantId"]
    client_id = credentials["clientId"]
    client_secret = credentials["clientSecret"]
    
    credential = DefaultAzureCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )

    # create a client
    ml_client = MLClient(credential, args.subscription_id, args.resource_group, args.workspace_name)

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