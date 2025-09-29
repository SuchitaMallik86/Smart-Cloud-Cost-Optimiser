import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Page Config
st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")
st.title("🌥 Multi-Cloud(AWS + Azure) Cost Dashboard")

# Load CSVs 
aws_csv_path = r"C:/Users/suchi/aws_cost.csv"
azure_csv_path = r"C:/Users/suchi/azure_cost_analysis.csv"

try:
    aws_data = pd.read_csv(aws_csv_path)
except FileNotFoundError:
    aws_data = pd.DataFrame()

try:
    azure_data = pd.read_csv(azure_csv_path)
except FileNotFoundError:
    azure_data = pd.DataFrame()

# Data Cleaning 
if not aws_data.empty:
    aws_data["lineItem/UnblendedCost"] = pd.to_numeric(
        aws_data["lineItem/UnblendedCost"], errors="coerce"
    ).fillna(0)
else:
    aws_data = pd.DataFrame({
        "product/servicename": [
            "Amazon EC2","Amazon S3","AWS Lambda","AWS Glue","Amazon RDS",
            "Amazon DynamoDB","Amazon CloudWatch","Amazon VPC","Amazon KMS","Amazon CloudTrail"
        ],
        "lineItem/UnblendedCost": [0]*10
    })

if not azure_data.empty:
    azure_data["PreTaxCost"] = pd.to_numeric(
        azure_data["PreTaxCost"], errors="coerce"
    ).fillna(0)
else:
    azure_data = pd.DataFrame({
        "ServiceName": [
            "Azure Virtual Machines","Azure Storage","Azure SQL Database","Azure Functions",
            "Azure Kubernetes Service (AKS)","Azure App Service","Azure Cosmos DB",
            "Azure Virtual Network","Azure Key Vault","Azure Monitor"
        ],
        "PreTaxCost": [0]*10
    })

#  KPIs 
total_aws_cost = aws_data["lineItem/UnblendedCost"].sum()
total_azure_cost = azure_data["PreTaxCost"].sum()

kpi1, kpi2 = st.columns(2)
kpi1.metric("💰 Total AWS Cost", f"${total_aws_cost:,.2f}")
kpi2.metric("💰 Total Azure Cost", f"${total_azure_cost:,.2f}")

#  Chart Type Selection 
chart_type = st.radio("📊 Choose chart type:", ["Bar", "Pie"], horizontal=True)

#  Filters 
aws_services = st.multiselect(
    "Filter AWS Services:",
    options=aws_data["product/servicename"].unique(),
    default=aws_data["product/servicename"].unique()
)
azure_services = st.multiselect(
    "Filter Azure Services:",
    options=azure_data["ServiceName"].unique(),
    default=azure_data["ServiceName"].unique()
)

filtered_aws = aws_data[aws_data["product/servicename"].isin(aws_services)]
filtered_azure = azure_data[azure_data["ServiceName"].isin(azure_services)]

# Layout (2 Columns for AWS & Azure) 
col1, col2 = st.columns(2)

# AWS Costs 
with col1:
    st.subheader("AWS Service Costs")
    if not filtered_aws.empty:
        if chart_type == "Bar":
            fig1, ax1 = plt.subplots(figsize=(6, 5))
            filtered_aws.groupby("product/servicename")["lineItem/UnblendedCost"].sum().sort_values().plot(
                kind="barh", ax=ax1, color="skyblue"
            )
            ax1.set_xlabel("Cost (USD)")
            st.pyplot(fig1)
        else:
            fig1, ax1 = plt.subplots()
            aws_grouped = filtered_aws.groupby("product/servicename")["lineItem/UnblendedCost"].sum().fillna(0)
            if aws_grouped.sum() > 0:
                aws_grouped.plot(kind="pie", autopct="%1.1f%%", ax=ax1, ylabel="", cmap="Blues")
                st.pyplot(fig1)
            else:
                st.info("No AWS cost data available for pie chart.")
    else:
        st.warning("No AWS services selected.")

# Azure Costs 
with col2:
    st.subheader("Azure Service Costs")
    if not filtered_azure.empty:
        if chart_type == "Bar":
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            filtered_azure.groupby("ServiceName")["PreTaxCost"].sum().sort_values().plot(
                kind="barh", ax=ax2, color="orange"
            )
            ax2.set_xlabel("Cost (USD)")
            st.pyplot(fig2)
        else:
            fig2, ax2 = plt.subplots()
            azure_grouped = filtered_azure.groupby("ServiceName")["PreTaxCost"].sum().fillna(0)
            if azure_grouped.sum() > 0:
                azure_grouped.plot(kind="pie", autopct="%1.1f%%", ax=ax2, ylabel="", cmap="Oranges")
                st.pyplot(fig2)
            else:
                st.info("No Azure cost data available for pie chart.")
    else:
        st.warning("No Azure services selected.")

# AWS vs Azure Comparison 
st.subheader("📈 AWS vs Azure Total Cost Comparison")
comparison_df = pd.DataFrame({
    "AWS": [total_aws_cost],
    "Azure": [total_azure_cost]
})
st.bar_chart(comparison_df.T)

#  Expandable Data Tables 
with st.expander("🔎 Show AWS Cost Details"):
    st.dataframe(filtered_aws)

with st.expander("🔎 Show Azure Cost Details"):
    st.dataframe(filtered_azure)

#  Download Buttons 
dl1, dl2 = st.columns(2)
with dl1:
    st.download_button(
        "⬇ Download AWS Data",
        filtered_aws.to_csv(index=False),
        "aws_filtered.csv",
        "text/csv"
    )
with dl2:
    st.download_button(
        "⬇ Download Azure Data",
        filtered_azure.to_csv(index=False),
        "azure_filtered.csv",
        "text/csv"
    )

    # ====== THE END(●'◡'●) ======