import boto3
import pandas as pd
import gzip
import io

s3 = boto3.client('s3')

bucket_name = "billing-data86"
file_key = "cost-usage-report86/smart_cost_saver/20250801-20250901/smart_cost_saver-00001.csv.gz"

obj = s3.get_object(Bucket=bucket_name, Key=file_key)

with gzip.GzipFile(fileobj=obj['Body']) as gz:
    df = pd.read_csv(gz)

print(df.head())
print("\nTotal rows:", len(df))
print("\nColumns in CUR file:\n",df.columns.tolist())

# Select only relevant columns if they exist
relevant_columns = [
    "lineItem_UsageStartDate",
    "lineItem_ProductCode",
    "lineItem_UsageType",
    "lineItem_Operation",
    "lineItem_UnblendedCost"
]

available_columns = [col for col in relevant_columns if col in df.columns]
df_filtered = df[available_columns]

print("\nFiltered Data:\n", df_filtered.head())

print(df.columns.tolist())

df_grouped = df.groupby("product/servicename")["lineItem/UnblendedCost"].sum().reset_index()
print(df_grouped.sort_values(by="lineItem/UnblendedCost", ascending=False).head(10))

import matplotlib.pyplot as plt

# Sort services by cost (descending) and take top 10
df_grouped = df.groupby("product/servicename")["lineItem/UnblendedCost"].sum().reset_index()
df_top10 = df_grouped.sort_values(by="lineItem/UnblendedCost", ascending=False).head(10)

# Plot
plt.figure(figsize=(10,6))
bars = plt.bar(df_top10["product/servicename"], df_top10["lineItem/UnblendedCost"], color="skyblue")

plt.title("Top 10 AWS Services by Cost", fontsize=14, fontweight="bold")
plt.xlabel("Service", fontsize=12)
plt.ylabel("Cost (Unblended)", fontsize=12)
plt.xticks(rotation=45, ha="right")

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:.6f}", 
             ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.show()

df_grouped.to_csv("aws_cost.csv",index=False)
print(df.columns.tolist())