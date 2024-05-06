# Explorando Discografias com Python e Web Scraping 🖥️🐍

Este projeto consiste em um script Python que utiliza técnicas de Web Scraping para extrair automaticamente os títulos das músicas e suas letras de um site de letras de músicas. O objetivo é facilitar a análise e exploração da discografia de artistas musicais

## Funcionalidades

1. **Extrair Títulos das Músicas:** 

    O script percorre uma página de discografia de um artista específico e extrai os títulos das músicas listadas.

2. **Extrair Letras das Músicas:**

    Para cada música, o script acessa a página da letra individual e extrai o conteúdo da letra.

3. **Processamento Paralelo:**

    Utiliza threads para processamento paralelo, otimizando o tempo de extração de dados. Para a minha máquina, houve um speedup de aproximadamente **5x**.

4. **Exportar Dados:**

    O resultado final é um dicionário contendo os títulos das músicas como chaves e as letras como valores, além de uma lista simples dos títulos para referência rápida.

## Como Usar

Clone este repositório:

    git clone https://github.com/manuguse/letras-de-musicas-web-scraping.git

Instale as dependências necessárias:

    pip install requests

Execute o script main.py:

    python main.py

Após a execução, os dados serão salvos em arquivos de texto: songs_dict.txt (dicionário de títulos e letras) e titles_list.txt (lista de títulos).

Requisitos:

    Python 3.x
    Bibliotecas Python: requests

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de recebimento.
