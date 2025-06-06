import pandas as pd
import matplotlib.pyplot as plt

# Create a dataframe from an Excel file
df = pd.read_excel('sales_data.xlsx', sheet_name='Sales')

# Display the first few rows of the dataframe
print("\nFirst few rows of the dataframe:")
print(df.head())

# Display the structure of the dataframe
print("\nStructure of the dataframe:")
print(df.info())

# Display summary statistics of the dataframe
print("\nSummary statistics of the dataframe:")
print(df.describe())

# Check for missing values in the dataframe
print("\nMissing values in each column:")
print(df.isnull().sum())

# Fill missing values in 'Units Sold' with 0
df['Units Sold'] = df['Units Sold'].fillna(0)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter the dataframe to include only rows where 'Units Sold' is greater than 0
df = df[df['Units Sold'] > 0]

# Calculate  and display total sales by multiplying 'Units Sold' by 'Unit Price'
df['Total Sales'] = df['Units Sold'] * df['Unit Price']
sales_by_region = df.groupby('Region')['Total Sales'].sum()
print("\nTotal sales by region:")
print(sales_by_region)

# Plot total sales by month
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Total Sales'].sum()
print("\nTotal sales by month:")
print(monthly_sales)

# Plotting the data
# Bar chart: Total Sales by Region
sales_by_region.plot(kind='bar', title='Total Sales by Region')
plt.ylabel('Sales ($)')
plt.show()

# Line chart: Monthly Sales Trend
monthly_sales.plot(kind='line', title='Monthly Sales Trend')
plt.ylabel('Sales ($)')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Save the summary data to an Excel file
with pd.ExcelWriter('sales_summary.xlsx') as writer:
    sales_by_region.to_excel(writer, sheet_name='Sales by Region')
    monthly_sales.to_excel(writer, sheet_name='Monthly Sales')