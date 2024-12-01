import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Olist Dataset Dashboard", layout="wide")

# Load datasets once at the beginning
@st.cache_data
def load_data():
    customers = pd.read_csv('data/customers_dataset.csv')
    order_items = pd.read_csv('data/order_items_dataset.csv')
    orders = pd.read_csv('data/orders_dataset.csv')
    products = pd.read_csv('data/products_dataset.csv')
    category_translation = pd.read_csv('data/product_category_name_translation.csv')
    payments = pd.read_csv('data/order_payments_dataset.csv')
    return customers, order_items, orders, products, category_translation, payments

customers, order_items, orders, products, category_translation, payments = load_data()



# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f5;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    h1, h2, h3, h4 {
        color: #333;
    }
    .stMarkdown {
        color: #555;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 12px;
        color: #777;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit Sidebar for navigation
st.sidebar.title("Olist Dataset Dashboard")
selection = st.sidebar.radio("Go to", ["Landing Page", "Customer Demographics", "Order Trends", "Payment Methods"])

# Page 0: Landing Page
if selection == "Landing Page":
    st.title("Olist Dataset Dashboard")
    st.subheader("About the Creator")
    st.write("""
    This dashboard was created by **Izzat Arroyyan** as part of the **IDCamp Data Science Path assignment**.
    """)
    st.write("Find more about me:")

    # Links with icons
    st.markdown("""
    <div style="text-align: left;">
        <a href="https://www.linkedin.com/in/izzatarroyyan" target="_blank" style="text-decoration: none; display: flex; align-items: center; margin-bottom: 10px;">
            <img src="https://img.icons8.com/color/24/000000/linkedin.png" alt="LinkedIn" style="margin-right: 10px;">
            <span>LinkedIn: izzatarroyyan</span>
        </a>
        <a href="https://github.com/izzatarroyyan12" target="_blank" style="text-decoration: none; display: flex; align-items: center; margin-bottom: 10px;">
            <img src="https://img.icons8.com/ios-glyphs/24/000000/github.png" alt="GitHub" style="margin-right: 10px;">
            <span>GitHub: izzatarroyyan12</span>
        </a>
        <a href="mailto:izzatarroyyan11@gmail.com" style="text-decoration: none; display: flex; align-items: center;">
            <img src="https://img.icons8.com/color/24/000000/gmail.png" alt="Email" style="margin-right: 10px;">
            <span>Email: izzatarroyyan11@gmail.com</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## About the Dataset
    The dataset used in this dashboard is sourced from an **e-commerce platform** and consists of multiple interconnected tables:
    - **Orders Dataset**: Contains details about orders, including order ID, timestamps for various stages of the order process, and delivery information.
    - **Customers Dataset**: Includes customer demographic and geographic data, such as state and city.
    - **Products Dataset**: Provides information about the products available on the platform, such as category, dimensions, and weight.
    - **Category Translations**: Maps product categories from their original language to English for better accessibility.
    - **Payments Dataset**: Contains details about the payment methods used for each order, including payment type (e.g., credit card, boleto), payment value, and payment status.

    The dataset was provided by **Olist**, the largest department store in Brazilian marketplaces. The goal of this dashboard is to analyze customer demographics, order trends, and product data to uncover patterns and insights that can help improve business strategies.
    You can access the dataset on [Kaggle here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data).
    """)

    st.markdown("Explore the dashboard using the navigation bar on the left to uncover insights about customer demographics, order trends, and more.")

# Page 1: Customer Demographics and Geography
elif selection == "Customer Demographics":
    st.title("Customer Demographics and Geography")
    st.subheader("Explore the distribution of customers across regions and demographics.")
    
    customer_count_by_state = customers.groupby('customer_state').size().reset_index(name='count')

    # Sorting options
    sort_by = st.selectbox("Sort by", options=["State Code", "Count"], index=1)
    sort_order = st.radio("Sort Order", options=["Ascending", "Descending"], index=1)
    ascending = sort_order == "Ascending"
    
    # Apply correct sorting based on selection
    if sort_by == "State Code":
        sort_by_column = 'customer_state'
    else:
        sort_by_column = 'count'

    customer_count_by_state = customer_count_by_state.sort_values(by=sort_by_column, ascending=ascending)

    # Visualization: Customers by State
    fig = px.bar(customer_count_by_state, x='customer_state', y='count', title='Customers by State', labels={'customer_state': 'State Code', 'count': 'Number of Customers'}, color='count', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    
    # Filter by State
    state = st.selectbox("Select State", customer_count_by_state['customer_state'].unique())
    filtered_customers = customers[customers['customer_state'] == state]
    
    customer_count_by_city = filtered_customers.groupby('customer_city').size().reset_index(name='count').sort_values(by='count', ascending=False)
    top_cities = customer_count_by_city.head(6)
    others_count = customer_count_by_city['count'][6:].sum()

    # Add "Others" row to the data
    top_cities = pd.concat([top_cities, pd.DataFrame([{'customer_city': 'Others', 'count': others_count}])], ignore_index=True)

    # Pie chart
    fig_city_pie = px.pie(top_cities, values='count', names='customer_city', title=f'Distribution of Customers by City in {state}', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_city_pie)

# Page 2: Order Trends Over Time
elif selection == "Order Trends":
    st.title("Order Trends Over Time")
    st.subheader("Explore the number of orders over time.")
    
    # Ensure the 'orders' dataset is processed once and reused
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    # Merge with product and category translation
    merged_orders = orders.merge(order_items[['order_id', 'product_id']], on='order_id', how='left')\
                          .merge(products[['product_id', 'product_category_name']], on='product_id', how='left')\
                          .merge(category_translation[['product_category_name', 'product_category_name_english']], 
                                 left_on='product_category_name', right_on='product_category_name', how='left')
    
    # Filter by time and product categories
    st.subheader("Filter by Time and Product Categories")

    # Ensure 'month' is in datetime format
    merged_orders['month'] = pd.to_datetime(merged_orders['month'], format='%Y-%m')

    # Get unique months as datetime and sort them
    unique_months = sorted(merged_orders['month'].unique())

    # Convert unique months to Period for filtering (to only keep year and month)
    unique_months_periods = [month.to_period('M') for month in unique_months]

    # Convert unique months periods back to string for the selectbox options
    unique_months_str = [month.strftime('%B %Y') for month in unique_months_periods]

    # Time period filter (Month-Year selection)
    start_month = st.selectbox("Select Start Month", unique_months_str, index=0)
    end_month = st.selectbox("Select End Month", unique_months_str, index=len(unique_months_str) - 1)

    # Convert the selected months back to Period for filtering
    start_month_period = pd.Period(start_month, freq='M')
    end_month_period = pd.Period(end_month, freq='M')

    # Ensure start_month_period is not after end_month_period
    if start_month_period >= end_month_period:
        st.error("The Start Month cannot be the same as or later than the End Month. Please modify your selection.")
    else:
        # Product category filter
        product_categories = category_translation['product_category_name_english'].unique()
        product_category = st.multiselect("Select Product Categories", options=product_categories, default=[])

        # Filter data based on the selected months
        filtered_orders = merged_orders[
            (merged_orders['month'].dt.to_period('M') >= start_month_period) &
            (merged_orders['month'].dt.to_period('M') <= end_month_period)
        ]

        # Apply product category filter if selected
        if product_category:
            filtered_orders = filtered_orders[
                filtered_orders['product_category_name_english'].isin(product_category)
            ]

        # Update visualization with filtered data
        filtered_orders_per_month = (
            filtered_orders.groupby(filtered_orders['month'].dt.to_period("M").astype(str))
            .size()
            .reset_index(name='count')
        )

        fig_filtered = px.line(
            filtered_orders_per_month,
            x='month',
            y='count',
            title=f"Orders Over Time ({', '.join(product_category) if product_category else 'All Categories'})",
            markers=True,
            line_shape='linear'
        )
        st.plotly_chart(fig_filtered)



# Page 3: Payment Methods Analysis
elif selection == "Payment Methods":
    st.title("Payment Methods Analysis")
    st.subheader("Explore the popularity of different payment methods over time.")
    
    # Load datasets (only once at the beginning)
    payments = pd.read_csv('data/order_payments_dataset.csv')
    orders = pd.read_csv('data/orders_dataset.csv')
    
    # Ensure the necessary columns are in datetime format for date filtering
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')

    # Merge payments with orders on 'order_id' to include timestamp and month
    merged_data = payments.merge(
        orders[['order_id', 'order_purchase_timestamp', 'month']], 
        on='order_id', how='inner'
    )
    
    # Group by month and payment_type to get counts of each payment method per month
    payment_method_count = merged_data.groupby(['month', 'payment_type']).size().reset_index(name='count')
    
    # Convert 'month' to string for display (e.g., "January 2022")
    payment_method_count['month_str'] = payment_method_count['month'].dt.strftime('%B %Y')
    unique_months = sorted(payment_method_count['month'].unique())
    unique_months_str = [month.strftime('%B %Y') for month in unique_months]
    
    # Month-Year Range Selector
    start_month = st.selectbox("Select Start Month", unique_months_str, index=0)
    end_month = st.selectbox("Select End Month", unique_months_str, index=len(unique_months_str) - 1)
    
    # Convert selected strings back to Period for filtering
    start_month_period = pd.Period(start_month, freq='M')  # Specify frequency 'M' for months
    end_month_period = pd.Period(end_month, freq='M')
    
    if start_month_period >= end_month_period:
        st.error("The Start Month cannot be the same as or later than the End Month. Please modify your selection.")
    else:
        # Filter the data based on the selected range
        filtered_data = payment_method_count[
            (payment_method_count['month'] >= start_month_period) & 
            (payment_method_count['month'] <= end_month_period)
        ]
        
        # Filter by Payment Method (multi-select)
        payment_types = st.multiselect(
            "Select Payment Methods",
            options=merged_data['payment_type'].unique(),
            default=merged_data['payment_type'].unique()  # Set default as all payment types selected
        )
        
        # Apply the payment method filter
        if payment_types:
            filtered_data = filtered_data[filtered_data['payment_type'].isin(payment_types)]
        
        # Visualization: Plot payment methods over the selected time range
        fig = px.bar(
            filtered_data, 
            x='month_str', 
            y='count', 
            color='payment_type', 
            title='Payment Methods Over Time',
            labels={'count': 'Transaction Count', 'month_str': 'Month', 'payment_type': 'Payment Method'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        # Set barmode to 'group' for a clustered bar chart
        fig.update_layout(
            barmode='group',  # Cluster bars side by side
            width=1100,       # Increase figure width
            height=600,       # Increase figure height
        )
        st.plotly_chart(fig)


# Footer
st.markdown("<div class='footer'>Created with ❤️ by Izzat Arroyyan</div>", unsafe_allow_html=True)