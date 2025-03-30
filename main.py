import streamlit as st
import requests
from typing import List
import urllib.parse
import re
import time
from pathlib import Path

# Função para obter as imagens do Google
def get_google_images(query: str) -> List[str]:
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&hl=pt-br&tbs=isz:l"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        image_urls = []
        pattern = r'https?://[^\s<>"]+?\.(?:jpg|jpeg|gif|png)'
        matches = re.findall(pattern, response.text)

        for url in matches:
            if 'gstatic.com' not in url and 'google.com' not in url:
                image_urls.append(url)  # Mantém a URL original

        return list(set(image_urls))[:50]  # Limita para 50 imagens únicas
    except Exception as e:
        st.error(f"Erro ao buscar imagens: {e}")
        return []

# Função para extrair nome do arquivo da URL
def get_filename_from_url(url: str) -> str:
    return Path(url).name  # Retorna apenas o nome do arquivo

# Função principal
def main():
    st.title("Google Images Grid")
    
    search_query = st.text_input("Digite sua busca", placeholder="Ex: paisagens, receitas, moda...")

    if st.button("Buscar"):
        if not search_query.strip():
            st.warning("Por favor, digite algo para buscar.")
        else:
            st.spinner("Buscando imagens...")

            # Obter as imagens
            image_urls = get_google_images(search_query)

            if image_urls:
                st.success(f"Encontradas {len(image_urls)} imagens para: {search_query}")
                cols = st.columns(5)  # Cria 5 colunas para o grid de imagens
                for i, url in enumerate(image_urls):
                    col = cols[i % 5]
                    with col:
                        st.image(url, use_column_width='auto', width=250)

                        # Obtém o nome original do arquivo
                        filename = get_filename_from_url(url)

                        # Botão de download com link direto
                        st.markdown(f'<a href="{url}" download="{filename}" target="_blank">📥 Baixar {filename}</a>', unsafe_allow_html=True)
            else:
                st.warning("Nenhuma imagem encontrada. Tente outra busca.")
    else:
        st.info("Digite um termo e clique no botão 'Buscar' para começar.")

if __name__ == "__main__":
    main()
