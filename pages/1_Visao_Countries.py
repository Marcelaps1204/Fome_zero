import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title= 'Visão Countries', page_icon =' ', layout='wide')

#=========================================================
#---------------------- FUNÇÕES --------------------------
#=========================================================

def avg_cost (df1):
    Avg_price = df1[['Average Cost for two', 'Country Code']].groupby('Country Code').mean().reset_index()
    Avg_price.columns = ['País', 'Média Valor de um Prato para Duas Pessoas']
    fig = px.bar(Avg_price, x='País', y='Média Valor de um Prato para Duas Pessoas', title='Média de Preços de um Prato para Duas Pessoas por País', text_auto=True)
    return fig

def avg_countries (df1):
    df1_votes1 = df1.loc[:, ['Country Code', 'Votes']].groupby('Country Code').mean().sort_values('Votes', ascending=False).reset_index()
    df1_votes1.columns = ['País', 'Avaliações']
    fig = px.bar(df1_votes1, x='País', y='Avaliações', title='Média de Avaliações Feitas por País', text_auto=True)
    return fig


def cities_countries (df1):    
    df1_city = df1.loc[:, ['Country Code', 'City']].groupby('Country Code').nunique().sort_values('City', ascending= False).reset_index()
    df1_city.columns = ['País', 'Cidade']
    fig = px.bar(df1_city, x='País', y='Cidade', title='Quantidade de Cidades Registrados por País', text_auto=True)
    return fig

def restaurants_countries (df1):
    df1_rest = df1.loc[:,['Restaurant ID', 'Country Code']].groupby('Country Code').nunique().sort_values('Restaurant ID', ascending= False).reset_index()
    df1_rest.columns = ['País', 'Restaurantes']
    fig = px.bar(df1_rest, x='País', y='Restaurantes', title='Quantidade de Restaurantes Registrados por País', text_auto=True)
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

linhas_selecionadas = df1['Country Code'].isin(countries)
df1 = df1.loc[linhas_selecionadas,:]
    

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')


#========================================================
#------------------- Layout Streamlit--------------------
#========================================================
st.markdown('### 🌏  Visão Países ')
st.markdown("""___""")
st.markdown('### Seu Restaurante Favorito está Aqui')
st.markdown("""___""")

with st.container():
    fig = restaurants_countries(df1)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    fig = cities_countries (df1)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        fig = avg_countries(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = avg_cost(df1)
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    st.markdown('Média de Valor de um Prato para Duas Pessoas de Acordo com o País e Moeda Corrente')
    f1_avg = df1.loc[:,['Country Code', 'Average Cost for two', 'Currency']].groupby(['Country Code', 'Currency']).mean().reset_index()
    st.dataframe (f1_avg, use_container_width=True)
