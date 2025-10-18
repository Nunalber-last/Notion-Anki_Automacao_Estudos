import base64
import os
import re
import time
import requests
from notion_client import Client

# === Configurações iniciais ===
NOTION_API_KEY = "_____________________________"
DATABASE_ID = "_____________________________"
ANKI_CONNECT_URL = "http://localhost:______"

# Conexão com o Notion
notion = Client(auth=NOTION_API_KEY)


# === 1. Obter dados da base do Notion ===
def get_notion_data():
    response = notion.databases.query(database_id=DATABASE_ID)
    results = response.get("results", [])
    data = []

    for page in results:
        props = page["properties"]

        # Captura dos campos (respeitando seus nomes reais)
        titulo = props.get("titulo", {}).get("title", [])
        frente = props.get("frente", {}).get("rich_text", [])
        verso = props.get("verso", {}).get("rich_text", [])
        imagem = props.get("imagem", {}).get("files", [])
        data_prop = props.get("data_prop", {}).get("date", {})

        # Extrair texto de cada campo
        titulo_text = titulo[0]["text"]["content"] if titulo else ""
        frente_text = frente[0]["text"]["content"] if frente else ""
        verso_text = verso[0]["text"]["content"] if verso else ""
        data_text = data_prop.get("start", "") if data_prop else ""

        # Extrair URL da imagem (caso exista)
        imagem_url = ""
        if imagem:
            img = imagem[0]
            if "file" in img and "url" in img["file"]:
                imagem_url = img["file"]["url"]
            elif "external" in img and "url" in img["external"]:
                imagem_url = img["external"]["url"]

        # Adiciona só se houver conteúdo (para evitar erro de card vazio)
        if titulo_text or frente_text or verso_text:
            data.append({
                "titulo": titulo_text,
                "frente": frente_text,
                "verso": verso_text,
                "imagem": imagem_url,
                "data": data_text
            })

    return data


# === Função para criar nomes de arquivos seguros ===
def gerar_nome_imagem_seguro(titulo, url):
    """Gera nome de arquivo seguro baseado no título e timestamp."""
    base_nome = re.sub(r'[^a-zA-Z0-9_-]+', '_', titulo.lower())[:50]  # limita tamanho
    ext = os.path.splitext(url.split("?")[0])[-1] or ".jpg"  # mantém extensão
    nome_seguro = f"{base_nome}_{int(time.time())}{ext}"
    return nome_seguro


# === 2. Upload da imagem para o Anki ===
def upload_image_to_anki(image_url, titulo):
    """Baixa a imagem, renomeia e envia para o Anki via storeMediaFile."""
    if not image_url:
        return ""

    try:
        img_data = requests.get(image_url).content
        filename = gerar_nome_imagem_seguro(titulo, image_url)
        payload = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": filename,
                "data": base64.b64encode(img_data).decode("utf-8")
            }
        }
        response = requests.post(ANKI_CONNECT_URL, json=payload).json()
        if response.get("error") is None:
            print(f"🖼️ Imagem salva no Anki: {filename}")
            return filename  # retorna nome limpo
        else:
            print("Erro ao salvar imagem:", response)
            return ""
    except Exception as e:
        print("Falha ao baixar imagem:", e)
        return ""


# === 3. Enviar cada registro ao Anki ===
def add_to_anki(card):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "NotionCards",
                "modelName": "NotionBasic",
                "fields": {
                    "titulo": card["titulo"],
                    "frente": card["frente"],
                    "verso": card["verso"],
                    "imagem": f"<img src='{card['imagem']}'>" if card["imagem"] else "",
                    "data": card["data"]
                },
                "options": {"allowDuplicate": False},
                "tags": ["notion"]
            }
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload)
    return response.json()


# === 4. Executar o processo ===
if __name__ == "__main__":
    flashcards = get_notion_data()
    print(f"📚 Cartões encontrados no Notion: {len(flashcards)}")

    for card in flashcards:
        print(f"→ Processando: {card['titulo']}")

        # Baixa e envia a imagem (caso exista)
        if card["imagem"]:
            card["imagem"] = upload_image_to_anki(card["imagem"], card["titulo"])
        else:
            card["imagem"] = ""

        # Envia ao Anki
        result = add_to_anki(card)
        print(f"✅ Resultado: {result}")
