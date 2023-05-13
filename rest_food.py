#Importação de bibliotecas

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image



#Importação do dataframe

df = pd.read_csv ('raw_data.csv')



#Tratamento e limpeza da base de dados

##Removendo restaurantes duplicados da base de dados

df = df.drop_duplicates()


##Definindo apenas 1 tipo de culinária por restaurate

df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])


##Criando coluna de nome do país a partir do código do país

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

df['Country Name'] = df['Country Code'].apply(lambda x: COUNTRIES.get(x))



#Criação de gráficos e tabelas

## Restaurantes cadastrados na plataforma

def qtd_rest_cadast():
    
    qtd_rest_cadast = ( df.loc[:, "Restaurant ID"]
                        .nunique() )
            
    formatted_output = format(qtd_rest_cadast, ",")
    
    return formatted_output
    

## Avaliações recebidas na plataforma

def qtd_aval_receb():

    qtd_aval_receb = ( df.loc[:, "Votes"]
                        .sum() )
            
    formatted_output = format(qtd_aval_receb, ",")
    
    return formatted_output


## Quantidade de restaurantes cadastrados por país

def tab_rest_cad_pais():
    
    tab_rest_cad_pais = ( df.loc[:, ["Country Name", "Restaurant ID"]]
                          .groupby("Country Name")
                          .nunique("Restaurant ID")
                          .sort_values("Restaurant ID", ascending=False)
                          .reset_index().loc[0:20, :] )

    tab_rest_cad_pais.rename(columns={"Country Name": "País", "Restaurant ID": "Restaurantes cadastrados"}, inplace=True)
    
    return tab_rest_cad_pais


## Quantidade de avaliações por país

def tab_rest_aval_pais():

    tab_rest_aval_pais = ( df.loc[:, ["Country Name", "Votes"]]
                            .groupby("Country Name")
                            .sum("Votes")
                            .sort_values("Votes", ascending=False)
                            .reset_index() )

    tab_rest_aval_pais.rename(columns={"Country Name": "País", "Votes": "Avaliações recebidas"}, inplace=True)
    
    return tab_rest_aval_pais


## Avaliação média dos restaurantes por país

def tab_aval_med_pais():

    tab_aval_med_pais = ( df.loc[:, ["Country Name", "Aggregate rating"]]
                                    .groupby("Country Name")
                                    .mean("Aggregate rating")
                                    .round(1).sort_values("Aggregate rating", ascending=False)
                                    .reset_index() )

    tab_aval_med_pais.rename(columns={"Country Name": "País", "Aggregate rating": "Nota média"}, inplace=True)

    return tab_aval_med_pais


## Quantidade de restaurantes cadastrados por cidade

def tab_rest_cad_cidade():

    tab_rest_cad_cidade = ( df.loc[:, ["City", "Restaurant ID"]]
                            .groupby("City")
                            .nunique("Restaurant ID")
                            .sort_values("Restaurant ID", ascending=False)
                            .reset_index()
                            .loc[0:125, :] )

    tab_rest_cad_cidade.rename(columns={"City": "Cidade", "Restaurant ID": "Restaurantes cadastrados"}, inplace=True)
    
    return tab_rest_cad_cidade


## Quantidade de avaliações recebidas pelos restaurantes de cada cidade

def tab_rest_aval_cidade():

    tab_rest_aval_cidade = ( df.loc[:, ["City", "Votes"]]
                             .groupby("City")
                             .sum("Votes")
                             .sort_values("Votes", ascending=False)
                             .reset_index() )

    tab_rest_aval_cidade.rename(columns={"City": "Cidade", "Votes": "Avaliações recebidas"}, inplace=True)

    return tab_rest_aval_cidade


## Avaliação média dos restaurantes por cidade

def tab_aval_med_cidade():

    tab_aval_med_cidade = ( df.loc[:, ["City", "Aggregate rating"]]
                              .groupby("City")
                              .mean("Aggregate rating")
                              .round(1)
                              .sort_values("Aggregate rating", ascending=False)
                              .reset_index() )

    tab_aval_med_cidade.rename(columns={"City": "Cidade", "Aggregate rating": "Nota média"}, inplace=True)

    return tab_aval_med_cidade


## 20 restaurantes mais bem avaliados pelos clientes

def tab_20_rest_maiores_notas():

    tab_20_rest_maiores_notas = ( df.loc[:, ["Restaurant Name", "Restaurant ID", "Aggregate rating"]]
                                  .sort_values(["Aggregate rating", "Restaurant ID"], ascending=[False, True])
                                  .reset_index()
                                  .iloc[0:20, :] )

    tab_20_rest_maiores_notas.rename(columns={"Restaurant Name": "Restaurante", "Restaurant ID": "ID do Restaurante", "Aggregate rating": "Avaliação"}, inplace=True)

    tab_20_rest_maiores_notas = tab_20_rest_maiores_notas.loc[:, ["Restaurante", "Avaliação"]]
    
    return tab_20_rest_maiores_notas


