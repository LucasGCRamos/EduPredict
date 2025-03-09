import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise Exploratória", page_icon="🎓", layout="wide")
st.title("📊 Análise Exploratória dos Dados")
st.markdown(
    "Esta análise apresenta uma visão geral dos dados acadêmicos, explorando fatores como situação financeira, familiar e demográfica."
)

# Carregar os dados
dados = pd.read_parquet('pisi3_database/dataset_traduzido.parquet')

# Mostrar o dataset
st.subheader("📌 Visão Geral do Dataset")
st.write(f"- **Número de Linhas:** {dados.shape[0]}")
st.write(f"- **Número de Colunas:** {dados.shape[1]}")

# Definir grupos de variáveis
grupos_variaveis = {
    "Financeiro": ["Devedor", "Pagamento em dia", "Bolsista"],
    "Família": ["Qualificação da mãe", "Qualificação do pai"],
    "Demografia": ["Gênero", "Estado civil", "Idade na inscrição"],
    "Outros": ["Deslocado", "Necessidade de educação especial"]
}

# Filtros no corpo da página
st.header("🔍 Filtros para gráfico interativo")

# Função para criar filtros
def criar_filtro(coluna, dados):
    opcoes = ["Todos"] + list(dados[coluna].unique())
    return st.selectbox(coluna, opcoes)

