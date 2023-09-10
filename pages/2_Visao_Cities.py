import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title= 'Visão Cities', page_icon =' ', layout='wide')

#=========================================================
#---------------------- FUNÇÕES --------------------------
#=========================================================

def different_cuisines (df1):
    df3 = df1.loc[:, ['City', 'Cuisines','Country Code']].groupby(['City', 'Country Code']).nunique().sort_values('Cuisines', ascending=False).reset_index()
    df3.columns = ['Cidade', 'País', 'Tipos de Culinária']
    df3 = df3.head(10)
    fig = px.bar(df3, x='Cidade', y= 'Tipos de Culinária', color='País', text_auto=True)
    return fig

def low_rating (df1):
    rest_menos2 = df1['Aggregate rating'] <= 2.5
    df2 = df1.loc[rest_menos2, :]
    df3 = df2.loc[:,['City', 'Restaurant ID', 'Country Code']].groupby(['City', 'Country Code']).count().sort_values('Restaurant ID',ascending=False).reset_index()
    df3.columns = ['Cidade', 'País', 'Restaurantes']
    df3 = df3.head(7)
    fig = px.bar(df3, x='Cidade', y= 'Restaurantes', color='País', text_auto=True)
    return fig

def high_rating (df1):
    rest_mais4 = df1['Aggregate rating'] >= 4.0
    df2 = df1.loc[rest_mais4, :]
    df3 = df2.loc[:,['City', 'Country Code', 'Restaurant ID']].groupby(['City','Country Code']).count().sort_values('Restaurant ID', ascending=False).reset_index()
    df3 = df3.head(7)
    df3.columns = ['Cidade', 'País', 'Restaurantes']
    fig = px.bar(df3, x='Cidade', y= 'Restaurantes', color='País', text_auto=True)
    return fig

def top_restaurants_cities (df1):
    df1_aux = df1.loc[:, ['City', 'Restaurant ID', 'Country Code']].groupby(['City', 'Country Code']).nunique().sort_values('Restaurant ID', ascending=False)
    df1_aux1 = df1_aux.head(10).reset_index()
    df1_aux1.columns = ['Cidade', 'País', 'Restaurantes']
    fig = px.bar(df1_aux1, x='Cidade', y='Restaurantes', color='País', text_auto=True)
    return fig

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
    
    
df = pd.read_csv('zomato.csv')
df1 = df.copy()


    
#=========================================================
#----------------- LIMPEZA DATASET -----------------------
#=========================================================

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

#linhas_selecionadas = df1['Country Code'].isin(countries)
#df1 = df1.loc[linhas_selecionadas,:]


#https://www.youtube.com/watch?v=YClmpnpszq8

#========================================================
#------------------- Layout Streamlit--------------------
#========================================================

st.markdown('### 🌆    Visão Cidades')
st.markdown("""___""")
st.markdown('#### Seu Restaurante Favorito está Aqui')
st.markdown('##### Top 10 Cidades com Mais Restaurantes na Base da Dados')
    
with st.container():
    fig = top_restaurants_cities (df1)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('###### 7 Cidades com Restaurantes com Média de Avaliação Acima de 4')
        fig = high_rating (df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('###### 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2,5')
        fig = low_rating (df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
with st.container():
    st.markdown('###### Top 10 Cidades com Restaurantes e Tipos de Culinária Distintos')
    fig = different_cuisines (df1)
    st.plotly_chart(fig, use_container_width=True)
