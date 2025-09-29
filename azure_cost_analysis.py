from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
import datetime
import pandas as pd

# 🔹 Your new service principal credentials
TENANT_ID = "5070ccf0-6440-4cfe-b8b1-8ddd2b6e2a71"
CLIENT_ID = "c95d9dbe-96de-4a8c-b826-f58858cabfa0"
CLIENT_SECRET = "SpY8Q~yH2h6WsJqrzfEsd81-XdNWrxgqiJKsmad0"
SUBSCRIPTION_ID = "e824989c-1016-4eb2-9ba0-12e8ad032bb6"

# Authenticate using service principal
credentials = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Initialize Cost Management client
client = CostManagementClient(credentials)

# Set time range (last 7 days)
today = datetime.date.today()
start_date = today - datetime.timedelta(days=7)

# Convert to full ISO 8601 datetime strings
start_date_str = start_date.strftime("%Y-%m-%dT00:00:00Z")
today_str = today.strftime("%Y-%m-%dT00:00:00Z")

# Prepare the query
scope = f"/subscriptions/{SUBSCRIPTION_ID}"  # must include leading slash
query = {
    "type": "Usage",
    "timeframe": "Custom",
    "timePeriod": {
        "from": start_date_str,
        "to": today_str
    },
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {"name": "PreTaxCost", "function": "Sum"}
        },
        "grouping": [{"type": "Dimension", "name": "ServiceName"}]
    }
}

# Run the query
result = client.query.usage(scope=scope, parameters=query)

# Convert result to dictionary
data = result.as_dict()
columns = [col['name'] for col in data.get('columns', [])]
rows = data.get('rows', [])

# Print results in a readable table
print(f"\nAzure Daily Cost Report ({start_date_str} to {today_str}):\n")

if not rows:
    print("⚠ No cost data available for this subscription in the given date range.")
else:
    print(" | ".join([col.ljust(25) for col in columns]))
    print("-" * (len(columns) * 28))

    for row in rows:
        print(" | ".join([str(item).ljust(25) for item in row]))

         

# Convert Azure rows + columns into a DataFrame
df_azure = pd.DataFrame(rows, columns=columns)

# Save to CSV
df_azure.to_csv("azure_cost.csv", index=False)
print("\nAzure data saved to azure_cost.csv ✅")