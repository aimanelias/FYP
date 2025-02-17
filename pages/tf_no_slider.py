#TF IDF NO SLIDER
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
def recommend(laptop_name):
    laptops.reset_index(drop=True, inplace=True)  # Reset the index to align with the similarity matrix

    # Check if the laptop exists in the data
    if laptop_name not in laptops['name'].values:
        st.write(f"Laptop '{laptop_name}' not found in the database.")
        return [], [], []

    # Get the index of the selected laptop model
    index = laptops[laptops['name'] == laptop_name].index[0]

    # Ensure the index is within bounds
    if index >= len(similarity):
        st.write("Error: The index is out of bounds for the similarity matrix.")
        return [], [], []

    # Sort laptops by similarity, retrieving similarity scores
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_laptops_name = []  # List to store recommended laptop names
    recommended_laptops_image = []  # List to store recommended laptop images
    similarity_scores = []  # List to store similarity scores

    printed_names = set()  # To avoid duplicate recommendations

    # Display recommendations
    for i in distances[1:]:
        name = laptops.iloc[i[0]]['name']
        img_link = laptops.iloc[i[0]]['img_link']
        similarity_score = i[1]

        # Check to ensure the input is excluded as recommendations
        if name != laptop_name and name not in printed_names:
            printed_names.add(name)
            recommended_laptops_name.append(name)
            recommended_laptops_image.append(img_link)
            similarity_scores.append(f"{similarity_score:.2f}")

        # Stop when 5 recommendations have been added
        if len(printed_names) == 5:
            break

    # Return the lists of recommended laptops, images, and similarity scores
    return recommended_laptops_name, recommended_laptops_image, similarity_scores


#***** DISPLAY LAPTOP DETAILS *****
def display_laptop_details(laptop_name):
    # Fetch the details of the specified laptop
    laptop_details = laptops[laptops['name'] == laptop_name].iloc[0]  # Get the first match (should be unique)

    if laptop_details is not None:
        st.write("### LAPTOP SPECIFICATION")
        
        # Create three columns for the layout (one for the image, two for the spec labels and details)
        col1, col2, col3 = st.columns([2, 1, 2])  # Adjust column width ratios as needed
        
        with col1:
            # Display laptop image
            st.image(laptop_details['img_link'], use_container_width=True)
        
        with col2:
            # Specifications labels
            st.write("**Name:**")
            st.write("**Brand:**")
            st.write("**Processor:**")
            st.write("**RAM:**")
            st.write("**Storage:**")
            st.write("**Operating System:**")
            st.write("**Price:**")

        with col3:
            # Specifications details
            st.write(f"{laptop_details['name']}")
            st.write(f"{laptop_details['brand']}")
            st.write(f"{laptop_details['processor']}")
            st.write(f"{laptop_details['ram']} GB")
            st.write(f"{laptop_details['storage']} GB")
            st.write(f"{laptop_details['os']}")
            st.write(f"RM {laptop_details['price']}")



#***** DISPLAY MORE DETAILS *****
def display_more_details(laptop_name):
    laptop_details = laptops[laptops['name'] == laptop_name].iloc[0]  # Get the first match (there should be only one)

    if laptop_details is not None:
        # Create two columns
        st.write(f"{laptop_details['name']}")
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



#----- RECOMMENDATION BUTTON -----
recommendation_button = st.button('Recommend', key='recommendation_button')    
if recommendation_button or st.session_state.get("recommended_state", False):
    st.session_state["recommended_state"] = True
    st.write("**HERE ARE SOME RECOMMENDATIONS FOR YOU**")
    recommended_names, recommended_images, similarity_scores = recommend(selected_laptop)
    cols = st.columns(5)

    for i in range(5):
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

st.write(st.session_state)