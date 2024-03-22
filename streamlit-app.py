import pandas as pd
import streamlit as st

# Importação de dados do GSC. Colunas necessárias: Landing Page e Query
def load_data(file):
    gsc_data = pd.read_csv(file)
    gsc_data = gsc_data[~gsc_data['Landing Page'].str.contains("#")]
    return gsc_data

# Agrupamento de keywords por URL
def group_keywords(gsc_data):
    kwd_by_urls = gsc_data.groupby('Landing Page')['Query'].apply(list)
    kwd_by_urls_df = pd.DataFrame(kwd_by_urls)
    return kwd_by_urls_df

# Função que irá checar as páginas ranqueando para os mesmos termos
def keywords_similares(row, kwd_by_urls_df, percent):
    url_atual = row.name
    kwds_atuais = set(row['Query'])
    
    if len(kwds_atuais) < 10:
        return pd.Series([[], []])
    
    urls_similares = []
    kwds_compartilhadas = []
    for url, queries in kwd_by_urls_df.itertuples():
        if url != url_atual:
            kwds_url = set(queries)
            kwds_comum = kwds_url.intersection(kwds_atuais)
            if len(kwds_comum) >= percent * len(kwds_atuais):
                urls_similares.append(url)
                kwds_compartilhadas.append(list(kwds_comum))
    return pd.Series([urls_similares, kwds_compartilhadas])

def main():
    st.title("Encontre páginas semelhantes com dados do GSC")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    percent = st.slider('Porcentagem de palavras compartilhadas', min_value=0.0, max_value=1.0, value=0.8, step=0.01)
    
    if st.button('Iniciar'):
        if uploaded_file is not None:
            # Inicia a barra de progresso
            progress_bar = st.progress(0)
            
            gsc_data = load_data(uploaded_file)
            progress_bar.progress(33)  # Atualiza a barra de progresso após a conclusão da função load_data
            
            kwd_by_urls_df = group_keywords(gsc_data)
            progress_bar.progress(66)  # Atualiza a barra de progresso após a conclusão da função group_keywords
            
            # Aplicação da função acima e exportação apenas das URLs que ranqueiam para os mesmos termos
            kwd_by_urls_df[['URLs Semelhantes', 'Keywords Compartilhadas']] = kwd_by_urls_df.apply(keywords_similares, args=(kwd_by_urls_df, percent), axis=1)
            kwd_by_urls_df = kwd_by_urls_df[kwd_by_urls_df['URLs Semelhantes'].apply(lambda x: len(x) != 0)]
            
            progress_bar.progress(100)  # Atualiza a barra de progresso após a conclusão da função keywords_similares
            
            st.write(kwd_by_urls_df)
        else:
            st.error('Por favor, faça o upload de um arquivo CSV.')

if __name__ == "__main__":
    main()
