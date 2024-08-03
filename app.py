# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# venv\Scripts\Activate.ps1 - Virtual env activate in terminal
# Library
import os.path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the app to wide mode
st.set_page_config(layout="wide")

# Load and preprocess the dataset
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.csv")
df = pd.read_excel("./MSVAR_Data.xlsx", header = 0)
df = df.drop(df.columns[[0]], axis=1) 

# Header
st.title('Financial Growth Observation')

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# Column 1: Display the raw data
with col1:
    st.subheader('Raw Data')
    st.write(df)

# Column 2: Plot selection and graph display
with col2:
    st.subheader('Plot Selection')
    
    # Dropdown to select plot type
    plot_type = st.selectbox("Select plot type", ["Histogram", "Boxplot", "Violin Plot", "Scatter Plot"])
    
    # Conditional selection of variables based on plot type
    if plot_type in ["Histogram", "Boxplot", "Violin Plot"]:
        variable = st.selectbox("Select a variable", df.columns)
    elif plot_type == "Scatter Plot":
        x_var = st.selectbox("Select X-axis variable", df.columns)
        y_var = st.selectbox("Select Y-axis variable", df.columns)
    
    # Button to generate plot
    if st.button(f"Generate {plot_type}"):
        plt.figure(figsize=(10, 6))
        
        # Generate the plot based on the selected type
        if plot_type == "Histogram":
            plt.hist(df[variable], bins=30, color='blue', edgecolor='black')
            plt.title(f'Histogram of {variable}')
            plt.xlabel(variable)
            plt.ylabel('Frequency')
            
        elif plot_type == "Boxplot":
            sns.boxplot(y=df[variable], color='blue')
            plt.title(f'Boxplot of {variable}')
            
        elif plot_type == "Violin Plot":
            sns.violinplot(y=df[variable], color='blue')
            plt.title(f'Violin Plot of {variable}')
            
        elif plot_type == "Scatter Plot":
            plt.scatter(df[x_var], df[y_var], color='blue')
            plt.title(f'Scatter Plot of {x_var} vs {y_var}')
            plt.xlabel(x_var)
            plt.ylabel(y_var)
        
        # Display the plot in Streamlit
        st.pyplot(plt)
