#.\env\Scripts\Activate
# streamlit run app.py

#find icon here https://fonts.google.com/icons
import streamlit as st
st.set_page_config(
    page_title="FYP",
    page_icon='💻', 
    layout='wide')


# --- PAGES SETUP --- 
about_me_page = st.Page(
    page="pages/about-me.py",
    title="About Me",
    icon=":material/account_circle:",
)

about_project_page = st.Page(
    page="pages/about-project.py",
    title="About Project",
    icon=":material/help:",
    default=True
)

project_page = st.Page(
    page="pages/combined.py", 
    title="START HERE", 
    icon=":material/laptop_chromebook:",
)

project_analysis_page = st.Page(
    page="pages/analysis.py",
    title="Analysis",
    icon=":material/monitoring:",
)

#tf_no_slider, RF_only, tf_slider

# --- NAVIGATION SETUP [without sections] ---
#pg = st.navigation(pages=[about_page, project_page])

# --- NAVIGATION SETUP [with sections] ---

pg = st.navigation(
    {
        "INFO":[about_project_page, about_me_page],
        "PROJECT":[project_page, project_analysis_page],
    }
)

# --- SHARE ON ALL PAGES ---
#st.logo("")
st.sidebar.text("Laptop RS by Aiman")

# --- RUN NAVIGATION ---
pg.run()
