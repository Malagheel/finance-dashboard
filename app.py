import streamlit as st
import pandas as pd
import sqlite3

# Set up Streamlit page
st.set_page_config(page_title="Finance Dashboard", layout="wide")
st.title("💰 Personal Finance Dashboard")
st.success("✅ App started successfully!")

# Connect to SQLite database
conn = sqlite3.connect("finance_dashboard.db")

# --- Calculate Total Income, Expense, and Net Balance KPIs ---
query_kpis = """
SELECT 
    SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) AS total_income,
    SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) AS total_expense
FROM transactions t
JOIN categories c ON t.category_id = c.id
"""
df_kpis = pd.read_sql_query(query_kpis, conn)

# Extract KPI values
total_income = df_kpis["total_income"][0]
total_expense = df_kpis["total_expense"][0]
net_balance = total_income - total_expense

# --- KPI Display ---
st.markdown("### 📊 Key Financial Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expense", f"${total_expense:,.2f}")
col3.metric("Net Balance", f"${net_balance:,.2f}")

# --- Net Balance Per Month ---
st.header("📈 Net Balance Per Month")
query1 = """
SELECT 
    strftime('%Y-%m', t.date) AS month,
    SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) -
    SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) AS net_balance
FROM transactions t
JOIN categories c ON t.category_id = c.id
GROUP BY month
ORDER BY month;
"""
df1 = pd.read_sql_query(query1, conn)
st.line_chart(df1.set_index("month")["net_balance"])

# --- Income vs Expense Per Month ---
st.header("💸 Monthly Income vs Expense")
query2 = """
SELECT 
    strftime('%Y-%m', t.date) AS month,
    SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) AS income,
    SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) AS expense
FROM transactions t
JOIN categories c ON t.category_id = c.id
GROUP BY month
ORDER BY month;
"""
df2 = pd.read_sql_query(query2, conn)
st.bar_chart(df2.set_index("month")[["income", "expense"]])

# --- Top Expense Categories ---
st.header("🔮 Top Expense Categories")
query3 = """
SELECT 
    c.name AS category,
    SUM(t.amount) AS total_spent
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE c.type = 'expense'
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 3;
"""
df3 = pd.read_sql_query(query3, conn)
st.table(df3)

# --- All Transactions Table ---
st.header("📋 All Transactions")
query4 = """
SELECT 
    t.date,
    c.name AS category,
    c.type,
    t.amount,
    a.name AS account
FROM transactions t
JOIN categories c ON t.category_id = c.id
JOIN accounts a ON t.account_id = a.id
ORDER BY t.date DESC;
"""
df4 = pd.read_sql_query(query4, conn)

# --- Month Filter ---
st.sidebar.header("Filter by Month")
months = df4['date'].str[:7].unique()
selected_month = st.sidebar.selectbox("Select Month", sorted(months, reverse=True))

filtered_df = df4[df4['date'].str.startswith(selected_month)]
st.dataframe(filtered_df)

# --- Download Button ---
st.download_button(
    "Download Transactions CSV",
    data=filtered_df.to_csv(index=False),
    file_name="transactions.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + SQLite")
