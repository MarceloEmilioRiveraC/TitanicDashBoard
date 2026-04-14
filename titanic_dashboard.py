import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Titanic Data Insights", layaout = "wide")
st.title("Titanic Passanger Dashboard")
st.markdown("Explore the demographics and survival rates of passengers")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    df['Survived'] = df['Survived'].map({0: 'Perished', 1: 'Survived'})
    df['Pclass'] = df['Pclass'].map({1: 'First Class', 2: 'Second Class', 3: 'Third Class'})
    return df
df = load_data() 

st.sidebar.header("Filter Options")
gender_filter = st.sidebar.multiselect("" 
    "Select Gender: ", 
    options = df['Sex'].unique(),
    default = df['Sex'].unique()
)
class_filter = st.sidebar.multiselect(
    "Select Class: ",
    options = df['Pclass'].unique(),
    default = df['Pclass'].unique()
)

filtered_df = df[(df['Sex'].isin(gender_filter)) & (df['Pclass'].isin(class_filter))]

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("Total Passengers with these characteristics", len(filtered_df))
with col2:
    survival_rate = (filtered_df['Survived'] == 'Survived').mean() * 100
    st.metric("Survival Rate", f"{survival_rate:.1f}%")
with col3:
    avg_fare = filtered_df['Fare'].mean()
    st.metric("Average Fare", f"${avg_fare:.2f}")

st.divider()
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.subheader("Survival Count by Gender")
    fig_sex = px.histgram(
        filtered_df,
        x = 'Sex',
        color = 'Survived',
        barmode = 'group',
        color_discrete_map = {'Survived': '#2ecc71', 'Perished': 'red'}
        )
    st.plotly_chart(fig_sex, use_container_width= True , config = {'displaylogo': False})

with row2_col2:
    st.subheader('Age Distribution of Passengers')
    fig_age = px.histogram(filtered_df, x = 'Age', color = 'Survived', nbins = 30, color_discrete_map = {'Survived': '#2ecc71', 'Perished': 'red'})
    st.plotly_chart(fig_age, use_container_width= True , config = {'staticPlot': False})

st.subheader("Raw Data Header")
st.dataframe(filtered_df.head(10), width= "Stretch")
