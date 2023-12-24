import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import lightgbm


@st.cache_data
def get_data():
    df = pd.read_csv("games_detailed_info.csv")
    return df

st.set_page_config(layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/BoardGameGeek_Logo.svg/1200px-BoardGameGeek_Logo.svg.png", width=400)
st.title("🎲:red[KUTU] :blue[OYUNU SEÇME] :red[ARACI]🎲")

st.header("🪀KUTU OYUNU SEÇME ARACI🪀")
tab_home, tab_rec, tab_ml = st.tabs(["Ana Sayfa", "Oyun Tavsiyesi", "Rating Tahmini(ML)"])
tab_home.markdown("Kutu oyunları için bir tavsiye sistemi oluşturduk.")

# st.subheader("PROJE AŞAMALARI")
# st.image("pic66668.jpg", width=100)

column_bgg, column_recommender = tab_home.columns([2,1], gap="small")

column_bgg.subheader("Recommendation System")
column_bgg.markdown("Öyle yaptık böyle yaptık")
column_recommender.subheader("Machine Learning")
column_recommender.markdown("Öyle oldu böyle oldu")
# sidebar
st.sidebar.image("https://cf.geekdo-images.com/-Qer2BBPG7qGGDu6KcVDIw__original/img/PlzAH7swN1nsFxOXbfUvE3TkE5w=/0x0/filters:format(png)/pic2452831.png")
st.sidebar.image("https://cf.geekdo-images.com/T1ltXwapFUtghS9A7_tf4g__original/img/xIAzJY7rl-mtPStRZSqnTVsAr8Y=/0x0/filters:format(jpeg)/pic1401448.jpg")
st.sidebar.image("https://cf.geekdo-images.com/EPdI2KbLVtpGWLgL_eJLFg__original/img/ahppJwWWpWQTzT8LR-2ObsjB7OY=/0x0/filters:format(jpeg)/pic5885690.jpg")

# rectab
df = get_data()
tab_rec.subheader("Tavsiye Sistemi")

selected_game = tab_rec.selectbox(label="KUTU OYUNU", options=df["primary"].unique(), help="Lütfen bir oyun ismi seçiniz.")
tab_rec.write(f"Seçilen oyun: { selected_game}")
filtered_df = df[df.primary == selected_game]
if tab_rec.button('Oyun Tavsiye Et!'):
    tab_rec.write('Oyun bilgileri geldi!')
    tab_rec.image(df[df['primary'] == selected_game]['thumbnail'].iloc[0])

fig = px.scatter(df[:100], x="average", y="yearpublished", size="usersrated", color="averageweight",
           hover_name="primary", color_continuous_scale='reds')
# fig.add_hline(y=10, line_dash="dash", line_color="black")
fig.update_yaxes(range=["1990", "2021"])
fig.update_xaxes(range=["6", "9"])
tab_rec.plotly_chart(fig, use_container_width=True)

fig = px.scatter(df[:100], x="yearpublished", y="average", size="usersrated", color="averageweight",
           hover_name="primary", color_continuous_scale='reds')
# fig.add_hline(y=10, line_dash="dash", line_color="black")
fig.update_yaxes(range=["5", "10"])
fig.update_xaxes(range=["1990", "2021"])
tab_rec.plotly_chart(fig, use_container_width=True)

# tab_ml



# modele beslemek için gerekli seçimleri yap
tab_ml.markdown("<h1 style='text-align: center; '>Oyununuz için değerleri seçiniz</h1>", unsafe_allow_html=True)

# sütunlara ayır
column_one, column_two, column_three = tab_ml.columns([3, 3, 3], gap="small")

def load_model():
    return joblib.load("deneme_2_lgbm_model.joblib")

model = load_model()
def user_input_features():
    # Create user input fields here.
    feature1 = yearpublished
    feature2 = minplayers
    feature3 = maxplayers
    options = ["Family_Game", "Strategy_Game", "Heavy_Game", "Party_Game", "Children's_Game"]
    selected_options = column_one.multiselect("Select game types:", options)

    # Sort options and drop the first category (alphabetically)
    dropped_first_option = sorted(options)[0]  # 'Children's_Game' is dropped
    options_without_first = [opt for opt in options if opt != dropped_first_option]

    # Initialize the DataFrame for NEW_CAT with zeros for the remaining categories
    new_cat_df = pd.DataFrame(columns=options_without_first)
    new_cat_df.loc[0] = [0] * len(options_without_first)

    # Mark selected options as 1, except for the first one
    for option in selected_options:
        if option in new_cat_df.columns:
            new_cat_df.at[0, option] = 1

    # Assembling the data
    data = {'yearpublished': feature1, 'minplayers': feature2, 'maxplayers': feature3}
    features_df = pd.DataFrame(data, index=[0])

    return pd.concat([features_df, new_cat_df], axis=1)

# Slider inputs (example values, adjust according to your data)
yearpublished = column_two.slider('Choose Year Published', 1900, 2023)
maxplayers = column_one.slider('Choose Max Number of Players', 1, 10)
minplayers = column_one.slider('Choose Min Number of Players', 1, 10)

tab_ml = st.container()
tab_ml.write("# Model Prediction")
input_df = user_input_features()

# Display the user input features
# tab_ml.write("## User Input features")
# tab_ml.write(input_df)

if tab_ml.button('Predict'):
    prediction = model.predict(input_df)
    tab_ml.write("Oyunun tahmin edilen ratingi:")
    tab_ml.write(prediction)

number = tab_ml.slider('Pick a number', 0, df["Unnamed: 0"].max())
tab_ml.image(df[df['Unnamed: 0'] == number]['thumbnail'].iloc[0])
tab_ml.write(df[df["Unnamed: 0"] == number]["primary"].iloc[0])
tab_ml.write("CD")