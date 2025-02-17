#PAGE ANALYSIS 
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go

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
    p.model {
        font-size: 14px; 
        color: black;
        font-family: "Trebuchet MS", sans-serif;
    }
    p.number {
        font-size: 50px;
        color: black;
        text-align: center;
        border-radius: 10px;
        font-weight: bold;
    }
            
    p.header {
        font-size: 20px;
        text-align: center;
        margin: 0;
    }
            
    p.min_price {
        font-size: 20px;
        color: green;    
        font-weight: bold;
    }

    p.max_price {
        font-size: 20px;
        color: red; 
        font-weight: bold;
    }
            
    div.outer {
        display: flex; 
        justify-content: space-around; 
    }
            
    div.inner {
        padding: 10px; 
        background-color: white; 
        border-radius: 10px; 
        width: 350px; 
        text-align: center;  
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">DATA VISUALISATION</p>', unsafe_allow_html=True)

# Load the data
laptops = pickle.load(open('model/analysis.pkl', 'rb'))
data = pickle.load(open('model/df_combined.pkl', 'rb'))

#---LAPTOP USECASE DISTRIBUTION---
#To count occurrences of each brand
use_df = laptops['usecases'].value_counts().reset_index()
use_df.columns = ['usecases', 'count']  # Rename columns

fig_use_dist = px.pie(
    use_df,
    names='usecases',
    values='count',
    labels={'usecases': 'Laptop Use case', 'count': 'Number of Laptops'},
    #text='count'  #display count on top of each bar
    template="gridon",
)
fig_use_dist.update_traces(
    textfont=dict( #Label edit
        size=15, 
        color='white' 
    )
)


st.plotly_chart(fig_use_dist)
opt = st.selectbox('Choose Laptop Type:', ['', 'Gaming', 'Hybrid', 'Office'])

 
if opt == '':
        st.error('Choose laptop type to see more details', icon=":material/error:")
else:   
    gaming_laptops = laptops[laptops['usecases'] == opt]

    #---LAPTOP BRAND DISTRIBUTION---
    #To count occurrences of each brand
    brand_df = gaming_laptops['laptop_brand'].value_counts().reset_index()
    brand_df.columns = ['laptop_brand', 'count']  # Rename columns
    #brand_counts = brand_counts.sort_values(by='count', ascending=False)
    fig_brand_dist = px.bar(
        brand_df,
        x='laptop_brand',
        y='count',
        orientation='v', #can use h as horizontal
        color_discrete_sequence=["#0083BB"] * len(brand_df),
        #color_discrete_sequence=px.colors.qualitative.Set3, px.colors.sequential.RdBu
        labels={'laptop_brand': 'Laptop Brand', 'count': 'Number of Laptops'},
        text='count',  #display count on top of each bar
        template="plotly_white", #https://plotly.com/python/templates/
    )
    fig_brand_dist.update_traces( #update the bar chart
        textposition='outside',  #set the label position
        textfont=dict(size=13)  
    )
    fig_brand_dist.update_layout( #update layout for better appearance
        title={
            'text': '<b>LAPTOP BRAND DISTRIBUTION</b>', 
            'x': 0.5,  # Center title (0 is left, 1 is right)
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        xaxis=dict(showgrid=False),    #remove gridlines on x-axis
        yaxis=dict(showgrid=False)     #remove gridlines on y-axis
    )

    
    #---LAPTOP OPERATING SYSTEM DISTRIBUTION---
    #To count occurrences of each brand
    os_df = gaming_laptops['os_brand'].value_counts().reset_index()
    os_df.columns = ['os_brand', 'count']  # Rename columns
    # Create a bar chart using Plotly Express
    fig_os_dist = px.pie(
        os_df,
        names='os_brand',
        values='count',
        labels={'os_brand': 'Laptop Operating System', 'count': 'Number of Laptops'},
        #text='count'  #display count on top of each bar
        template="gridon",
    )
    fig_os_dist.update_traces(
        textfont=dict( #Label edit
            size=10, 
            color='white' 
        )
    )
    fig_os_dist.update_layout(
        title={
            'text': '<b>LAPTOP OS DISTRIBUTION</b>',
            'x': 0.5,
            'xanchor': 'center',
        }
    )
    #---LAPTOP PRICE EACH BRAND DISTRIBUTION---
    min_max_brand_df = gaming_laptops[['laptop_brand', 'price_rm']]
    min_max_brand_df = gaming_laptops.groupby('laptop_brand')['price_rm'].agg(['min', 'max']).reset_index()
    min_max_brand_df.columns = ['Laptop Brand', 'Minimum Price', 'Maximum Price']
    # --- OPTIONAL: VISUALIZE AS A BAR CHART ---
    fig_price_brand_dist = px.bar(
        min_max_brand_df,
        x='Laptop Brand',
        y=['Minimum Price', 'Maximum Price'],
        barmode='group',  # Group bars for min and max side by side
        labels={'value': 'Price (RM)', 'variable': 'Price Type'},  # Label axes
        template='plotly_white',
    )
    fig_price_brand_dist.update_layout( #update layout for better appearance
        title={
            'text': '<b>PRICE DISTRIBUTION</b>', 
            'x': 0.5,  # Center title (0 is left, 1 is right)
            'y': 0.9,  # Move title up a bit
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        xaxis=dict(showgrid=False),    #remove gridlines on x-axis
        yaxis=dict(showgrid=False),    #remove gridlines on y-axis
        barmode='stack',
    )
    
    #---LAPTOP PRICE EACH USECASE DISTRIBUTION---
    min_price = gaming_laptops["price_rm"].min()
    max_price = gaming_laptops["price_rm"].max()
    # Get the models of the cheapest and most expensive laptops
    cheapest_laptop = gaming_laptops[gaming_laptops["price_rm"] == min_price].iloc[0]
    most_expensive_laptop = gaming_laptops[gaming_laptops["price_rm"] == max_price].iloc[0]
    # Extract the model names
    cheapest_model = cheapest_laptop["name"]
    most_expensive_model = most_expensive_laptop["name"]
    st.markdown(
        f"""
        <div class="outer">
            <div class="inner">
                <p class="min_price">CHEAPEST LAPTOP</p>
                <p class="number">RM {min_price:.2f}</p>
                <p class="model"">{cheapest_model}</p>
            </div>
            <div class="inner">
                <p class="max_price">MOST EXPENSIVE LAPTOP</p>
                <p class="number">RM {max_price:.2f}</p>
                <p class="model"">{most_expensive_model}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("\n\n")
    st.plotly_chart(fig_brand_dist)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_price_brand_dist)
    with col2:
        st.plotly_chart(fig_os_dist)
        
    