## 20 restaurantes com mais avaliações recebidas dos clientes

def tab_20_rest_mais_aval_receb():

    tab_20_rest_mais_aval_receb = ( df.loc[:, ["Restaurant Name", "Restaurant ID", "Votes"]]
                                    .sort_values(["Votes", "Restaurant ID"], ascending=[False, True])
                                    .reset_index()
                                    .iloc[0:20, :] )

    tab_20_rest_mais_aval_receb.rename(columns={"Restaurant Name": "Restaurante", "Restaurant ID": "ID do Restaurante", "Votes": "Avaliações recebidas"}, inplace=True)

    tab_20_rest_mais_aval_receb = tab_20_rest_mais_aval_receb.loc[:, ["Restaurante", "Avaliações recebidas"]]
    
    return tab_20_rest_mais_aval_receb


## 20 tipos culinários com mais restaurantes cadastrados

def tab_20_tipo_cul_mais_rest_cadast():

    tab_20_tipo_cul_mais_rest_cadast = ( df.loc[:, ["Cuisines", "Restaurant ID"]]
                                         .groupby("Cuisines")
                                         .nunique("Restauarant ID")
                                         .sort_values("Restaurant ID", ascending=False)
                                         .reset_index()
                                         .loc[0:20, :] )

    tab_20_tipo_cul_mais_rest_cadast.rename(columns={"Cuisines": "Tipo de Culinária", "Restaurant ID": "Restaurantes Cadastrados"}, inplace=True)
    
    return tab_20_tipo_cul_mais_rest_cadast


## 20 tipos culinários com maior avaliação média

def tab_20_tipo_cul_maior_not_media():

    tab_20_tipo_cul_maior_not_media = ( df.loc[:, ["Cuisines", "Aggregate rating"]]
                                        .groupby("Cuisines")
                                        .mean("Aggregate rating")
                                        .round(2)
                                        .sort_values("Aggregate rating", ascending=False)
                                        .reset_index()
                                        .loc[0:20, :] )

    tab_20_tipo_cul_maior_not_media.rename(columns={"Cuisines": "Tipo de Culinária", "Aggregate rating": "Nota média"}, inplace=True)
    
    return tab_20_tipo_cul_maior_not_media


## 20 tipos culinários com menor avaliação média

def tab_20_tipo_cul_menor_not_media():

    tab_20_tipo_cul_menor_not_media = ( df.loc[:, ["Cuisines", "Aggregate rating"]]
                                        .groupby("Cuisines")
                                        .mean("Aggregate rating")
                                        .round(2)
                                        .sort_values("Aggregate rating", ascending=True)
                                        .reset_index()
                                        .loc[0:20, :] )

    tab_20_tipo_cul_menor_not_media.rename(columns={"Cuisines": "Tipo de Culinária", "Aggregate rating": "Nota média"}, inplace=True)
    
    return tab_20_tipo_cul_menor_not_media



#Criação do dashboard

##Introdução

st.set_page_config(
    page_title="Rest & Food - Dashboard",
    page_icon="📊",
    layout="centered")

image = Image.open('icone-restaurante.png')

st.image(image, width=80)

st.header('Rest & Food')

st.markdown('Dashboard com os principais indicadores do marketplace de restaurantes Rest & Food.')

st.markdown('**Clique em uma das abas abaixo para escolher um tipo de visão gerencial:**')

tab1, tab2, tab3, tab4, tab5 = st.tabs (["Geral 📈", 
                                         "Países 🌍", 
                                         "Cidades 🏙️", 
                                         "Restaurantes 🍳", 
                                         "Culinária 👨🏻‍🍳"])


##Aba geral 📈

with tab1:
    
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            qtd_rest_cadast = qtd_rest_cadast()

            st.metric(label = "Restaurantes cadastrados na plataforma", 
                      value=qtd_rest_cadast, 
                      help="Quantidade total de restaurantes cadastrados na plataforma", 
                      label_visibility="visible")
            
            
        with col2:
            
            qtd_aval_receb = qtd_aval_receb()

            st.metric(label = "Avaliações recebidas na plataforma", 
                      value=qtd_aval_receb, 
                      help="Quantidade total de avaliações recebidas pelos restaurantes na plataforma", 
                      label_visibility="visible")
            
            
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            qtd_pais_rest_cadast = ( df.loc[:, "Country Code"]
                                       .nunique() )

            st.metric(label = "Países onde a plataforma está presente", 
                      value=qtd_pais_rest_cadast, 
                      help="Quantidade total de paises em que plataforma possui algum restaurante cadastrado", 
                      label_visibility="visible")
            
            
        with col2:
            
            qtd_cid_rest_cadast = ( df.loc[:, "City"]
                                      .nunique() )

            st.metric(label = "Cidades onde a plataforma está presente", 
                      value=qtd_cid_rest_cadast, 
                      help="Quantidade total de cidades em que plataforma possui algum restaurante cadastrado", 
                      label_visibility="visible")
        
        
