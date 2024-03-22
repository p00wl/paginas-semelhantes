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
        return []
    
    urls_similares = []
    for url, queries in kwd_by_urls_df.itertuples():
        if url != url_atual:
            kwds_compartilhadas = set(queries).intersection(kwds_atuais)
            if len(kwds_compartilhadas) >= percent * len(kwds_atuais):
                urls_similares.append(url)
    return urls_similares

def main():
    st.title("Encontre páginas semelhantes com dados do GSC")

    with st.expander("Antes de usar"):
        st.write("""
        1. Crie um dashboard no Looker Studio com o gráfico de 'Tabela'.
        2. Na tabela, insira como dimensão os campos Landing Page e Query.
        3. Filtre o período que deseja coletar os dados (sugestão: últimos 30 dias)
        4. Nos três pontos da tabela, clique em exportar para CSV.
        Verifique se o arquivo .csv exportado possui as colunas Landing Page e Query (nomeadas exatamente desta forma)
        """)

    with st.expander("Por que exportar os dados pelo Looker Studio?"):
        st.write("""
        O Search Console possui uma limitação de 1000 linhas. No Looker Studio, você pode expandir essa limitação, conseguindo exportar quase tudo que precisa.
        Porém, ainda assim existe limitação. Portanto, a depender do tamanho do seu site, alguns dados podem ser truncados. O ideal é exportar via BigQuery ou outra solução de big data que permita extrair os dados do GSC.
        """)

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    percent = st.slider('Porcentagem de palavras compartilhadas', min_value=0.0, max_value=1.0, value=0.8, step=0.01)
    
    if st.button('Iniciar'):
        if uploaded_file is not None:
            gsc_data = load_data(uploaded_file)
            kwd_by_urls_df = group_keywords(gsc_data)
            
            # Aplicação da função acima e exportação apenas das URLs que ranqueiam para os mesmos termos
            kwd_by_urls_df['URLs Semelhantes'] = kwd_by_urls_df.apply(keywords_similares, args=(kwd_by_urls_df, percent), axis=1)
            kwd_by_urls_df = kwd_by_urls_df[kwd_by_urls_df['URLs Semelhantes'].apply(lambda x: len(x) != 0)]
            
            st.write(kwd_by_urls_df)
        else:
            st.error('Por favor, faça o upload de um arquivo CSV.')

if __name__ == "__main__":
    main()