# Criar expanders para cada grupo de variáveis
with st.expander("**Dados demograficos**", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        genero = criar_filtro("Gênero", dados)
    with col2:
        estado_civil = criar_filtro("Estado civil", dados)
    with col3:
        idade_min, idade_max = st.slider(
            "Idade na inscrição",
            min_value=int(dados["Idade na inscrição"].min()),
            max_value=int(dados["Idade na inscrição"].max()),
            value=(int(dados["Idade na inscrição"].min()), int(dados["Idade na inscrição"].max()))
        )

with st.expander("**Dados financeiros**", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        devedor = criar_filtro("Devedor", dados)
    with col2:
        pagamento_em_dia = criar_filtro("Pagamento em dia", dados)
    with col3:
        bolsista = criar_filtro("Bolsista", dados)

with st.expander("**Dados familiares**", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        qualificacao_mae = criar_filtro("Qualificação da mãe", dados)
    with col2:
        qualificacao_pai = criar_filtro("Qualificação do pai", dados)

with st.expander("**Outros**", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        deslocado = criar_filtro("Deslocado", dados)
    with col2:
        necessidade_educacao_especial = criar_filtro("Necessidade de educação especial", dados)

# Aplicar filtros ao dataset
dados_filtrados = dados.copy()

# Filtros de Demografia
if genero != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Gênero"] == genero]
if estado_civil != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Estado civil"] == estado_civil]
dados_filtrados = dados_filtrados[
    (dados_filtrados["Idade na inscrição"] >= idade_min) &
    (dados_filtrados["Idade na inscrição"] <= idade_max)
]

# Filtros de Financeiro
if devedor != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Devedor"] == devedor]
if pagamento_em_dia != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Pagamento em dia"] == pagamento_em_dia]
if bolsista != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Bolsista"] == bolsista]

# Filtros de Família
if qualificacao_mae != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Qualificação da mãe"] == qualificacao_mae]
if qualificacao_pai != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Qualificação do pai"] == qualificacao_pai]

# Filtros de Outros
if deslocado != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Deslocado"] == deslocado]
if necessidade_educacao_especial != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Necessidade de educação especial"] == necessidade_educacao_especial]

# Agrupar por Target e contar os registros
contagem_target = dados_filtrados["Target"].value_counts().reset_index()
contagem_target.columns = ["Target", "Contagem"]

# Gráfico principal
st.subheader("📈 Gráfico interativo com distribuição de formação acadêmica")

# Exemplo de gráfico: Barras por Target
fig = px.bar(
    contagem_target,
    x="Target",
    y="Contagem",
    title=f"Distribuição de formação acadêmica com filtros aplicados",
    labels={"Contagem": "Quantidade de estudantes", "Target": "Status acadêmico"},
    text="Contagem"  # Mostra o valor da contagem em cima da barra
)

# Exibir o gráfico
st.plotly_chart(fig)


st.subheader("Gráficos de acordo com caracteristicas selecionadas")

# Seleção do grupo de variáveis
grupo_selecionado = st.selectbox("Escolha o grupo de variáveis para análise:", list(grupos_variaveis.keys()))
variaveis_selecionadas = grupos_variaveis[grupo_selecionado]

# Função para aplicar filtro para "Outro" em variáveis gerais
def aplicar_filtro(dados_plot):
    contagem = dados_plot.value_counts()
    dados_plot = dados_plot.replace(contagem[contagem < 71].index, 'Outro')
    return dados_plot

# Função para aplicar filtro específico na variável "Necessidade de educação especial"
def aplicar_filtro_necessidade_educacao(dados_plot):
    # Mantém apenas "Sim" e "Não", e substitui os outros valores por "Outro"
    valores_permitidos = ['Sim', 'Não']
    dados_plot = dados_plot.apply(lambda x: x if x in valores_permitidos else 'Outro')
    return dados_plot

# Gráficos de Barra
st.subheader("📊 Distribuição das Variáveis")
# Exibe gráficos de barra para todas as variáveis do grupo selecionado
for variavel in variaveis_selecionadas:
    dados_plot = dados[variavel].copy()
    
    # Aplica filtro somente se a variável não for "Necessidade de educação especial"
    if variavel == "Necessidade de educação especial":
        dados_plot = aplicar_filtro_necessidade_educacao(dados_plot)
    else:
        dados_plot = aplicar_filtro(dados_plot)  # Aplica o filtro para outras variáveis
    
    dados_plot = dados_plot.value_counts().reset_index()
    dados_plot.columns = [variavel, 'Contagem']

         # Ordena os dados pela contagem (do maior para o menor)
    dados_plot = dados_plot.sort_values(by='Contagem', ascending=True)

    # Se for "Qualificação da mãe" ou "Qualificação do pai", barras horizontais
    if variavel in ["Qualificação da mãe", "Qualificação do pai"]:
        fig = px.bar(dados_plot, 
                     y=variavel, 
                     x="Contagem", 
                     title=f"Distribuição de {variavel}", 
                     orientation='h')  # Barras horizontais
        fig.update_layout(yaxis=dict(tickangle=0, tickmode="linear"))
    else:
        fig = px.bar(dados_plot, 
                     x=variavel, 
                     y="Contagem", 
                     title=f"Distribuição de {variavel}", 
                     orientation='v')  # Barras verticais
        fig.update_layout(xaxis=dict(tickangle=0, tickmode="linear"))
    
    st.plotly_chart(fig)

    # Adicionando comentários explicativos
    if variavel == "Gênero":
        st.write("**Insight**: A população de mulheres é significativamente maior que a de homens no conjunto de dados.")
    elif variavel == "Estado civil":
        st.write("**Insight**: A grande maioria da população é composta por solteiros, com poucos casados ou divorciados.")
    elif variavel == "Devedor":
        st.write("**Insight**: A maior parte da população está em dia com suas obrigações financeiras, com uma pequena porcentagem de devedores.")
    elif variavel == "Pagamento em dia":
        st.write("**Insight**: A maioria da população realiza os pagamentos dentro do prazo estipulado, com poucos casos de pagamentos em atraso.")
    elif variavel == "Bolsista":
        st.write("**Insight**: A maioria da população não é bolsista, com uma pequena porcentagem recebendo algum tipo de bolsa.")
    elif variavel == "Qualificação da mãe":
        st.write("**Insight**: A maior parte das mães possui ensino médio completo ou superior, com poucos casos de ensino fundamental ou menos.")
    elif variavel == "Qualificação do pai":
        st.write("**Insight**: Similar às mães, a maioria dos pais tem nível médio ou superior, com uma pequena porcentagem com nível fundamental.")
    elif variavel == "Deslocado":
        st.write("**Insight**: A população de deslocados apresenta uma quantidade considerável de indivíduos em situação de deslocamento")
    elif variavel == "Necessidade de educação especial":
        st.write("**Insight**: A grande maioria das pessoas não tem necessidade de educação especial, enquanto apenas um número muito pequeno possui essa necessidade. Isso indica que a necessidade de educação especial é uma condição relativamente rara dentro deste grupo.")

# Gráficos de comparação com "Target"
st.subheader("📈 Comparação com a Variável de Interesse")
for variavel in variaveis_selecionadas:
    dados_plot = dados[[variavel, "Target"]].copy()
    
    # Aplica filtro somente se a variável não for "Necessidade de educação especial"
    if variavel == "Necessidade de educação especial":
        dados_plot[variavel] = aplicar_filtro_necessidade_educacao(dados_plot[variavel])
    else:
        dados_plot[variavel] = aplicar_filtro(dados_plot[variavel])  # Aplica o filtro para outras variáveis
    
    # Agrupar por variável e Target para contar as ocorrências
    dados_plot = dados_plot.groupby([variavel, 'Target']).size().reset_index(name='Contagem')

     # Ordena os dados pela contagem (do maior para o menor)
    dados_plot = dados_plot.sort_values(by='Contagem', ascending=True)

    # Se for "Qualificação da mãe" ou "Qualificação do pai", barras horizontais
    if variavel in ["Qualificação da mãe", "Qualificação do pai"]:
        fig = px.bar(dados_plot, 
                     y=variavel, 
                     x="Contagem", 
                     color='Target', 
                     title=f"Distribuição de {variavel} com Target", 
                     orientation='h')  # Barras horizontais
        fig.update_layout(yaxis=dict(tickangle=0, tickmode="linear"))
    else:
        fig = px.bar(dados_plot, 
                     x=variavel, 
                     y="Contagem", 
                     color='Target', 
                     title=f"Distribuição de {variavel} com Target", 
                     orientation='v')  # Barras verticais
        fig.update_layout(xaxis=dict(tickangle=0, tickmode="linear"))
    
    st.plotly_chart(fig)

    # Adicionando comentários explicativos sobre o gráfico com "Target"
    if variavel == "Gênero":
        st.write("**Insight**: As mulheres têm uma maior proporção de graduadas, enquanto os homens apresentam uma maior quantidade de desistentes.")
    elif variavel == "Estado civil":
        st.write("**Insight**: Solteiros têm maior diversidade de status acadêmico, enquanto casados e divorciados têm uma concentração maior de desistentes.")
    elif variavel == "Devedor":
        st.write("**Insight**: Devedores apresentam uma maior proporção de desistentes em comparação aos que estão em dia com seus pagamentos.")
    elif variavel == "Pagamento em dia":
        st.write("**Insight**: Aqueles que pagam em dia têm maior concentração de graduados, enquanto os devedores têm uma maior proporção de desistentes.")
    elif variavel == "Bolsista":
        st.write("**Insight**: Bolsistas têm uma proporção mais alta de graduados, enquanto não bolsistas têm uma maior quantidade de desistentes.")
    elif variavel == "Qualificação da mãe":
        st.write("**Insight**: A qualificação da mãe tem impacto na distribuição do status acadêmico dos filhos. Mães com ensino secundário e ensino básico (1º e 3º ciclos) têm uma maior quantidade de filhos graduandos e matriculados, mas também uma proporção significativa de filhos desistentes. Já as mães com ensino superior, apesar de representarem uma quantidade menor, apresentam um número expressivo de graduados.")
    elif variavel == "Qualificação do pai":
        st.write("**Insight**: A qualificação do pai também influencia significativamente o status acadêmico dos filhos. Pais com ensino básico e secundário têm um número considerável de filhos desistentes, mas a maior parte dos filhos dessas categorias está em processo de graduação ou matrícula. Pais com ensino superior têm uma menor quantidade de filhos desistentes, com um número considerável de graduandos.")
    elif variavel == "Deslocado":
        st.write("**Insight**: A maior parte dos deslocados com target está em processo de graduação, mas a taxa de desistência é significativa")
    elif variavel == "Necessidade de educação especial":
        st.write("**Insight**: A quantidade de pessoas com necessidade de educação especial é baixa em comparação com a população geral. No entanto, entre os que têm essa necessidade, a maioria está graduando e matriculado.")