##Aba países 🌍

with tab2:
    
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            pais_mais_rest_cadast = ( df.loc[:, ["Country Name", "Restaurant ID"]]
                                        .groupby("Country Name")
                                        .nunique("Restaurant ID")
                                        .sort_values("Restaurant ID", ascending=False)
                                        .reset_index()
                                        .iloc[0,0] )

            st.metric(label = "País com mais restaurantes cadastrados", 
                      value=pais_mais_rest_cadast, 
                      help="País que possui a maior quantidade de restaurantes cadastrados na plataforma", 
                      label_visibility="visible")
            
            
        with col2:
            
            pais_mais_aval_reg = ( df.loc[:, ["Country Name", "Votes"]]
                                     .groupby("Country Name").sum("Votes")
                                     .sort_values("Votes", ascending=False)
                                     .reset_index()
                                     .iloc[0,0] )

            st.metric(label = "País com maior quantidade de avaliações recebidas", 
                      value=pais_mais_aval_reg, 
                      help="País que possui a maior quantidade de avaliações recebidas pelos seus restaurantes na plataforma", 
                      label_visibility="visible")
            
        
    with st.container():
        
        st.markdown('Quantidade de restaurantes cadastrados por país', 
                    help="Quantidade de restaurantes cadastrados na plataforma por país em ordem decrescente")
        
        tab_rest_cad_pais = tab_rest_cad_pais()

        st.dataframe(tab_rest_cad_pais, 
                     use_container_width=True)
        
        
    with st.container():
        
            st.markdown('Quantidade de avaliações recebidas pelos restaurantes de cada país', 
                        help="Quantidade de avaliações recebidas pelos restaurantes de cada país em ordem decrescente")

            tab_rest_aval_pais = tab_rest_aval_pais()

            st.dataframe(tab_rest_aval_pais, 
                         use_container_width=True)
            
            
    with st.container():
        
            st.markdown('Avaliação média dos restaurantes por país', 
                        help="Nota média recebidas pelos restaurantes de cada país")
            
            tab_aval_med_pais = tab_aval_med_pais()
            
            st.dataframe(tab_aval_med_pais, 
                         use_container_width=True)
            
            
##Aba cidades 🏙️

with tab3:
    
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            cidade_mais_rest_cadast = ( df.loc[:, ["City", "Restaurant ID"]]
                                        .groupby("City").nunique("Restaurant ID")
                                        .sort_values("Restaurant ID", ascending=False)
                                        .reset_index()
                                        .iloc[0,0] )

            st.metric(label = "Cidade com mais restaurantes cadastrados", 
                      value=cidade_mais_rest_cadast, 
                      help="Cidade que possui a maior quantidade de restaurantes cadastrados na plataforma", 
                      label_visibility="visible")
            
            
        with col2:
            
            cidade_mais_aval_reg = ( df.loc[:, ["City", "Votes"]]
                                     .groupby("City").sum("Votes")
                                     .sort_values("Votes", ascending=False)
                                     .reset_index()
                                     .iloc[0,0] )

            st.metric(label = "Cidade com maior quantidade de avaliações recebidas", 
                      value=cidade_mais_aval_reg, 
                      help="Cidade que possui a maior quantidade de avaliações recebidas pelos seus restaurantes na plataforma", 
                      label_visibility="visible")
            
        
    with st.container():
        
        st.markdown('Quantidade de restaurantes cadastrados por cidade', 
                    help="Quantidade de restaurantes cadastrados na plataforma por cidade em ordem decrescente")

        tab_rest_cad_cidade = tab_rest_cad_cidade()
        
        st.dataframe(tab_rest_cad_cidade, 
                     use_container_width=True)
        
        
    with st.container():
        
            st.markdown('Quantidade de avaliações recebidas pelos restaurantes de cada cidade', 
                        help="Quantidade de avaliações recebidas pelos restaurantes de cada cidade em ordem decrescente")

            tab_rest_aval_cidade = tab_rest_aval_cidade()

            st.dataframe(tab_rest_aval_cidade, 
                         use_container_width=True)
            
            
    with st.container():
        
            st.markdown('Avaliação média dos restaurantes por cidade', 
                        help="Nota média recebidas pelos restaurantes de cada cidade")
            
            tab_aval_med_cidade = tab_aval_med_cidade()
            
            st.dataframe(tab_aval_med_cidade, 
                         use_container_width=True)
            
            
