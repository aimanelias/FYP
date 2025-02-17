# COMBINED TF IDF AND RANDOM FOREST
import os
import pandas as pd
import pickle
from sklearn import metrics
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import time
import plotly.express as px
import plotly.graph_objects as go

# Models loading with error handling
try:
    cv = pickle.load(open('model/cv_combined.pkl', 'rb'))
    laptops = pickle.load(open('model/df_combined.pkl', 'rb'))
    model = pickle.load(open('model/model_combined.pkl', 'rb'))
    vector = pickle.load(open('model/vector_combined.pkl', 'rb'))
except FileNotFoundError:
    st.error("Required model files not found. Please ensure 'similarity.pkl' and 'laptop_list.pkl' exist in the model directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model files: {str(e)}")
    st.stop()

st.markdown("""
<style>
    p.title {
        font-size:50px ;
        color: black;
        text-align: center;
        background-color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    p.header {
        font-size:20px ;
    }
</style>
""", unsafe_allow_html=True)





#***** PREDICTION AND RECOMMEND FUNCTION *****



#***** RECOMMENDATION FUNCTION *****
def recommend(laptop_spec, vector):
    user_input_vector = cv.transform([laptop_spec])
    similarity_scores = cosine_similarity(user_input_vector, vector).flatten()
    top_5_indices = similarity_scores.argsort()[-5:][::-1]
    st.session_state["top_5_indices"] = top_5_indices
    top_5_laptops = laptops.iloc[top_5_indices]
    st.write("**HERE ARE SOME RECOMMENDATIONS FOR YOU**")
    columns = st.columns(5, vertical_alignment="top")
    for col, (_, laptop) in zip(columns, top_5_laptops.iterrows()):
        with col:
            st.image(laptop['img_link'], caption=laptop['name'], width=150)
    return top_5_indices


#***** OPTION DISPLAY FOR INPUT DICTIONARY *****
processor_mapping = {
    'i3': 'Intel i3', 'i5': 'Intel i5', 'i7': 'Intel i7', 'i9': 'Intel i9', 
    'ryzen 3': 'Ryzen 3', 'ryzen 5': 'Ryzen 5', 'ryzen 7': 'Ryzen 7', 
    'ryzen 9': 'Ryzen 9', 'apple': 'Apple CPU', 'integrated': 'Integrated CPU'
}
options_dict = {
    'brand': sorted(laptops['brand'].unique()),
    'ram': sorted(laptops['ram'].unique()),
    'cpu': sorted([processor_mapping.get(proc, proc) for proc in laptops['cpu'].unique()]),
    'storage': sorted(laptops['storage'].unique()),
    'os': sorted(laptops['os'].unique()),
    'display': sorted(laptops['display'].unique())
}


#***** INPUT *****
st.markdown('<p class="title">LAPTOP RECOMMENDER SYSTEM</p>', unsafe_allow_html=True)

for key, options in options_dict.items(): #insert empty space
    options.insert(0, f"") #Choose any or type to find {key}

#***** DROPDOWN INPUT *****
st.write('FILL THE LAPTOP SPECIFICATION')
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    selected_brand = st.selectbox('BRAND:', options_dict['brand'])
    selected_processor = st.selectbox('PROCESSOR / CPU:', options_dict['cpu'])
    selected_ram = st.selectbox('RAM:', options_dict['ram'])
with col2:
    selected_storage = st.selectbox('STORAGE:', options_dict['storage'])
    selected_os = st.selectbox('OPERATING SYSTEM / OS:', options_dict['os'])
    selected_display = st.selectbox('SCREEN SIZE:', options_dict['display'])
price = st.text_input('PRICE:')
selected_price = f"RM{price}" #add RM in front of price 

#concat all specs as full laptop specs
laptop_spec = f"{selected_brand} {selected_processor} {selected_ram} {selected_os} {selected_storage} {selected_display} {selected_price}" 
#st.write(laptop_spec) #display  the merged specs
#check and ensure user choose all specs
if (selected_brand == "" or
    selected_processor == "" or
    selected_ram == "" or
    selected_storage == "" or
    selected_os == "" or
    selected_display == "" or
    not price):
    st.error("PLEASE FILL ALL SPECIFICATIONS", icon=":material/error:")
    recommendation_button = False
else: #if user choose all, display recommend button to predict and recommend
    st.divider()
    recommendation_button = st.button('Recommend', key='recommendation_button')




def pop_predict(laptop_spec):
    msg = st.toast('Predicting...')
    user_input_vector = cv.transform([laptop_spec])
    predicted_category = model.predict(user_input_vector)[0]
    if predicted_category.lower() == 'Office':
        msg.toast(f"You need a {predicted_category.lower()} laptop", icon =":material/apartment:")
    if predicted_category.lower() == 'gaming':
        msg.toast(f"You need a {predicted_category.lower()} laptop", icon =":material/stadia_controller:")
    else:
        msg.toast(f"You need a {predicted_category.lower()} laptop", icon =":material/apartment:")



# Session initialization
if "predict_state" not in st.session_state:
    st.session_state["predict_state"] = False
if "recommend_state" not in st.session_state:
    st.session_state["recommend_state"] = False


#----- RECOMMENDATION BUTTON -----  
if recommendation_button:
    st.session_state["recommend_state"] = True
    st.session_state["predict_state"] = True  
    pop_predict(laptop_spec) 
    recommend(laptop_spec, vector)  # Call recommendation logic


#----- COMPARE BUTTON -----  
if st.session_state.get("recommendation_state", True):
    st.write("")
    compare_button = st.button('Compare', key='compare_button')
    st.session_state["recommendation_state"]  = True

    if compare_button:
        # Fetch the top 5 recommended laptops using the indices
        top_5_indices = st.session_state.get("top_5_indices", [])

        if len(top_5_indices) > 0:  # Check if top_5_indices is not empty
            top_5_laptops = laptops.iloc[top_5_indices]

            # Create the Plotly table
            fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=["MODEL", "BRAND", "PRICE", "CPU", "RAM", "STORAGE", "OS", "DISPLAY "],
                            fill_color='#EFB036',
                            align="left",
                            font=dict(size=12, color="black"),
                        ),
                        cells=dict(
                            values=[
                                top_5_laptops["name"].tolist(),        # Laptop names
                                top_5_laptops["brand"].tolist(),       # Laptop brands
                                top_5_laptops["price"].tolist(),       # Laptop prices
                                top_5_laptops["processor"].tolist(),   # Laptop CPUs
                                top_5_laptops["ram"].tolist(),         # Laptop RAMs
                                top_5_laptops["storage"].tolist(),     # Laptop storage
                                top_5_laptops["os"].tolist(),          # Laptop OS
                                top_5_laptops["display"].tolist(),     # Laptop screen sizes
                            ],
                            fill_color="white",
                            align="left",
                            font=dict(size=12, color="black"),
                        ),
                    )
                ]
            )
            # Reduce spacing with custom CSS
            st.markdown(
                """
                <style>
                    .stPlotlyChart {
                        margin-top: -30px;
                        margin-bottom: -90px;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Wrap the table in a container to manage spacing
            with st.container():
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No laptops found to display. Please run the recommendation system first.")


#----- CLEAR BUTTON ----- 
st.divider()   
clear_button = st.button('Clear')
if clear_button:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()


#st.write(st.session_state)