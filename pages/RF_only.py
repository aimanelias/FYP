import os
import numpy as np
import pandas as pd
import pickle
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import train_test_split
import streamlit as st


# Safe loading of pickle files with error handling
try:
    laptops = pickle.load(open('model/df_rf_only.pkl', 'rb'))
    rf_model = pickle.load(open('model/rf_model_only.pkl', 'rb'))
except FileNotFoundError:
    st.error("Required model files not found. Please ensure '.pkl' exist in the model directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model files: {str(e)}")
    st.stop()
    
st.markdown('<p class="title">LAPTOP RECOMMENDER SYSTEM</p>', unsafe_allow_html=True)

st.dataframe(laptops)
st.markdown("""
<style>
    p.title {
        font-size:50px ;
        color: black;
        text-align: center;
        background-color: white;
        border-radius: 10px;
    }
    p.header {
        font-size:20px ;
    }
</style>
""", unsafe_allow_html=True)

# Create a mapping for OS to numerical values
brand_mapping = {
    'Lenovo': 2, 'ASUS': 6, 'APPLE': 4, 'Redmi': 9, 'acer': 18, 'DELL': 11,
    'realme': 1, 'HP': 7, 'MSI': 5, 'SAMSUNG': 3, 'Infinix': 0, 'ALIENWARE': 19,
    'GIGABYTE': 15, 'Avita': 14, 'Mi': 16, 'MICROSOFT': 17, 'Sony': 8, 'Ultimus': 12,
    'Nokia': 10, 'LG': 13}
processor_mapping = {
    'i3': 2, 'i5': 3, 'i7': 1, 'i9': 7, 
    'ryzen 3': 8, 'ryzen 5': 5, 'ryzen 7': 0, 
    'ryzen 9': 6, 'apple': 9, 'integrated': 4
}
os_mapping = {'Windows': 3, 'MacOS': 2, 'ChromeOS': 0, 'DOS': 1}

#***** OPTION DISPLAY FOR INPUT*****
brand_options = ['Lenovo', 'ASUS', 'APPLE', 'Redmi', 'acer', 'DELL', 'realme', 'HP', 'MSI',
'SAMSUNG', 'Infinix', 'ALIENWARE', 'GIGABYTE', 'Avita', 'Mi', 'MICROSOFT', 'Sony', 'Ultimus', 'Nokia', 'LG']
processor_options = ['i3', 'i5', 'i7', 'i9', 'ryzen 3', 'ryzen 5', 'ryzen 7', 'ryzen 9', 'apple', 'integrated']
ram_options = sorted(laptops['ram'].unique())  # Get unique RAM options from the dataset
storage_options = sorted(laptops['storage'].unique())  # Get unique storage options from the dataset
os_options = ['Windows', 'MacOS', 'ChromeOS', 'DOS']
display_options = sorted(laptops['display'].unique())  # Get unique display sizes from the dataset

#***** DROPDOWN INPUT *****
st.write('FILL THE LAPTOP SPECIFICATION')
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    selected_brand = st.selectbox('BRAND:', brand_options)
    selected_processor = st.selectbox('PROCESSOR / CPU:', processor_options)
    selected_ram = st.selectbox('RAM (GB):', ram_options)
with col2:
    selected_storage = st.selectbox('Storage (GB):', storage_options)
    selected_os = st.selectbox('OPERATING SYSTEM / OS:', os_options)
    selected_display = st.selectbox('SCREEN SIZE (inch):', display_options)
    
selected_price = st.number_input('PRICE (inch):')
#***** MAPPING THE INPUT WITH ACTUAL VALUE *****
selected_brand_num = brand_mapping.get(selected_brand, None)
selected_processor_num = processor_mapping.get(selected_processor, None)
selected_os_num = os_mapping.get(selected_os, None)

st.write("brand", selected_brand_num, "CPU", selected_processor_num, "RAM", selected_ram,
         "os", selected_os_num, "STORAGE", selected_storage, "display", selected_display, 
         "price", selected_price)


laptop_spec = [[selected_brand_num, selected_processor_num, selected_ram, selected_os_num, 
                    selected_storage, selected_display, selected_price]]

X = laptops[['price', 'processor', 'ram', 'storage', 'display', 'brand', 'os']]
y = laptops['usecases']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, max_features= 1, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

# Evaluate the model's performance
rf_accuracy = metrics.accuracy_score(y_test,y_pred)
st.write("Accuracy(Random Forest):","{:.2%}".format(rf_accuracy))

predicted_usecase = rf_model.predict(laptop_spec)

def show_actual ():
    if predicted_usecase[0]== 0:
        return "Gaming"
    if predicted_usecase[0]== 1:
            return "Hybrid"
    if predicted_usecase[0]== 2:
            return "Office"
''' 
def suggest_top_laptops(laptops, laptop_spec):
    filtered_df = laptops[
        (laptops['processor'] == laptop_spec['processor']) &
        (laptops['laptop_brand'] == laptop_spec['brand']) &
        (laptops['os'] == laptop_spec['os']) &
        (laptops['ram'] >= laptop_spec['ram']) &  # RAM >= input
        (laptops['storage'] >= laptop_spec['storage']) &  # Storage >= input
        (laptops['display'] == laptop_spec['display'])  # Exact display match
    ]
    if not filtered_df.empty:
        filtered_df['price_diff'] = abs(filtered_df['price'] - user_input['price'])
        top_laptops = filtered_df.nsmallest(3, 'price_diff')  # Get top 3 laptops
        top_laptops_names = top_laptops['name'].tolist()
        return top_laptops_names
    else:
        return 
top_laptop_names = suggest_top_laptops(laptops, laptop_spec)'''

recommendation_button = st.button('Recommend', key='recommendation_button')
if recommendation_button:
    st.write("Predicted Usecase:", show_actual())
    st.write("Recommended Laptop Usecase:")