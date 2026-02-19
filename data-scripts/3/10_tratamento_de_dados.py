# %%
import pandas as pd

# %%
# carregando DataFrame corrigindo o tipo das colunas dt_venda e dt_entrega em datetime, lendo primeiro o dia na conversão
df_vendas = pd.read_csv('../data-scripts/3/base_vendas.csv', parse_dates=['dt_venda', 'dt_entrega'], dayfirst=True)
df_vendas.head()

# %%
colunas = df_vendas.columns
print(colunas)

# %%
# padronizando o nome das colunas, letra minúscula e espaço substituído por underline
colunas = list(i.strip().replace(' ', '_').lower() for i in colunas)

# %%
df_vendas.columns = colunas

# %%
# verificando se a mudança foi bem-sucedida
df_vendas.head()

# %%
# mudando o separador decimal do preço de vírgula para ponto, comum no Brasil
df_vendas['valor_unitario'] = df_vendas['valor_unitario'].str.replace(',', '.')

# %%
# convertendo as linhas de string para float
df_vendas['valor_unitario'] = df_vendas['valor_unitario'].astype(float)

# %%
df_vendas.info()

# %%
df_vendas['preco_custo'] = df_vendas['preco_custo'].str.replace(',', '.')

# %%
df_vendas['preco_custo'] = df_vendas['preco_custo'].astype(float)

# %%
df_vendas.info()

# %%
# forma prática de converter mais de uma coluna
df_vendas = df_vendas.astype({
    'matricula_funcionario':'str',
    'codigo_produto':'str'
})

# %%
df_vendas.info()

# %%
# caso não converta logo ao carregar o arquivo
df_vendas['dt_entrega'] = pd.to_datetime(df_vendas['dt_entrega'], format='%d/%m/%Y %H:%M')

# %%
df_vendas.info()

# %%
df_vendas.head()

# %%
# quantidade total de produtos vendidos
df_vendas['quantidade'].sum()

# %% [markdown]
# #Missing values/Valores faltantes

# %%
# caso queira completar valores nulos com 0
#df_vendas['comissao'] = df_vendas['comissao'].fillna(0)

# %%
# caso queira completar valores nulos com o último valor válido antes do valor nulo em questão
# df_vendas['comissao'] = df_vendas['comissao'].ffill()

# %%
 # caso queira completar valores nulos com o primeiro valor válido depois do valor nulo em questão
 df_vendas['comissao'] = df_vendas['comissao'].bfill()
 df_vendas['comissao']


# %%
# caso queira linhas com valores nulos removidas, independente da linha ter valores em outras colunas
# df_vendas.dropna(inplace=True)
# df_vendas.info()

# %%
df_vendas['comissao'] = df_vendas['comissao'].str.replace(',', '.')
df_vendas['comissao'] = df_vendas['comissao'].astype(float)


# %%
# moda das comissões
moda = df_vendas['comissao'].mode()[0]
print(moda)

# %%
# caso queira completar nulos com o valor da moda obtida
# df_vendas['comissao'] = df_vendas['comissao'].fillna(moda)

# %%
df_vendas['comissao']

# %%
# Exemplo de quartis de comissão (apenas exemplar de método, pois há muita inconsistência nas comissões originalmente)

# Criando nova coluna para os grupos onde:
# q=4 4 grupos (quartis)
# labels=False retorna apenas os números dos grupos (0, 1, 2, 3) em vez de intervalos
# duplicates='drop' resolve valores duplicados nos limites dos quartis, por isso foram criados apenas 3 grupos

df_vendas['comissao_qcut'] = pd.qcut(df_vendas['comissao'], q=4, labels=False, duplicates='drop')

# Moda por quartil

# Agrupa o dataframe pelos quartis de comissão criados anteriormente
# Para cada grupo, seleciona a coluna 'codigo_loja'
# .agg() aplica uma função personalizada de agregação calcula a moda (valor mais frequente) e pega o primeiro elemento, tratando os sem moda definida

mode_by_quartile = df_vendas.groupby('comissao_qcut')['codigo_loja'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'No mode')


print("Moda de 'codigo_loja' por quartis de 'comissao':")
print(mode_by_quartile)

# %%
print("\nDistribuição de registros por quartil:")
print(df_vendas['comissao_qcut'].value_counts().sort_index())

# %%
display(df_vendas)

# %%
df_vendas.info()


