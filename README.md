# Previsão de Evasão Universitária com Machine Learning

Este projeto tem como objetivo identificar fatores associados à evasão universitária por meio da análise de dados educacionais, socioeconômicos e demográficos de estudantes, utilizando técnicas de aprendizado de máquina. O estudo visa oferecer subsídios para que universidades implementem intervenções eficazes e personalizadas com base em dados.

## Objetivos Específicos

- **Analisar os dados** do dataset *Predict Students Dropout and Academic Success* para identificar padrões e variáveis que contribuem para a evasão.
- **Agrupar estudantes** com características semelhantes por meio de algoritmos de clusterização, destacando perfis e fatores predominantes em cada grupo.
- **Desenvolver um modelo de classificação** para prever a probabilidade de evasão com base em variáveis-chave, como fatores socioeconômicos, desempenho acadêmico e dados demográficos.
- **Avaliar o desempenho** dos modelos criados, destacando os fatores mais relevantes e apresentando recomendações práticas para intervenções direcionadas.

---

## 1. Dataset

O projeto utiliza o dataset **Predict Students Dropout and Academic Success**, que contém informações sobre desempenho acadêmico, perfil socioeconômico e dados demográficos de estudantes. Este conjunto de dados está disponível publicamente no [Kaggle](https://www.kaggle.com/datasets/syedfaizanalii/predict-students-dropout-and-academic-success).

---

## 2. Clusterização dos Estudantes

Para identificar grupos de estudantes com características semelhantes, foi utilizado o algoritmo **K-Means**. Inicialmente, foram aplicados os métodos do **Cotovelo** e da **Silhueta** para determinar o número ideal de clusters.

---

## 3. Modelos de Classificação

Para prever a probabilidade de evasão, foram implementados os seguintes algoritmos de aprendizado supervisionado:

- **Random Forest**
- **Support Vector Machine (SVM)**
- **K-Nearest Neighbors (KNN)**

### 3.1 Preparação dos Dados

A variável alvo (`target`) originalmente possuía três classes: `desistentes`, `graduados` e `matriculados`. Para simplificar a análise, as classes `matriculados` e `graduados` foram agrupadas em uma única classe, focando na distinção entre `desistentes` e `não desistentes`.

### 3.2 Avaliação dos Modelos

Os modelos foram avaliados utilizando métricas como **acurácia**, **precisão**, **recall** e **f1-score**.

---

## 4. Interpretação com SHAP

Para compreender a influência de cada variável nas previsões dos modelos, foram utilizados os valores **SHAP

---

## 5. Tecnologias Utilizadas

- **Python 3.11+**
- **Pandas** — Manipulação de dados
- **NumPy** — Operações numéricas
- **Scikit-learn** — Modelagem de machine learning
- **Imbalanced-learn** — Técnicas de balanceamento (ex: SMOTE)
- **SHAP** — Interpretação dos modelos
- **Plotly** — Visualizações interativas
- **Matplotlib / Seaborn** — Gráficos estatísticos
- **Streamlit** — Interface da aplicação
- **Jupyter Notebook** — Prototipagem e análise exploratória

---

## 6. Execução Local

No terminal, navegue até o diretório raiz do projeto e execute o seguinte comando para criar um ambiente virtual:

```
python -m venv venv
```
**2. Ativar o Ambiente Virtual**
```
venv\Scripts\activate
```

**3. Instalar os Pacotes Necessários**
```
pip install -r requirements.txt
```

**3. Instalar os Pacotes Necessários**
```
streamlit run app.py
```
