#TF IDF HAS SLIDER, WRONG RECOMMENDATIONS
import os
import pandas as pd
import pickle
import streamlit as st


# Safe loading of pickle files with error handling
try:
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    laptops = pickle.load(open('model/laptop_list.pkl', 'rb'))
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
    }
    p.header {
        font-size:20px ;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">LAPTOP RECOMMENDER SYSTEM</p>', unsafe_allow_html=True)

# Session initialization
if "detail_state" not in st.session_state:
    st.session_state["detail_state"] = False
if "recommended_state" not in st.session_state:
    st.session_state["recommended_state"] = False
if "more_states" not in st.session_state:
    st.session_state["more_states"] = {}

#***** FUNCTION *****
#***** DISPLAY RECOMMENDATION LIST *****
def recommend(laptop_name, num_recommendations=5):
    laptops.reset_index(drop=True, inplace=True) # Reset the index to align with the similarity matrix

    #if laptop exists in the data
    if laptop_name not in laptops['name'].values:
        st.write(f"Laptop '{laptop_name}' not found.")
        return [], [], []

    index = laptops[laptops['name'] == laptop_name].index[0] #get the index of the selected laptop model
    # Ensure the index is within bounds
    if index >= len(similarity):
        st.write("Error: The index is out of bounds for the similarity matrix.")
        return [], [], []
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_laptops_name = [] #lists to store recommended laptop names and images
    recommended_laptops_image = []
    similarity_scores = []

    for i in distances[1:num_recommendations+1]:  
        recommended_laptops_name.append(laptops.iloc[i[0]]['name'])
        recommended_laptops_image.append(laptops.iloc[i[0]]['img_link']) 
        similarity_scores.append(f"{i[1]:.2f}")  # Format the similarity score to two decimals
        
    return recommended_laptops_name, recommended_laptops_image, similarity_scores

#***** DISPLAY LAPTOP DETAILS *****
def display_laptop_details(laptop_name):
    laptop_details = laptops[laptops['name'] == laptop_name].iloc[0]  # Get the first match (there should be only one)

    if laptop_details is not None:
        # Get the index of the selected laptop
        laptop_index = laptops[laptops['name'] == laptop_name].index[0]
        # Create two columns
        col1, col2, col3 = st.columns([1,1,1])  # Adjust the ratio to your needs
        
        with col1:
            # Show the laptop image in the first column
            st.image(laptop_details['img_link']) 
        
        with col2:
            st.write(f"**LAPTOP SPECIFICATION**")
            st.write(f"**Laptop Name:**")
            st.write(f"**Brand:**")
            st.write(f"**Processor:**")
            st.write(f"**RAM:**")
            st.write(f"**Storage:**")
            st.write(f"**Operating System:**")
            st.write(f"**Price:**")

        with col3:
            st.write(f"**DETAIL**")
            st.write(f"{laptop_details['name']}")
            st.write(f"{laptop_details['brand']}")
            st.write(f"{laptop_details['processor']}")
            st.write(f"{laptop_details['ram']} GB")
            st.write(f"{laptop_details['storage']} GB")
            st.write(f"{laptop_details['os']}")
            st.write(f"RM {laptop_details['price']}")
            st.write(f"**Index**: {laptop_index}")

#***** DISPLAY MORE DETAILS *****
def display_more_details(laptop_name):
    laptop_details = laptops[laptops['name'] == laptop_name].iloc[0]  # Get the first match (there should be only one)

    if laptop_details is not None:
        # Create two columns
        col1, col2= st.columns([1,1])  # Adjust the ratio to your needs
        with col1:
            st.write(f"**Laptop Name:**")
            st.write(f"**Brand:**")
            st.write(f"**Processor:**")
            st.write(f"**RAM:**")
            st.write(f"**Storage:**")
            st.write(f"**Operating System:**")
            st.write(f"**Price:**")

        with col2:
            st.write(f"{laptop_details['name']}")
            st.write(f"{laptop_details['brand']}")
            st.write(f"{laptop_details['processor']}")
            st.write(f"{laptop_details['ram']} GB")
            st.write(f"{laptop_details['storage']} GB")
            st.write(f"{laptop_details['os']}")
            st.write(f"RM {laptop_details['price']}")

#----- CLEAR BUTTON -----    
clear_button = st.button('Clear')
if clear_button:
    # Reset all states
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

#----- SEARCH BOX -----
laptop_list = laptops['name'].values #get all laptop names
selected_laptop = st.selectbox(
    'Type or select a laptop',
    laptop_list
)

#----- DETAIL BUTTON -----
detail_button = st.button('Detail', key='detail_button')
if detail_button or st.session_state.get("detail_state", False):
    st.session_state["detail_state"] = True
    display_laptop_details(selected_laptop)

#----- SLIDER -----
num_recommendations = st.slider('Select number of recommendations:', min_value=1, max_value=10, value=5, key='slider')

#----- RECOMMENDATION BUTTON -----
recommendation_button = st.button('Recommend', key='recommendation_button')    
if recommendation_button or st.session_state.get("recommended_state", False):
    st.session_state["recommended_state"] = True
    st.write("**HERE ARE SOME RECOMMENDATIONS FOR YOU**")
    recommended_names, recommended_images, similarity_scores = recommend(selected_laptop, num_recommendations=num_recommendations)
    cols = st.columns(num_recommendations)

    for i in range(num_recommendations):
        with cols[i]:
            st.image(recommended_images[i])
            st.text(recommended_names[i])
            st.write(f"**Similarity Score**: {similarity_scores[i]}")
            
            # Show More Recommendations button with individual state management
            button_key = f"more_button_{i}"
            more_button = st.button('More', key=button_key)
            
            # Initialize state for this specific button if not exists
            if button_key not in st.session_state["more_states"]:
                st.session_state["more_states"][button_key] = False
            
            # Update state when button is clicked
            if more_button:
                st.session_state["more_states"][button_key] = not st.session_state["more_states"][button_key]
            
            # Display details if this specific button's state is True
            if st.session_state["more_states"].get(button_key, False):
                display_more_details(recommended_names[i])
