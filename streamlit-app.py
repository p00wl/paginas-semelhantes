import pandas as pd
import streamlit as st

# Importação de dados do GSC. Colunas necessárias: Landing Page e Query
@st.cache
def load_data():
    gsc_data = pd.read_csv('dados/lp_mp.csv') # Caminho dos dados exportados do GSC por você
    gsc_data = gsc_data[~gsc_data['Landing Page'].str.contains("#")]
    return gsc_data

# Agrupamento de keywords por URL
@st.cache
def group_keywords(gsc_data):
    kwd_by_urls = gsc_data.groupby('Landing Page')['Query'].apply(list)
    kwd_by_urls_df = pd.DataFrame(kwd_by_urls)
    return kwd_by_urls_df

# Função que irá checar as páginas ranqueando para os mesmos termos
def keywords_similares(row, kwd_by_urls_df, percent):
    url_atual = row.name
    kwds_atuais = set(row['Query'])
    
    if len(kwds_atuais) < 10:
        return []
    
    urls_similares = []
    for url, queries in kwd_by_urls_df.itertuples():
        if url != url_atual:
            kwds_compartilhadas = set(queries).intersection(kwds_atuais)
            if len(kwds_compartilhadas) >= percent * len(kwds_atuais):
                urls_similares.append(url)
    return urls_similares

def main():
    st.title("Análise de Keywords")
    
    gsc_data = load_data()
    kwd_by_urls_df = group_keywords(gsc_data)
    
    percent = st.slider('Selecione a porcentagem', min_value=0.0, max_value=1.0, value=0.8, step=0.01)
    
    # Aplicação da função acima e exportação apenas das URLs que ranqueiam para os mesmos termos
    kwd_by_urls_df['URLs Semelhantes'] = kwd_by_urls_df.apply(keywords_similares, args=(kwd_by_urls_df, percent), axis=1)
    kwd_by_urls_df = kwd_by_urls_df[kwd_by_urls_df['URLs Semelhantes'].apply(lambda x: len(x) != 0)]
    
    st.write(kwd_by_urls_df)

if __name__ == "__main__":
    main()
