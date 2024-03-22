# Encontre Páginas Semelhantes com Dados do GSC

Este projeto é uma ferramenta de análise de SEO que utiliza dados do Google Search Console (GSC) para identificar páginas que ranqueiam para palavras-chave semelhantes. A ferramenta é construída em Python e utiliza a biblioteca Streamlit para a interface do usuário.

## Como Usar

1. Exporte os dados do GSC através do Looker Studio (ou outra ferramenta de sua preferência que permita a exportação de dados do GSC).
2. Carregue o arquivo CSV exportado na interface do Streamlit.
3. Ajuste a porcentagem de palavras-chave compartilhadas usando o controle deslizante.
4. Clique em 'Iniciar' para executar a análise.

## Funções Principais

- `load_data(file)`: Importa os dados do GSC de um arquivo CSV. As colunas necessárias são 'Landing Page' e 'Query'.
- `group_keywords(gsc_data)`: Agrupa as palavras-chave por URL.
- `keywords_similares(row, kwd_by_urls_df, percent)`: Verifica as páginas que ranqueiam para os mesmos termos.

## Requisitos

- Python 3.7+
- Pandas
- Streamlit

## Contribuições

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar uma solicitação pull.

## Licença

Este projeto está licenciado sob a licença MIT.
