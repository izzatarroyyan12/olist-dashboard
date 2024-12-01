# Olist Dataset Dashboard

This is an interactive dashboard created using **Streamlit**, which analyzes customer demographics, order trends, and payment methods from the **Olist e-commerce dataset**. The dashboard allows users to explore various aspects of the dataset through different visualizations and filters.

## Features

- **Landing Page**: Introduction and creator information.
- **Customer Demographics**: Explore the distribution of customers across regions and cities.
- **Order Trends**: Analyze order trends over time.
- **Payment Methods**: Explore the popularity of different payment methods over time.

## Additional Analysis

There are also notebooks that provide deeper analysis of the following questions. You can access these analyses in the `notebook.ipynb` file after cloning the repository, or you can run the notebook in [**Google Colaboratory**](https://colab.research.google.com/drive/17oBVE2OrMA5yKmFutU4WPXhm9AenUoxO?usp=sharing). To run the notebook in Google Colaboratory, you will need to manually upload the dataset.

### Pertanyaan 1:
**How does the difference between actual and estimated delivery times relate to the review scores given by customers?**

This analysis explores the impact of delivery time discrepancies on customer satisfaction as measured by review scores. The notebook performs a detailed analysis of the relationship between these variables.

### Pertanyaan 2:
**How has the usage of different payment methods evolved over time on Olist?**

This analysis tracks the trends in payment methods used by customers on Olist, helping to understand how the payment preferences have changed over time.

## Setup

To run this project locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/izzatarroyyan12/olist-dashboard.git
```
### 2. Install dependencies
Make sure you have Python installed. It’s recommended to use a virtual environment.
To install the required libraries, navigate to the project directory and run the following command:
```bash
cd olist-dataset-dashboard
pip install -r requirements.txt
```
### 3. Run the Streamlit app
After installing the dependencies, start the Streamlit application by running:
```bash
streamlit run app.py
```
This will start the app on your local server (usually http://localhost:8501).

## Dataset
This dashboard uses the Olist dataset, which contains data about an e-commerce platform in Brazil. You can access the dataset on [Kaggle here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data).

## Technologies Used
- **Streamlit**: For building the interactive web app.
- **Plotly**: For data visualization.
- **Pandas**: For data manipulation and analysis.
