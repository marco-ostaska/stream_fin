import streamlit as st
import yaml

# Função para carregar os dados do arquivo YAML
def load_data():
    with open("ativos.yml", "r") as file:
        data = yaml.safe_load(file)
    return data

# Função para salvar os dados no arquivo YAML
def save_data(data):
    with open("ativos.yml", "w") as file:
        yaml.safe_dump(data, file)

# Função para adicionar um ativo
def add_ativo(ticker, categoria):
    data = load_data()
    if categoria not in data:
        data[categoria] = {"spread": 0, "tickers": []}

    # Verificar se o ticker já existe na categoria
    tickers = [item["ticker"] for item in data[categoria]["tickers"]]
    if ticker in tickers:
        return False  # Retorna False se o ticker já existir

    data[categoria]["tickers"].append({"ticker": ticker})

    # Remover duplicados e ordenar os tickers
    unique_tickers = {item["ticker"]: item for item in data[categoria]["tickers"]}.values()
    data[categoria]["tickers"] = sorted(unique_tickers, key=lambda x: x["ticker"])

    save_data(data)
    return True  # Retorna True se o ticker for adicionado com sucesso


def montar_add():
   # Interface do Streamlit
    st.title("Adicionar Ativos")

    # Formulário para entrada de dados
    with st.form(key="add_ativo_form"):
        ticker = st.text_input("Ticker")
        categoria = st.selectbox("Categoria", ["infra", "shopping", "logistica", "acoes"])
        submit_button = st.form_submit_button(label="Adicionar Ativo")

    # Ação ao submeter o formulário
    if submit_button:
        if add_ativo(ticker, categoria):
            st.success(f"Ativo {ticker} adicionado à categoria {categoria}.")
        else:
            st.error(f"Ativo {ticker} já existe na categoria {categoria}.")



    # Exibir a lista atualizada de ativos
    st.header("Lista de Ativos")
    data = load_data()
    st.write(data)


def main():
    montar_add()



if __name__ == "__main__":
    main()
