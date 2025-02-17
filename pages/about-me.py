#PAGE ABOUT ME/AUTHOR
import streamlit as st

#--- HERO SECTION ---
st.title("ABOUT ME")
@st.dialog("Scan Me")
def contact():
    col1, col2 = st.columns(2)
    with col1:
        st.text("LinkedIn")
        st.image(r"templates/LinkedinCode.PNG", width=100)
    with col2:
        st.text("GitHub")
        st.image(r"templates/GithubCode.PNG", width=100)
    

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image(r"templates\profile.jpg", width=200)
with col2:
    st.title("MUHAMMAD AIMAN BIN MD ELIAS", anchor=False)
    st.write("BACHELOR OF COMPUTER SCIENCE, UITM SHAH ALAM")
    if st.button("Contact Me"):
        contact()

st.text("\n\n")
st.subheader("MY RESUME")
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
  st.image(r"templates\resume1.jpg", width=800)
with col2:
  st.image(r"templates\resume2.jpg", width=800)