from azure.cosmos import CosmosClient
import os


# Initialize the Cosmos client
endpoint = os.environ.get('ACCOUNT_HOST')
key = os.environ.get('ACCOUNT_KEY')
client = CosmosClient(endpoint, key)

# Connect to the database and container
database_name = os.environ.get('COSMOS_DATABASE')
container_name = os.environ.get('COSMOS_CONTAINER')
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)


def data():
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return (items)


def get_customer_by_id(id):
    query = f"SELECT * FROM c WHERE c.id = '{id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if items:
        return items
    else:
        return "Customer not found"