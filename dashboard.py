import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
all_order_df = pd.read_csv("all_order.csv")
payment_df = pd.read_csv("payment_cleaned.csv")

def create_best_seller_product():
    most_sold_product= all_order_df['product_category_name_english'].value_counts().sort_values(ascending=False).head(10)
    most_sold_product_df = most_sold_product.reset_index()
    most_sold_product_df.columns = ['product_category_name_english', 'total_sales']

    return most_sold_product_df

def create_payment_used_by_customers():
    payment_count = payment_df.payment_type.value_counts()
    payment_count_df = payment_count.reset_index()
    payment_count_df.columns = ['payment_type', 'total']

    return payment_count_df

def rfm():
    rfm_df = all_order_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max", 
    "order_id": "nunique", 
    "price": "sum" 
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df['max_order_timestamp'] = pd.to_datetime(rfm_df['max_order_timestamp'])
    all_order_df["order_purchase_timestamp"]= pd.to_datetime(all_order_df["order_purchase_timestamp"])

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = all_order_df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
 
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

with st.sidebar:
    st.image("shop.jpg")
    st.write(
        """ ### :sparkles: Selamat Datang :sparkles: """)

st.header(
    """
    E-Commerce Dashboard 🛍️
    """
)
st.subheader("Best Selling Product")


ig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 10))
colors = ["#72BCD4"]
 
sns.barplot(x="total_sales", y="product_category_name_english", data=create_best_seller_product(),palette=colors)
ax.set_ylabel("Product",fontdict={'size':15})
ax.set_xlabel("Total Sales", fontdict={'size':15})
ax.set_title("The Best Selling Product by Number of Sales", loc="center", fontsize=20)
ax.tick_params(axis ='y', labelsize=12)
 
st.pyplot(ig)

st.subheader("Top Payment Method Used by Customers")
fig = plt.figure(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="total", 
    x="payment_type",
    data=create_payment_used_by_customers(),
    palette=colors
)
plt.title("Number of Payment Type Used by Customer", loc="center", fontsize=15)
plt.ylabel("Total")
plt.xlabel("Payment Type")
plt.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm().recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm().frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = round(rfm().monetary.mean(), 3) 
    st.metric("Average Monetary", value=avg_frequency)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
 
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="recency", x="customer_id", data=rfm().sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15, labelrotation = 90)

sns.barplot(y="frequency", x="customer_id", data=rfm().sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])

ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15,labelrotation = 90)

sns.barplot(y="monetary", x="customer_id", data=rfm().sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15, labelrotation = 90)
 
plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)
st.pyplot(fig)


