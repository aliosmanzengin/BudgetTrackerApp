Functional Requirements Document (FRD)
1. Project Overview
Purpose: To develop a budgeting and spending tracker web application that helps users monitor their expenses by category, view trends, calculate averages, and plan future budgets.
Users: Individuals looking to manage their finances by tracking spending and analyzing spending habits.
2. Scope and Objectives
Track daily expenses across customizable categories.
Display weekly, monthly, and yearly summaries of total and category-wise spending.
Provide visual representations (charts and graphs) for spending trends and distribution.
Calculate average spending by week, month, and year based on historical data.
Future option: allow user-specific settings, budgets, and alerts for overspending.
3. Functional Requirements
3.1 User Interface (UI)
Home Page:

Show a brief summary of the user’s recent spending activity.
Display links to view detailed reports, add transactions, and access settings.
Transaction Management:

Add New Transaction:
Input fields: Date, Amount, Category (dropdown with predefined categories), Notes (optional).
Submit button to add transaction to the database.
Edit Transaction:
Option to edit past transactions.
Delete Transaction:
Option to remove transactions.
Category Management:

Predefined Categories: Rent, Food, Clothes, Transport, Subscriptions, Games, Gifts & Donations.
Custom Categories: Allow users to add/edit custom categories.
Spending Summary (by Time Period):

View total spending by category for the following periods:
Weekly
Monthly
Yearly
Display summary data in a table format, organized by time period and category.
Visualizations:

Spending Trends:
Line chart showing total spending over time (weekly/monthly).
Category Distribution:
Pie chart showing the distribution of spending by category over the selected period.
Comparison Bar Chart:
Bar chart comparing current spending with historical averages (weekly, monthly).
Averages and Analytics:

Weekly, Monthly, Yearly Averages:
Display average spending by category based on historical data.
Comparison with Budget (Future Addition):
Option to set budget per category and show comparison of actual spending vs. budget.
Settings:

Manage Categories: Add, rename, or delete custom categories.
Alerts and Notifications (Future Addition):
Allow users to set spending limits for categories and receive alerts if exceeded.
Data Export: Option to export data in CSV format for external analysis.
4. Non-Functional Requirements
Performance:

Fast response times for data loading and updates.
Efficient database queries for high performance on large datasets.
Reliability:

Data persistence through SQLite or another reliable database.
Regular saving of data to prevent data loss.
Usability:

Clean, intuitive design suitable for users with basic digital literacy.
Responsive design for compatibility across desktops, tablets, and mobile devices.
Scalability:

Flexible design to accommodate additional features, such as linking with bank accounts or mobile apps.
Security:

Basic data protection practices, such as input validation and sanitation.
Secure data storage if sensitive information (like bank data) is added in the future.
5. User Stories
As a user, I want to log my expenses with categories and dates so that I can track my spending.
As a user, I want to see my total spending by category each month so that I understand my expenses better.
As a user, I want to visualize my spending trends so that I can monitor my habits over time.
As a user, I want to set budgets per category and receive alerts so that I avoid overspending (future addition).
As a user, I want to export my data so that I can analyze it externally if needed.
6. Data Requirements
Database Tables:
Categories:
id: Integer, Primary Key
name: Text, Unique
Transactions:
id: Integer, Primary Key
date: Date
amount: Float
category_id: Foreign Key to Categories
notes: Text (optional)
7. Future Features
Budget limits per category with alert notifications.
Integration with financial APIs for automatic transaction logging.
Multi-user support, if the app is to be shared.
