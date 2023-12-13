import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def get_data():
    df = pd.read_csv("games_details.csv")
    return df

st.set_page_config(layout="wide")

st.title("🎲:red[KUTU] :blue[OYUNU SEÇME] :red[ARACI]🎲")

st.header("🪀KUTU OYUNU SEÇME ARACI")
tab_home, tab_rec, tab_ml = st.tabs(["Ana Sayfa", "Oyun Tavsiyesi", "Puan Tahmini(ML)"])

column_bgg, column_recommender = st.columns([2,1], gap="small")

tab_home.markdown("Kutu oyunları için bir tavsiye sistemi oluşturduk.")

column_bgg.image("pic66668.jpg", width=100)

st.subheader("Proje Aşamaları")

number = tab_ml.slider('Pick a number', 0, 1000)
# option = st.sidebar.selectbox('Select a number', range(1, 11))

if tab_rec.button('Oyun Tavsiye Et!'):
    tab_rec.write('Tavsiyeler Geldi!')



# recbox
df = get_data()
tab_rec.subheader("Tavsiye Sistemi")

selected_game = tab_rec.selectbox(label="KUTU OYUNU", options=df["primary"].unique(), help="Lütfen bir oyun ismi seçiniz.")
tab_rec.write(f"Seçilen oyun: { selected_game}")
filtered_df = df[df.primary == selected_game]

tab_rec.dataframe(df, width=1200)

fig = px.scatter(df[:100], x="yearpublished", y="average", size="usersrated", color="playingtime",
           hover_name="primary")
fig.add_hline(y=10, line_dash="dash", line_color="black")
fig.update_xaxes(range=["1993", "2020"])
tab_rec.plotly_chart(fig, use_container_width=True)
