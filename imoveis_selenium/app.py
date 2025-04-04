from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(
    title="API de Imóveis",
    description="Uma API para buscar e armazenar imóveis",
    version="1.0.0"
)

# Configuração do CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (altere conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para os imóveis
class Imovel(BaseModel):
    endereco: str
    quartos: str
    banheiros: str
    vagas: str
    area: str
    descricao: str
    link: str

# Banco de dados temporário
banco_de_dados = []

@app.post("/add_imoveis/", summary="Adicionar imóveis", response_model=dict)
def add_imoveis(imoveis: List[Imovel]):
    """
    Adiciona imóveis ao banco de dados temporário.
    """
    banco_de_dados.extend(imoveis)
    return {"message": "Imóveis adicionados com sucesso!", "total": len(banco_de_dados)}

@app.get("/imoveis/", summary="Listar imóveis", response_model=List[Imovel])
def get_imoveis():
    """
    Retorna a lista de imóveis cadastrados.
    """
    return banco_de_dados


# Função para enviar dados para API

def enviar_para_api(imoveis):
    url_api = "http://127.0.0.1:8000/add_imoveis/"
    response = requests.post(url_api, json=imoveis)

    # Debug: Mostrar status e conteúdo da resposta
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        print(response.json())  # Tentar converter para JSON
    except requests.exceptions.JSONDecodeError:
        print("Erro: Resposta não é um JSON válido.")

# Web Scraping
import time
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By

def coletar_imoveis():
    driver = Driver(uc=True)
    url = "https://www.imovelweb.com.br/apartamentos-aluguel-jardim-cidade-universitaria-castelo-branco-joao-pessoa-portal-do-sol-joao-pessoa-mangabeira-joao-pessoa.html"
    driver.uc_open_with_reconnect(url, 4)

    time.sleep(5)  # Tempo de espera para evitar bloqueios do site

    enderecos = []
    quartos = []
    banheiros = []
    vagas = []
    areas = []
    detalhes = []
    links = []

    # Coleta os endereços
    adresses = driver.find_elements(By.CLASS_NAME, "postingLocations-module__location-block")
    enderecos = [adress.text.strip() for adress in adresses if adress.text.strip()]

    # Coleta as características principais (quartos, banheiros, vagas, áreas)
    features = driver.find_elements(By.CLASS_NAME, "postingMainFeatures-module__posting-main-features-listing")

    for feature in features:
        linhas = [linha.strip() for linha in feature.text.split('\n') if linha.strip()]
        temp = {'área': None, 'quarto': None, 'banheiro': None, 'vaga': None}


        for linha in linhas:
            linha_lower = linha.lower()
            if 'm²' in linha_lower:
                temp['área'] = linha
            elif 'quarto' in linha_lower:
                temp['quarto'] = linha
            elif 'banheiro' in linha_lower or 'ban' in linha_lower:
                temp['banheiro'] = linha
            elif 'vaga' in linha_lower:
                temp['vaga'] = linha

        if temp['área']:
            areas.append(temp['área'])
        if temp['quarto']:
            quartos.append(temp['quarto'])
        if temp['banheiro']:
            banheiros.append(temp['banheiro'])
        if temp['vaga']:
            vagas.append(temp['vaga'])

    # Coleta as descrições dos anúncios
    descriptions = driver.find_elements(By.CLASS_NAME, "postingCard-module__posting-description")
    detalhes = [description.text.strip() for description in descriptions if description.text.strip()]

    # Coleta os links dos imóveis
    anuncios = driver.find_elements(By.CSS_SELECTOR, "[data-to-posting]")

    for anuncio in anuncios:
        link = anuncio.get_attribute("data-to-posting")
        if link:
            links.append(f"https://www.imovelweb.com.br{link}")

    driver.quit()  # Fecha o navegador

    # Transforma os dados em um formato adequado para API
    imoveis = []
    for i in range(len(enderecos)):
        imovel = {
            "endereco": enderecos[i] if i < len(enderecos) else "Não disponível",
            "quartos": quartos[i] if i < len(quartos) else "Não informado",
            "banheiros": banheiros[i] if i < len(banheiros) else "Não informado",
            "vagas": vagas[i] if i < len(vagas) else "Não informado",
            "area": areas[i] if i < len(areas) else "Não informada",
            "descricao": detalhes[i] if i < len(detalhes) else "Sem descrição",
            "link": links[i] if i < len(links) else "#"
        }
        imoveis.append(imovel)

    # Envia para a API


    return imoveis  # Retorna os dados coletados

# Executar o scraping e enviar os dados para a API
if __name__ == "__main__":
    imoveis_coletados = coletar_imoveis()

    if imoveis_coletados:
        print("🔹 Dados coletados com sucesso!")
        enviar_para_api(imoveis_coletados)
    else:
        print("❌ Nenhum imóvel foi coletado.")

