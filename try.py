#.\env\Scripts\Activate
#streamlit run try.py

#TRYING TO USE SESSION STATE
import pandas as pd
import pickle
import streamlit as st

# Set up initial session state for both button display texts
if 'button1_text' not in st.session_state:
    st.session_state.button1_text = False
if 'button2_text' not in st.session_state:
    st.session_state.button2_text = False

# Display Button 1 and update its display state
if st.button("Button 1"):
    st.session_state.button1_text = True

# Display text for Button 1 if clicked
if st.session_state.button1_text:
    st.write("Text displayed from Button 1")

# Display Button 2 only if Button 1 has been clicked
if st.session_state.button1_text and st.button("Button 2"):
    st.session_state.button2_text = True

# Display text for Button 2 if clicked
if st.session_state.button2_text:
    st.write("Text displayed from Button 2")


st.write(st.session_state)




# Title to distinguish both approaches
st.title("Comparison of Button Handling Approaches")


# ----------------------------------------------
# Approach 1: Single Callback Function Approach
# ----------------------------------------------

# Initialize session state for display texts for each approach
if 'button1_text_callback' not in st.session_state:
    st.session_state.button1_text_callback = False
if 'button2_text_callback' not in st.session_state:
    st.session_state.button2_text_callback = False

st.header("1. Single Callback Function Approach")

# Callback function to handle both buttons
def button_callback(button_id):
    if button_id == 1:
        st.session_state.button1_text_callback = True
    elif button_id == 2:
        st.session_state.button2_text_callback = True

# Button 1 with callback for Approach 1
if st.button("Button 1 (Callback)", on_click=button_callback, args=(1,)):
    st.write("Button 1 clicked")

# Button 2 appears after Button 1 is clicked, uses the same callback function
if st.session_state.button1_text_callback:
    if st.button("Button 2 (Callback)", on_click=button_callback, args=(2,)):
        st.write("Button 2 clicked")

# Text display based on session state
if st.session_state.button1_text_callback:
    st.write("Button 1 was clicked - Text displayed from Button 1 (Callback)")
if st.session_state.button2_text_callback:
    st.write("Button 2 was clicked - Text displayed from Button 2 (Callback)")


# ----------------------------------------------
# Approach 2: Multiple Button Logic Approach
# ----------------------------------------------

st.header("2. Multiple Button Logic Approach")

if 'button1_text_logic' not in st.session_state:
    st.session_state.button1_text_logic = False
if 'button2_text_logic' not in st.session_state:
    st.session_state.button2_text_logic = False

# Button 1 for Approach 2 with its own logic
if st.button("Button 1 (Logic)"):
    st.session_state.button1_text_logic = True

# Display text for Button 1 if clicked
if st.session_state.button1_text_logic:
    st.write("Clicked button 1")

# Button 2 only appears if Button 1 has been clicked
if st.session_state.button1_text_logic and st.button("Button 2 (Logic)"):
    st.session_state.button2_text_logic = True

# Display text for Button 2 if clicked
if st.session_state.button2_text_logic:
    st.write("Clicked button 2")