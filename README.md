# Budget Tracker Application

## Overview
The **Budget Tracker Application** is a web-based app that allows users to track and visualize their income and expenses over time. Built with Dash, Pandas, Plotly, and Dash Bootstrap Components, the application connects to a SQL Server database to store and retrieve financial data, providing users with a clear, interactive view of their budget performance.

## Features
- **Add/Remove Transactions**: Input income and expense entries into the SQL Server database.
- **Categorize Expenses**: Categorize transactions for better tracking.
- **Data Visualization**: Interactive graphs and charts to visualize your income, expenses, and savings.
- **Responsive UI**: Bootstrap-based responsive design for an optimal user experience across devices.
- **SQL Integration**: Connects to an SQL Server database to store, update, and retrieve transaction data.

## Technologies Used
- **Backend**: 
  - [Dash](https://dash.plotly.com/): A Python framework for building analytical web applications.
  - [Pandas](https://pandas.pydata.org/): For data manipulation and analysis.
  - [SQL Server](https://www.microsoft.com/en-us/sql-server): Database management system used for storing transaction data.
- **Frontend**:
  - [Plotly](https://plotly.com/python/): For generating interactive graphs and charts.
  - [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/): For responsive layout and styling.
- **Database**:
  - SQL Server for storing budget-related transactions.

## Installation

### Prerequisites
- Python 3.x
- SQL Server
- A SQL Server database and table to store budget data

### Clone the Repository
```bash
git clone https://github.com/yourusername/budget-tracker-app.git
cd budget-tracker-app
