from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import ClientSecretCredential


def execute_pipeline(rg_name, df_name, p_name, params={}):
    subscription_id = ''
    client_id=''
    client_secret=''
    tenant_id=''

    credentials = ClientSecretCredential(tenant_id, client_id, client_secret)

    adf_client = DataFactoryManagementClient(credentials, subscription_id)

    rg_name = ""
    adf_name = ""
    pipe_name = ""
    pipe_params = {}

    adf_client.pipelines.create_run(rg_name, adf_name, pipe_name, parameters=pipe_params)
