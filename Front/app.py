#Importación librerias
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie


warnings.filterwarnings("ignore")

  
#Lottie Animaciones
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Se ingresa el link de la animacion 

#Animation 1
lottie_url_predict = "https://assets3.lottiefiles.com/packages/lf20_A6VCTi95cd.json"

lottie_predict = load_lottieurl(lottie_url_predict)

#Animation 2
lottie_url_predict_comment = "https://assets9.lottiefiles.com/packages/lf20_w5h94x9x.json"

lottie_predict_comment = load_lottieurl(lottie_url_predict_comment)

# FastAPI endpoint
url = 'http://fastapi:8000/predict/?'

#MENU 
# Funcion para reducir el margen top
def margin(): 
    st.markdown("""
            <style>
                .css-18e3th9 {
                        padding-top: 1rem;
                        padding-bottom: 10rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
                .css-1d391kg {
                        padding-top: 3.5rem;
                        padding-right: 1rem;
                        padding-bottom: 3.5rem;
                        padding-left: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)



        
#MENU 
EXAMPLE_NO = 1


def streamlit_menu(example=1):
    
    if example == 1:
        # Tipo de menu sidebar 
        with st.sidebar:
            
            selected = option_menu(
                menu_title="Menú",  # require
                options=["Home","Prediction","Youtube Prediction"],  #require
                icons=["house", "heart", 'heart'],  # optional
                #menu_icon= "cast",  # optional
                default_index=0,  # optional
                styles={
                    "menu-icon":"Data",
                    
                    "menu_title":{"font-family": "Tahoma"},
                    "nav-link": {"font-family": "Tahoma", "text-align": "left", "margin":"0px",},
                    #"nav-link-selected": {""}, 
                    })
        return selected



selected = streamlit_menu(example=EXAMPLE_NO)

# Home
if selected == "Home":

    st.markdown("<h1 style='text-align: center; color: purple;'>DeepIA Tech</h1>", unsafe_allow_html=True)
   
    container = st.container()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')
#Se sube el logo y se centra
    with col2:
        st.image("Healthy.png")

    with col3:
        st.write(' ')
    
    
    st.markdown("<h5 style='text-align: justify; color: black;'>DeepIA Tech is a consultancy in which we are in charge of finding technological solutions. Our team is made up of data analytics, Artificial Intelligence developers and specialists in marketing and web design.</h5>", unsafe_allow_html=True)

    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")

    col1, col2, col3 = st.columns(3)

    with col1:
       st.image("./twiter_logo.png")

    with col2:
       st.image("./instagram_logo.png")

    with col3:
       st.image("./youtube_logo.png")

    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
#Descripcion de la empresa
    st.markdown("<h5 style='text-align: justify'>Healthy Comments is an application for the analysis of comments, as in social networks, which helps us to identify whether they are toxic or not, using Machine Learning. We want to continue developing our tool to make it more versatile and even to be able to automatically restrict harmful comments towards other people.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify'>We have technical support that helps to maintain the tool constantly and we offer training to the companies.</h5>", unsafe_allow_html=True)

    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
    st.image("./BigML-Dataset.png")

#Paginas 
if selected== "Prediction":
    
    margin()


    st.markdown("<h1 style='text-align: center; color: purple;'>Healthy comments</h1>", unsafe_allow_html=True)

    container = st.container()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:

        st_lottie(lottie_predict_comment, key="predict",
        speed=2,
        reverse=True,
        loop=True,
        quality="low", # medium ; high
        
        height=200,
        width=200,
        ) 

    

    form = st.form("my_form")
    prompt = form.text_area("Insert comment here:")



    # Fast-API Connection:
    if form.form_submit_button("Show Result"):
        #the request URL must be "api.8000" because "api" is the name of the backend service in the docker compose file
        request_text = f"http://api:8000/predict?prompt=${prompt}"
        
        response = requests.get( request_text, json=prompt)
        
        prediction = response.text
        st.success(f"The result of your comment is: {prediction}")
    
if selected== "Youtube Prediction":

    st.markdown("<h1 style='text-align: center; color: purple;'>Healthy comments</h1>", unsafe_allow_html=True)

    container = st.container()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:

            st_lottie(lottie_predict, key="predict",
            speed=2,
            reverse=True,
            loop=True,
            quality="low", # medium ; high
            
            height=200,
            width=200,
            ) 


        #Youtube Scrapper
            form2 = st.form("Youtube Comment")
            youtube_videoId = form2.text_input("Youtube video comments")
            print(type(youtube_videoId))


    # Conexión con la api:
            if form2.form_submit_button("Show result"):
                request_text2 = f"http://api:8000/predict_youtube_comment?prompt={youtube_videoId}"
                print(request_text2)
                response2 = requests.get(request_text2)
                prediction2 = response2.text
                st.success(f"Result: {prediction2}")

    









