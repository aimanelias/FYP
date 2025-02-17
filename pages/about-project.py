#PAGE ABOUT PROJECT
import streamlit as st

#--- MORE ABOUT PROJECT ---
col1, col2 = st.columns(2)
with col1:
  st.image("templates/logo.jpg", width=250)
with col2:
  st.title("ABOUT PROJECT")
  st.write("\n\n")
  st.subheader("FINAL YEAR PROJECT - CSP650", anchor=False)

""" """
st.write("\n\n")
st.write(
    """
    Welcome to the **Laptop Recommendation System**, a web-based application designed to help users find laptops that match their preferences. This system leverages powerful text analysis and machine learning techniques to recommend the most relevant laptops based on a set of features and user inputs. 
    Same as movie recommendation system, it is designed to find similar movies to suggest to users based on their preferences.
    
    ### Problem Statement:
    Due to rapid advancements in technology, the laptop market has become increasingly complex, with numerous options available to consumers. This lead to the problem for the user to find and compare the laptops that match their needs. 
    
    ### Purpose:
    The goal of this project is to help and compare the most similar laptops based on laptop specifications due to the largest number of laptops nowadays, it is quite challenging and time consuming to compare them manually.
    This project aims to simplify the laptop search process, saving users time and effort by presenting them with the most relevant recommendations based on their input.

    
    ### Key Features:
    - **TF-IDF (Term Frequency - Inverse Document Frequency)**: 
      - This technique is used to transform textual data (laptop specifications) into numerical vectors, highlighting the most significant terms while downplaying less informative words.
    - **Random Forest Classification**:
      - The vector is used as input training model, which predicts the use case or type of laptop (Gaming, Hybrid, Office) based on user inputs.
    - **Cosine Similarity**:
      - After predicting the laptop type, cosine similarity is applied to recommend the 5 most similar laptops. This ensures users receive personalized recommendations that align closely with their specified preferences.
    - **Web-Based Application**:
      - Built using the **Streamlit framework**, this system provides a user-friendly interface, allowing users to interact seamlessly by entering laptop specifications (e.g., brand, CPU, RAM, storage).
    

    ### How It Works:
    1. **Input**: Users provide detailed laptop specifications (brand, CPU, RAM, storage, etc.).
    2. **TF-IDF Transformation**: The textual features are converted into numerical vectors using TF-IDF.
    3. **Prediction**: The vectors are passed into a Random Forest model, which predicts the laptop use case/type.
    4. **Similarity Calculation**: Using cosine similarity, the system compares the input laptop to others in the dataset.
    5. **Output**: The top 5 most similar laptops are recommended and displayed on the system interface.

    
    ### Technologies Used:
    - **Python**
    - **Streamlit** (for web-based interface)
    - **TF-IDF** (for text vectorization)
    - **Random Forest Classifier** (for use case prediction)
    - **Cosine Similarity** (for measuring item similarity)
    - **Pandas** and **NumPy** (for data manipulation)

    I hope this simple project helps you find the perfect laptop with ease. Thank You!
    """
)
