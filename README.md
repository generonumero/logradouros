# Classificação de Logradouros Brasileiros por Gênero

Nesse repositório estão os scripts que classificam logradouros brasileiros com
base no banco de dados [IBGE
Nomes](http://censo2010.ibge.gov.br/nomes/#/search) (que por sua vez utiliza
dados do Censo Demográfico de 2010).


## Dados Fechados

Os dados dos logradouros brasileiros foram comprados (sim, [esses dados não são
públicos](https://www.codigourbano.org/por-que-o-cep-deve-ser-tratado-como-informacao-publica/))
e, por conta disso, não estão disponíveis nesse repositório.

## Rodando

Instale as dependências Python rodando:

    pip install -r requirements.txt

Então basta colocar os nomes no arquivo CSV `data/names.csv` e executar o
script:

    ./names_stats.py

O resultado ficará em `output/names-stats.csv`.
