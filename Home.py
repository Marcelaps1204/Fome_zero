import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config (
    page_title= 'Home',
    page_icon=' ')

#image_path='Documents/REPOS/FTC_python_CDS/Dataset/delivery-man-g35bcb24a6_1280.png'




#=========================================================
#---------------------- FUNÇÕES --------------------------
#=========================================================


# Country Code
COUNTRIES = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zeland',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapure',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'United Arab Emirates',
    215: 'England',
    216: 'United States of America',
}
def country_name(country_id):
    return COUNTRIES [country_id]
# Essa função vai atribuir nomes de países aos códigos, trocando eles, usando o lambda x, trocamos toda coluna Country Code


def create_price_type(price_range):
    if price_range == 1:
        return 'cheap'
    elif price_range == 2:
        return 'normal'
    elif price_range == 3:
        return 'expensive'
    else:
        return 'gourmet'
    
    
# Criação do nome das cores
COLORS = {
    '3F7E00':'darkgreen',
    '5BA829':'green',
    '9ACD32':'lightgreen',
    'CDD614':'orange',
    'FFBA00':'red',
    'CBCBC8':'darkred',
    'FF7800':'darkred',
}

def color_name(color_code):
    return COLORS [color_code]

def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df1.iterrows():

        name = line["Restaurant Name"]
        price_for_two = line["Average Cost for two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate rating"]
        color = line["Rating color"]

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)
    
    
#def adjust_columns_order(df1):
    #df1 = df1.copy()

    #new_cols_order = [
        #"Restaurant ID",
        #"Restaurant Name",
        #"Country Code",
        #"City",
        #"Address",
        #"Locality",
        #"Locality Verbose",
        #"Longitude",
        #"Latitude",
        #"Cuisines",
        #"price_type",
        #"Average Cost for two",
        #"Currency",
        #"Has Table booking",
        #"Has Online delivery",
        #"Is delivering now",
        #"Price range",
        #"Aggregate rating",
        #"Rating color",
        #"color_name",
        #"Rating text",
        #"Votes",
    #]

    #return df1.loc[:, new_cols_order]





    
#=========================================================
#----------------- LIMPEZA DATASET -----------------------
#=========================================================


def clean_code(df1):

# aLterando a coluna Country Code pelo nome do País usando a função lambda
    df1['Country Code'] = df1.apply(lambda x: country_name(x['Country Code']), axis = 1)

# Alterando a coluna Price range
    df1['Price range'] = df1.apply(lambda x: create_price_type(x['Price range']), axis = 1)

# Alterando o código de cor para o nome da cor
    df1['Rating color'] = df1.apply(lambda x: color_name(x['Rating color']), axis = 1)
#df1["color_name"] = df1.loc[:, "Rating color"].apply(lambda x: color_name(x))
# Categorizar os restaurantes somente por um tipo de culinária

    df1['Cuisines'] = df1.loc[:, 'Cuisines'].astype(str).apply(lambda x: x.split(",")[0])

    linhas_selecionadas = df1['Cuisines'] != 'nan'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1 = df1.dropna(subset=['Cuisines'])

# Excluindo linhas duplicadas
    df1 = df1.drop_duplicates()
    
    return df1

df = pd.read_csv('zomato.csv')
df1 = clean_code (df)



#===========================================
#-----------------Barra Lateral-------------
#===========================================


st.header('FOME ZERO')
st.sidebar.markdown ('# FOME ZERO')

image_path='fome_zero1.jpg'
image=Image.open(image_path)

st.sidebar.image(image, width=280)

#st.sidebar.markdown('## Fome Zero')
st.sidebar.markdown('#### Seu apetite em primeiro lugar')
st.sidebar.markdown("""___""")

#st.sidebar.markdown('##Selecione uma data limite')
#date_slider = st.sidebar.slider(
    #'Até qual valor?', 
    #value=pd.datetime(2022, 4, 13),
    #min_value=pd.datetime(2022, 2, 11),
    #max_value=pd.datetime(2022, 4, 6),
    #format='DD-MM-YYYY')

#st.header(date_slider)
#st.sidebar.markdown("""___""")


countries=st.sidebar.multiselect(
    'Escolha os Países que Deseja Visualizar os Restaurantes?',
    df1.loc[:, "Country Code"].unique(),
    default=['Brazil','Australia','England', 'United States of America', 'India'])
    

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# filtro de datas
#linhas_selecionadas = df1['Order_Date'] < date_slider
#df1 = df1.loc[linhas_selecionadas,:]

# filtro de trânsito
#linhas_selecionadas = df1['Country Code'].isin(countries)
#df1 = df1.loc[linhas_selecionadas,:]

#st.dataframe(df1)



#========================================================
#------------------- Layout Streamlit--------------------
#========================================================
st.markdown("""___""")
st.markdown('## Seu Restaurante Favorito está Aqui')
st.markdown("""___""")
st.markdown('### Temos aqui as seguintes marcas:')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    with col1:
        rest = df1['Restaurant ID'].nunique()
        col1.metric('Restaurantes Cadastrados', rest)
    
    with col2:
        country = df1['Country Code'].nunique()
        col2.metric('Países Cadastrados', country)
        
    with col3:
        cities = df1['City'].nunique()
        col3.metric('Cidades Cadastradas', cities)
        
    with col4:
        vote = df1['Votes'].sum()
        col4.metric('Avaliações Feitas na Plataforma', vote)
        
    with col5:
        cuisine = df1['Cuisines'].nunique()
        col5.metric('Tipos de Culinária Oferecidas', cuisine)

        
with st.container():
    create_map(df1)


   
