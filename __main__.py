import pandas as pd
import streamlit as st
from datetime import datetime
from model_scrapper import Scrapper
from streamlit_tags import st_tags_sidebar

# Configuração inicial do Streamlit
st.set_page_config(
    page_title='OSINT - News Scrapper',
    layout='centered'
)

# Função para recarregar a página
def reload_page():
    st.rerun()  # Recarrega a página

# Barra lateral com opções
st.sidebar.title("Controles")

# Botão de atualização
if st.sidebar.button("Atualizar dados"):
    reload_page()

st.sidebar.divider()

# Selecionar os portais dos quais se deseja raspar as notícias
st.sidebar.header('Filtro por portais de notícias')
portais_list = ['GLOBO', 'R7', 'VEJA', 'TERRA DO MANDU']
portais = st.sidebar.multiselect(
    "Selecione os portais de notícias",
    portais_list,
    portais_list,
    label_visibility='hidden'
)

st.sidebar.divider()

# Criar uma instância do Scrapper e obter as notícias
df_news = pd.DataFrame({
    'Fonte': [],
    'Manchete': [],
    'Link': []
    })

for portal in portais:
    scrapper_portal = Scrapper(portal.lower())
    scrapper_portal.update_news()

    df_portal = pd.DataFrame(
        list(scrapper_portal.news.items()), 
        columns=['Manchete', 'Link'],
    )
    df_portal['Fonte'] = portal

    df_news = pd.concat([df_news, df_portal], ignore_index=True)

# Filtro de palavras-chave
st.sidebar.header('Filtro por palavras')
keywords = st_tags_sidebar(label='Separar por espaços',
                          text='ENTER para adicionar.',
                          value=[],
                          suggestions=[],
                          maxtags=50,
                          key="afrfae")

# Aplicar filtro ao DataFrame
if keywords:
    keywords_list = [keyword.lower() for keyword in keywords]  # Converte palavras-chave para minúsculas
    df_news = df_news[df_news['Manchete'].str.lower().str.contains('|'.join(keywords_list))]

# Contar a quantidade de notícias encontradas
num_news = len(df_news)

# Criar links clicáveis
df_news['Link'] = df_news['Link'].apply(lambda x: f'<a href="{x}" target="_blank">Ir para a notícia</a>')
df_news = df_news[['Fonte', 'Manchete', 'Link']]

# Exibir título e informações do cabeçalho
st.title('OSINT - News Scrapper', anchor=False)
st.divider()

# Exibir a data e hora da última atualização e a quantidade de notícias encontradas
last_update = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
col1, col2 = st.columns([1, 3])  # Cria duas colunas

with col1:
    st.write(f"**Última atualização:** {last_update}")

with col2:
    st.write(f"**Quantidade de notícias encontradas:** {num_news}")

# Gerar o HTML da tabela
html_content = df_news.to_html(escape=False, index=True)

# Exibir a tabela HTML diretamente no Streamlit
st.markdown(html_content, unsafe_allow_html=True)
