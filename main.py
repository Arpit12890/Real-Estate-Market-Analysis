# We will solve this problem using Exploratory Data Analysis (EDA).
# EDA helps us understand patterns, relationships, and anomalies in the data before applying any advanced modeling.
# The solution is divided into logical steps: 1. Data loading and understanding
# 2. Data cleaning and preparation
# 3. Analysis to answer each business question
# 4. Summary of insights


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Data Loading
df=pd.read_csv('data.csv')
# print(df.info())

#Data Cleaning
##Standardize Column Names
df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")

df=df.drop_duplicates()

# Convert Numeric Columns
df['price']=df['price'].str.replace(',','').astype(float)
df['rate_per_sqft']=df['rate_per_sqft'].str.replace(',','').astype(float)

# categorical columns cleaning
df['status']=df['status'].str.strip().str.lower()
df['rera_approval']=df['rera_approval'].str.strip().str.lower().map({'approved by rera':True,'not approved by rera':False})
df['flat_type']=df['flat_type'].str.strip().str.lower()

df=df.drop_duplicates()
# print(df.info())

# Answering Business Questions with Analysis

# idxmax() returns the index label corresponding to the maximum value.
#Which is the costliest flat in the dataset?
costliest_flat=df.loc[df['price'].idxmax()]
print(f"the costliest flat is a {costliest_flat['flat_type']} flat in {costliest_flat['locality']} priced at {costliest_flat['price']/10000000} crores.")

# Which locality has the highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
print(f"The locality with the highest average price is {highest_avg_price_locality}.")

# Which locality has the highest rate per square foot?
highest_avg_rate_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax()
print(f"The locality with the highest average rate per square foot is {highest_avg_rate_locality}.")

# Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()

under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()

if ready_to_move_avg_price > under_construction_avg_price:  
    print(f"Ready-to-move properties cost more on average ({ready_to_move_avg_price}) than under-construction properties ({under_construction_avg_price}).")    

# Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price > rera_not_approved_avg_price:
    print("RERA-approved properties command a price premium on average.")
else:
    print("RERA-approved properties do not command a price premium on average.")
    
# How does area (sqft) impact property price?
sns.scatterplot(data=df, x='area', y='price')
# plt.show()

# Which BHK configuration is the most expensive on average?
most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
print(f"The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

# Which flat type (Apartment, Floor, Plot) is the costliest?
most_expensive_flat_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"The costliest flat type on average is {most_expensive_flat_type}.")

# Do certain builders or companies consistently price higher?
print("Top 5 builders/companies with the highest average price per square foot:",end=" ")
top_5_builders = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)
for builder in top_5_builders.index:
    print(builder,end=", ")
    
# Are larger homes always more expensive per square foot?--> NO
sns.scatterplot(data=df, x='area', y='rate_per_sqft')
plt.show()


    
   