##Aba restaurantes 🍳

with tab4:
    
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            rest_maior_avaliacao = ( df.loc[:, ["Restaurant Name", "Restaurant ID", "Aggregate rating"]]
                                       .sort_values(["Aggregate rating", "Restaurant ID"], ascending=[False, True])
                                       .iloc[0,0] )

            st.metric(label = "Restaurante com a maior avaliação", 
                      value=rest_maior_avaliacao, 
                      help="Restaurante com a maior avaliação dada pelos clientes na plataforma", 
                      label_visibility="visible")
            
            
        with col2:
            
            rest_mais_avaliacoes = ( df.loc[:, ["Restaurant Name", "Votes"]]
                                       .sort_values("Votes", ascending=False)
                                       .reset_index()
                                       .iloc[0,1] )

            st.metric(label = "Restaurante com mais avaliações recebidas", 
                      value=rest_mais_avaliacoes, 
                      help="Restaurante que mais recebeu avaliações de clientes na plataforma", 
                      label_visibility="visible")
            
            
    with st.container():
        
            st.markdown("20 restaurantes mais bem avaliados pelos clientes", 
                        help="Os 20 restaurantes mais bem avaliados pelos clientes na plataforma")
                        
            tab_20_rest_maiores_notas = tab_20_rest_maiores_notas()
                    
            st.dataframe(tab_20_rest_maiores_notas, 
                         use_container_width=True)
            
            
    with st.container():
        
            st.markdown("20 restaurantes com mais avaliações recebidas dos clientes", 
                        help="Os 20 restaurantes que receberam mais avaliações de clientes na plataforma")
                        
            tab_20_rest_mais_aval_receb = tab_20_rest_mais_aval_receb()
                
            st.dataframe(tab_20_rest_mais_aval_receb, 
                         use_container_width=True)
            

##Aba Culinária 👨🏻‍🍳

with tab5:
    
    with st.container():
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            
            qtd_tipos_culinarios_distintos = ( df.loc[:, "Cuisines"]
                                                 .nunique() )

            st.metric(label = "Tipos culinários distintos oferecidos na plataforma", 
                      value=qtd_tipos_culinarios_distintos, 
                      help="Quantidade de tipos culinários oferecidos pelos restaurantes cadastrados na plataforma", 
                      label_visibility="visible")
            
            
        with col2:
            
            cul_mais_rest_cadastrados = ( df.loc[:, ["Cuisines", "Restaurant ID"]]
                                            .groupby("Cuisines")
                                            .nunique("Restaurant ID")
                                            .sort_values("Restaurant ID", ascending=False)
                                            .reset_index()
                                            .iloc[0,0] )

            st.metric(label = "Culinária com mais restaurantes cadastrados", 
                      value=cul_mais_rest_cadastrados, 
                      help="Tipo culinário com maior quantidade de restaurantes cadastrados na plataforma", 
                      label_visibility="visible")
            
            
        with col3:
            
            cul_maior_aval_media = ( df.loc[:, ["Cuisines", "Aggregate rating"]]
                                       .groupby("Cuisines")
                                       .mean("Aggregate rating")
                                       .sort_values("Aggregate rating", ascending=False)
                                       .reset_index()
                                       .iloc[0,0] )

            st.metric(label = "Culinária com maior nota média dada pelos clientes", 
                      value=cul_maior_aval_media, 
                      help="Tipo culinário com maior nota dada pelos clientes na plataforma", 
                      label_visibility="visible")
            
 
    with st.container():
        
        st.markdown("20 tipos culinários com mais restaurantes cadastrados", 
                    help="Os 20 tipos culinários com mais restaurantes cadastrados na plataforma")
                        
        tab_20_tipo_cul_mais_rest_cadast = tab_20_tipo_cul_mais_rest_cadast()
                           
        st.dataframe(tab_20_tipo_cul_mais_rest_cadast, 
                     use_container_width=True)
        
        
    with st.container():
        
        st.markdown("20 tipos culinários com maior avaliação média", 
                    help="Os 20 tipos culinários que receberam maior nota média na plataforma")
                        
        tab_20_tipo_cul_maior_not_media = tab_20_tipo_cul_maior_not_media()
                             
        st.dataframe(tab_20_tipo_cul_maior_not_media, 
                     use_container_width=True)
        

    with st.container():
        
        st.markdown("20 tipos culinários com menor avaliação média", 
                    help="Os 20 tipos culinários que receberam menor nota média na plataforma")
                        
        tab_20_tipo_cul_menor_not_media = tab_20_tipo_cul_menor_not_media()
                           
        st.dataframe(tab_20_tipo_cul_menor_not_media, 
                     use_container_width=True)