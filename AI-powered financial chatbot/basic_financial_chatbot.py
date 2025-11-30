import pandas as pd

# Load your analyzed data (change filename if needed)
df = pd.read_csv("GFC_Financial_Data.csv")

# Rename columns for easier access
df.rename(columns={
    "Total Revenue (USD Millions)": "Total Revenue",
    "Net Income (USD Millions)": "Net Income",
    "Total Assets (USD Millions)": "Total Assets",
    "Total Liabilities (USD Millions)": "Total Liabilities",
    "Operating Cash Flow (USD Millions)": "Operating Cash Flow"
}, inplace=True)

def get_latest_year(company):
    return df[df["Company"] == company]["Fiscal Year"].max()

def simple_chatbot(user_query):
    user_query = user_query.lower()

    # --- TOTAL REVENUE ---
    if "total revenue" in user_query:
        company = input("Enter company name: ").title()
        year = int(input("Enter fiscal year: "))

        result = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]

        if not result.empty:
            revenue = result["Total Revenue"].values[0]
            return f"The total revenue of {company} in {year} was ${revenue} million."
        else:
            return "Data not found for the selected company/year."

    # --- NET INCOME ---
    elif "net income" in user_query and "change" not in user_query:
        company = input("Enter company name: ").title()
        year = int(input("Enter fiscal year: "))

        result = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]

        if not result.empty:
            net_income = result["Net Income"].values[0]
            return f"The net income of {company} in {year} was ${net_income} million."
        else:
            return "Data not found for the selected company/year."

    # --- NET INCOME TREND ---
    elif "net income changed" in user_query or "net income change" in user_query:
        company = input("Enter company name: ").title()
        company_data = df[df["Company"] == company].sort_values("Fiscal Year")

        if len(company_data) >= 2:
            first = company_data.iloc[0]["Net Income"]
            last = company_data.iloc[-1]["Net Income"]
            change = last - first

            if change > 0:
                trend = "increased"
            elif change < 0:
                trend = "decreased"
            else:
                trend = "remained stable"

            return f"Over the last three years, {company}'s net income has {trend} by ${abs(change)} million."
        else:
            return "Not enough data to analyze trend."

    # --- FINANCIAL HEALTH (DEBT RATIO) ---
    elif "financial health" in user_query or "debt" in user_query:
        company = input("Enter company name: ").title()
        year = get_latest_year(company)

        result = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]

        if not result.empty:
            assets = result["Total Assets"].values[0]
            liabilities = result["Total Liabilities"].values[0]
            debt_ratio = liabilities / assets

            if debt_ratio < 0.4:
                risk = "Low Financial Risk"
            elif debt_ratio <= 0.6:
                risk = "Moderate Financial Risk"
            else:
                risk = "High Financial Risk"

            return f"{company}'s latest debt ratio is {debt_ratio:.2f}, indicating {risk}."
        else:
            return "Financial health data not found."

    # --- OPERATING CASH FLOW ---
    elif "cash flow" in user_query:
        company = input("Enter company name: ").title()
        year = int(input("Enter fiscal year: "))

        result = df[(df["Company"] == company) & (df["Fiscal Year"] == year)]

        if not result.empty:
            cashflow = result["Operating Cash Flow"].values[0]
            return f"{company} generated ${cashflow} million in operating cash flow in {year}."
        else:
            return "Cash flow data not found."

    # --- FALLBACK ---
    else:
        return "Sorry, I can only provide information on predefined financial queries."

# --- CHAT LOOP ---
print("GFC Financial Chatbot Prototype")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("Ask a financial question: ")

    if user_input.lower() == "exit":
        print("Chatbot session ended.")
        break

    response = simple_chatbot(user_input)
    print("Chatbot:", response)
    print()



"""
GFC Financial Chatbot Prototype

Overview:
This is a simplified Python-based chatbot designed to provide insights from corporate financial data.
It uses pre-analyzed 10-K and 10-Q financial data for Microsoft, Tesla, and Apple to answer predefined financial queries.

How It Works:
1. Loads a CSV file (GFC_Financial_Data.csv) containing financial metrics for each company over the last three fiscal years:
   - Total Revenue
   - Net Income
   - Total Assets
   - Total Liabilities
   - Operating Cash Flow
2. Users provide a query, company name, and optionally a fiscal year. The chatbot matches the query using if-else logic.
3. Retrieves the relevant data and generates a response. For trends or financial health, it performs simple calculations and interprets results.

Predefined Queries Supported:
- Total Revenue: Requires company and year; returns total revenue.
- Net Income: Requires company and year; returns net income.
- Net Income Trend: Requires company; returns net income trend over 3 years.
- Financial Health: Requires company; calculates debt ratio and indicates risk.
- Operating Cash Flow: Requires company and year; returns operating cash flow.

Limitations:
- Only handles predefined queries.
- Data is static; does not pull live financial information.
- Simple logic; not an NLP or predictive AI model.
- Command-line interaction (or function calls in notebook) only.

Usage:
- Command-line: Run `python basic_financial_chatbot.py` and follow prompts.
- Jupyter Notebook: Use `simple_chatbot(query, company, year)` function.
"""