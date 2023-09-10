import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
import utils as ut
import gudhi as gd
from folium.plugins import MarkerCluster

st.set_page_config(page_title= 'Visão Cuisines', page_icon =' ', layout='wide')

#=========================================================
#---------------------- FUNÇÕES --------------------------
#=========================================================

def worst_cuisines (df1):
    df1_06 = df1.loc[:, ['Aggregate rating', 'Cuisines']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=True).reset_index()
    df1_06.columns = ['Culinária', 'Média das Avaliações']
    df2 = df1_06.head(num_restaurantes)
    fig = px.bar(df2, x='Culinária', y='Média das Avaliações', text_auto=True)
    return fig

def best_cuisines (df1):
    df1_06 = df1.loc[:, ['Aggregate rating', 'Cuisines']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=False).reset_index()
    df1_06.columns = ['Culinária', 'Média das Avaliações']
    df2 = df1_06.head(num_restaurantes)
    fig = px.bar(df2, x='Culinária', y='Média das Avaliações', text_auto=True)   
    return fig

def high_cuisines (df1):
    maior_nota1 = df1['Aggregate rating'] == 4.9
    df2 = df1.loc[maior_nota1,:]
    maior_nota = df2[['Restaurant ID',  'Restaurant Name', 'Country Code',  'City', 'Cuisines', 'Aggregate rating', 'Votes']].sort_values('Restaurant ID', ascending=False)
    maior_nota2 = maior_nota.head(num_restaurantes) 
    return maior_nota2

# Função de melhores tipos culinarios
def melhor_restaurante (tipo):
    
    linhas_selecionadas = (df1['Cuisines'] == tipo) 
    df_aux01 = (df1.loc[linhas_selecionadas, ['Restaurant ID', 'Aggregate rating', 'Restaurant Name', 'Country Code']].groupby(['Restaurant ID', 'Restaurant Name'])).mean().sort_values(by='Aggregate rating').reset_index()
    maior_nota = df_aux01['Aggregate rating'].max()
    print(maior_nota)
    
    # Selecionando os que tem nota igual a maior
    linhas_selecionadas = (df_aux01['Aggregate rating'] == maior_nota)
    # Selecionando por ID
    df_aux01 = df_aux01.loc[linhas_selecionadas, :].sort_values(by='Restaurant ID')
    return df_aux01

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

#st.sidebar.markdown('## Selecione uma data limite')
#rest_slider = st.sidebar.slider (
 #   'Selecione a Quantidade de Restaurantes que Deseja Visualizar', 
  #  value='Restaurant ID', 
   # min_value=1,
    #max_value=20)
    


#st.header(rest_slider)
countries=st.sidebar.multiselect(
    'Escolha os Países que Deseja Visualizar os Restaurantes?',
    df1.loc[:, "Country Code"].unique(),
    default=['Brazil','Australia','England', 'United States of America', 'India'])

num_restaurantes = st.sidebar.slider('Escolha a quantidade de restaurantes a serem exibidos:', value=10, min_value=0, max_value=20)

cuisine=st.sidebar.multiselect(
    'Escolha os Tipos de Culinária?',
    df1.loc[:, 'Cuisines'].unique(),
    default=['BBQ','Brazilian','Japanese', 'Italian', 'Arabian'])

linhas_selecionadas = df1['Restaurant ID'] > num_restaurantes
df1 = df1.loc[linhas_selecionadas,:]

linhas_selecionadas = df1['Country Code'].isin(countries)
df1 = df1.loc[linhas_selecionadas,:]

    
st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

#========================================================
#------------------- Layout Streamlit--------------------
#========================================================

st.markdown('### 🍴  Visão Cuisines')
st.markdown("""___""")
st.markdown('#### Melhores Restaurantes dos Principais Tipos Culinários')

with st.container():
    
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        #Italian
        df_aux = melhor_restaurante('Italian')
        st.metric(label='Italiana: '+ str(df_aux.iloc[0,1]), value=df_aux.iloc[0,2])
    with col2:
        #Brazilian
        df_aux = melhor_restaurante('Brazilian')
        st.metric(label='Brasileira: '+ str(df_aux.iloc[0,1]), value=df_aux.iloc[0,2])
    with col3:
        #Japanese
        df_aux = melhor_restaurante('Japanese')
        st.metric(label='Japonesa: '+ str(df_aux.iloc[0,1]), value=df_aux.iloc[0,2])
    with col4:
        #BBQ
        df_aux = melhor_restaurante('BBQ')
        st.metric(label='BBQ: '+ str(df_aux.iloc[0,1]), value=df_aux.iloc[0,2])
    with col5:
        #Arabian
        df_aux = melhor_restaurante('Arabian')
        st.metric(label='Árabe: '+ str(df_aux.iloc[0,1]), value=df_aux.iloc[0,2])
        

with st.container():
    #st.write('Top', num_restaurantes, 'Restaurantes')
    st.markdown(f"#### Top {num_restaurantes} Restaurantes")
    maior_nota = high_cuisines (df1)                     
    st.write(maior_nota)
    
with st.container():
    st.markdown('')
    col1, col2 = st.columns(2)
    
    with col1:   
        st.markdown('')
        st.markdown(f'###### Os {num_restaurantes} Melhores Tipos de Culinárias')
        fig = best_cuisines (df1)  
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('')
        st.markdown(f'###### Os {num_restaurantes} Piores Tipos de Culinárias')
        fig = worst_cuisines (df1)
        st.plotly_chart(fig, use_container_width=True)
    

    
   
                
    

    
    
    
    
    
    
   
