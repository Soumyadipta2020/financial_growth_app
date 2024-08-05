# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# venv\Scripts\Activate.ps1 - Virtual env activate in terminal

# Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
from io import BytesIO

# Page config
st.set_page_config(page_title="India's Financial Growth", page_icon="📈", layout="wide")

# HTML code for social media links
## image to base64
bl_image = Image.open("images/brand_logo.png")
bl_buffered = BytesIO()
bl_image.save(bl_buffered, format="PNG")
bl_img_str = base64.b64encode(bl_buffered.getvalue()).decode("utf-8")

self_image = Image.open("images/self.png")
self_buffered = BytesIO()
self_image.save(self_buffered, format="PNG")
self_img_str = base64.b64encode(self_buffered.getvalue()).decode("utf-8")

linkedin_image = Image.open("images/linkedin-logo.png")
linkedin_buffered = BytesIO()
linkedin_image.save(linkedin_buffered, format="PNG")
linkedin_img_str = base64.b64encode(linkedin_buffered.getvalue()).decode("utf-8")

github_image = Image.open("images/github-logo.png")
github_buffered = BytesIO()
github_image.save(github_buffered, format="PNG")
github_img_str = base64.b64encode(github_buffered.getvalue()).decode("utf-8")

orchidid_image = Image.open("images/orchid-id.png")
orchidid_buffered = BytesIO()
orchidid_image.save(orchidid_buffered, format="PNG")
orchid_img_str = base64.b64encode(orchidid_buffered.getvalue()).decode("utf-8")

so_image = Image.open("images/so_logo.png")
so_buffered = BytesIO()
so_image.save(so_buffered, format="PNG")
so_img_str = base64.b64encode(so_buffered.getvalue()).decode("utf-8")

kaggle_image = Image.open("images/kaggle-logo.png")
kaggle_buffered = BytesIO()
kaggle_image.save(kaggle_buffered, format="PNG")
kaggle_img_str = base64.b64encode(kaggle_buffered.getvalue()).decode("utf-8")

hf_image = Image.open("images/hf_logo.png")
hf_buffered = BytesIO()
hf_image.save(hf_buffered, format="PNG")
hf_img_str = base64.b64encode(hf_buffered.getvalue()).decode("utf-8")

## HTML
social_media_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px;">
    <div style="display: flex; justify-content: flex-start;">
        <a href="https://sites.google.com/view/soumyadipta-das" target="_blank" style="margin-right: 5px;">
            <img src="data:bl_image/png;base64,{bl_img_str}" style="width:40px; height:40px;"/>
        </a>
    </div>
    <div style="display: flex; justify-content: flex-end;">
        <a href="https://sites.google.com/view/soumyadipta-das" target="_blank" style="margin-right: 5px;">
            <img src="data:self_image/png;base64,{self_img_str}" style="width:30px; height:30px; border-radius:50%;"/>
        </a>
        <a href="https://www.linkedin.com/in/soumyadipta-das/" target="_blank" style="margin-right: 5px;">
            <img src="data:linkedin_image/png;base64,{linkedin_img_str}" style="width:30px; height:30px; border-radius: 80%;"/>
        </a>
        <a href="https://github.com/Soumyadipta2020" target="_blank" style="margin-right: 5px;">
            <img src="data:github_image/png;base64,{github_img_str}" style="width:30px; height:30px; border-radius: 70%;"/>
        </a>
        <a href="https://orcid.org/0000-0002-2414-8494" target="_blank" style="margin-right: 5px;">
            <img src="data:orchidid_image/png;base64,{orchid_img_str}" style="width:30px; height:30px;"/>
        </a>
        <a href="https://www.scienceopen.com/user/soumyadipta-das" target="_blank" style="margin-right: 5px;">
            <img src="data:so_image/png;base64,{so_img_str}" style="width:30px; height:30px;"/>
        </a>
        <a href="https://www.kaggle.com/soumyadiptadas" target="_blank" style="margin-right: 5px;">
            <img src="data:kaggle_image/png;base64,{kaggle_img_str}" style="width:30px; height:30px; border-radius: 80%;"/>
        </a>
        <a href="https://huggingface.co/soumyadiptadas" target="_blank">
            <img src="data:hf_image/png;base64,{hf_img_str}" style="width:30px; height:30px;"/>
        </a>
    </div>
</div>
"""

## Inject the HTML into the Streamlit app
st.markdown(social_media_html, unsafe_allow_html=True)

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
    st.header('Raw Data')
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
    st.header('Plot Selection')
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

    df_graph_filter = df_graph[df_graph["TYPE"] == type_filter].fillna(0)

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


# Footer HTML and CSS
footer = """
<style>
footer {
    visibility: hidden;
}
.main-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: #6c757d;
    background-color: #121212;
}
</style>

<div class="main-footer">
    <p>© 2024 Soumyadipta Das. All rights reserved. | 
    <a href="https://sites.google.com/view/soumyadipta-das" target="_blank">Profile</a>
</div>
"""

# Injecting the footer into the Streamlit app
st.markdown(footer, unsafe_allow_html=True)