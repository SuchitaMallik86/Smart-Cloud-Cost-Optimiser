# Smart-Cloud-Cost-Optimiser
This project is a Cloud Cost Optimization Dashboard built using Python and Streamlit, which helps monitor and compare expenses across AWS and Azure services. It collects billing data, processes it with Pandas, and visualizes costs through interactive graphs. Currently, the dashboard is functional, and I am working on adding a chatbot assistant to answer cost-related queries, which is planned as the next phase.

# Features
 - Upload and process AWS & Azure billing CSVs
 - Visualize per-service costs with bar charts
 - Compare usage & costs across providers
 - Interactive dashboard powered by Streamlit
 - Planned feature: Chatbot for answering cost-related queries (in progress)

# Tech Stack
AWS & Azure - Data Source(CSV Billing files)
Python 3.13+ - Dashboard Backend
Streamlit – Dashboard frontend
Pandas – Data processing
Matplotlib – Visualizations

# Project Structure
├── AWS_analysis.py   ---> AWS cost analysis script
├── Azure_analysis.py ---> Azure cost analysis script
├── Cost_Dashboard.py ---> Streamlit dashboard
└── README.md         ---> Project documentation

# Future Enhancements
 - Chatbot to answer natural language cost queries
 - Multi-cloud combined comparison dashboard
 - Trend analysis over time

# Who can use this
- Cloud Engineers – to track and optimize AWS & Azure costs
- Finance/Management Teams – to get visibility into cloud spend
- Students/Researchers – to learn cloud cost analysis and dashboards
- Startups/Companies – to avoid unnecessary cloud overspending

# Installation & Usage

1. Clone the repository

$ git clone https://github.com/your-username/cloud-cost-dashboard.git
$ cd cloud-cost-dashboard

2. Install required dependencies

$ pip install -r requirements.txt

3. Prepare input files

Download/export  AWS cost report.
Download/export your Azure cost report.
Place them in the same folder as the scripts

4. Run the analysis scripts

python AWS-cost-analysis.py
python azure-cost-analysis.py

5. Launch the dashboard

streamlit run Cost_Dashboard.py

6. Open the given local URL in your browser (usually http://localhost:8501/) to view the dashboard.
