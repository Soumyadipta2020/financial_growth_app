# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# venv\Scripts\Activate.ps1 - Virtual env activate in terminal
# Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="India's Financial Growth", page_icon="📈", layout="wide")

# Header
st.title("📈 India's Financial Growth")
st.write(
    """
    This app visualizes important KPI's of financial growth of Indian economy. 
    The Data is available at [Database of Indian Economy](https://data.rbi.org.in/DBIE/#/dbie/home).
    """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_excel("./Indian_economic_growth.xlsx", header = 0)
    return df

df = load_data()
# df['Date'] = pd.to_datetime(df['Date'].astype(str).str[:10], format = '%Y-%m-%d').dt.date
# df = df.drop(df.columns[[0]], axis=1)

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# Column 1: Display the raw data
with col1:
    st.subheader('Raw Data')
    min_date = df['YEAR'].min()
    max_date = df['YEAR'].max()
    date_filter = st.slider("Select Date Range", min_date, max_date, (min_date, max_date))

    # Filter the dataframe based on the widget input
    df_filtered = df[(df["YEAR"].between(date_filter[0], date_filter[1]))]
    df_filtered = df_filtered.sort_values(by="YEAR", ascending=False)

    # Display the data as a table using `st.dataframe`.
    st.dataframe(
        df_filtered,
        use_container_width=True,
    )

# Column 2: Plot selection and graph display
with col2:
    st.subheader('Plot Selection')
    # Data format
    df_graph = df.melt(id_vars = ["PRICE TYPE", "CLASSIFICATION OF SECTOR WISE GCF", "BASE PERIOD", "YEAR"], 
                       value_vars = ["ACTUALS (INR)", "% CHANGE"], var_name = "TYPE", value_name = "VALUE").pivot(
                           index=["PRICE TYPE", "BASE PERIOD", "YEAR", "TYPE"], 
                           columns="CLASSIFICATION OF SECTOR WISE GCF",
                           values="VALUE"
                           ).reset_index()
    
    # Type filter
    type_options = df_graph["TYPE"].unique()
    type_filter = st.selectbox("Select a type of data:", type_options)

    df_graph_filter = df_graph[df_graph["TYPE"] == type_filter]

    # Price Type filter
    price_type = df_graph_filter["PRICE TYPE"].unique()
    price_type_filter = st.selectbox("Select a price type:", price_type)

    df_graph_filter = df_graph_filter[df_graph_filter["PRICE TYPE"] == price_type_filter]

    # Dropdown to select plot type
    plot_type = st.selectbox("Select plot type", ["Histogram", "Boxplot", "Violin Plot", "Scatter Plot"])
    
    # Conditional selection of variables based on plot type
    available_columns = df_graph_filter.columns[~df_graph_filter.columns.isin(["TYPE", "PRICE TYPE"])]
    if plot_type in ["Histogram", "Boxplot", "Violin Plot"]:
        variable = st.selectbox("Select a variable", available_columns)
    elif plot_type == "Scatter Plot":
        x_var = st.selectbox("Select X-axis variable", available_columns)
        y_var = st.multiselect("Select Y-axis variable", available_columns)
    
    # Button to generate plot
    if st.button(f"Generate {plot_type}"):
        plt.figure(figsize=(10, 6))
        
        # Generate the plot based on the selected type
        if plot_type == "Histogram":
            plt.hist(df_graph_filter[variable], bins=30, color='blue', edgecolor='black')
            plt.title(f'Histogram of {variable}')
            plt.xlabel(variable)
            plt.ylabel('Frequency')
            
        elif plot_type == "Boxplot":
            sns.boxplot(y=df_graph_filter[variable], color='blue')
            plt.title(f'Boxplot of {variable}')
            
        elif plot_type == "Violin Plot":
            sns.violinplot(y=df_graph_filter[variable], color='blue')
            plt.title(f'Violin Plot of {variable}')
            
        elif plot_type == "Scatter Plot":
            for y in y_var:
                plt.plot(df_graph_filter[x_var], df_graph_filter[y], label=y)
            plt.title('Scatter Plot')
            plt.xlabel(x_var)
            plt.ylabel("Values")
            plt.legend(title="Y Variables")
        
        # Display the plot in Streamlit
        st.pyplot(plt)
