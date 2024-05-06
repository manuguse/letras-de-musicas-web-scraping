import requests
from html.parser import HTMLParser
from threading import Thread, Lock
from time import time


class SongsParser(HTMLParser):
    """ 
    Um parser de HTML customizado para extrair títulos de músicas e as URLs de suas letras.

    Este parser é projetado para analisar a estrutura HTML da página de discografia da Taylor Swift no site Letras.mus.br.
    Ele procura por tags 'li' que contenham a classe 'songList-table-row --song isVisible' e extrai o nome da música e a URL da letra.
    Músicas que são versões alternativas (remix, live, demo, etc) são ignoradas.

    As informações extraídas são armazenadas em um dicionário, onde as chaves são os nomes das músicas
    e os valores são as URLs das letras.
    """
    def __init__(self):
        super().__init__()
        self.songs = dict()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'li' and attrs.get('class') == 'songList-table-row --song isVisible':
            name = attrs.get('data-name').strip()
            wrong_words = ['remix', 'version', 'live', 'acoustic', 'demo', 'voice memo', 'the vault', 'long pond']
            for word in wrong_words:
                if word in name.lower():
                    return
            self.songs[name] = attrs.get('data-shareurl').strip()

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
    
class LyricsParser(HTMLParser):
    """ 
    Um parser de HTML customizado para extrair as letras das músicas.
    
    Usando como base a estrutura HTML da página de letra de uma música no site Letras.mus.br,
    o parser entra na tag 'div' que contém a classe 'lyric-original' e extrai o conteúdo da letra.
    
    Ele também trata as tags 'br' e 'p' para adicionar quebras de linha no texto extraído. A letra
    é armazenada em um atributo 'lyrics' do objeto.
    """

    def __init__(self):
        super().__init__()
        self.lyrics = ''
        self.inside_lyrics = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and attrs.get('class') == 'lyric-original':
            self.inside_lyrics = True
        elif tag == 'br' and self.inside_lyrics:
            self.lyrics += '\n'  
            self.is_first_line = False
        elif tag == 'p' and self.inside_lyrics:
            self.lyrics += '\n'

    def handle_endtag(self, tag):
        if tag == 'div':
            self.inside_lyrics = False

    def handle_data(self, data):
        if self.inside_lyrics:
            self.lyrics += data
    
def get_lyrics(url):
    """ 
    Método que faz uma requisição GET para a URL da letra de uma música e extrai o conteúdo da letra
    utilizando o parser de letras.
    """
    request = requests.get(url)
    parser = LyricsParser()
    parser.feed(request.content.decode('utf-8')) # pega o conteudo da pagina
    return parser.lyrics

def write_songs_titles(songs):
    """ 
    Método que escreve os títulos das músicas em um arquivo de texto, no formato de lista.
    """
    with open('titles_list.txt', 'w') as file:
        file.write(str(list(songs)))
        
def write_lyrics(lyrics):
    """ 
    Método que escreve as letras das músicas em um arquivo de texto, no formato de dicionário.
    """
    with open('songs_dict.txt', 'w') as file:
        file.write(str(lyrics))
        
def get_songs_urls():
    """"
    Método que faz uma requisição GET para a página de discografia da Taylor Swift e extrai os títulos.
    Retorna um objeto do parser de músicas.    
    """
    request = requests.get('https://www.letras.mus.br/taylor-swift/discografia/')
    parser = SongsParser()
    parser.feed(request.content.decode('utf-8')) # pega o conteudo da pagina
    return parser
    
def get_songs_dict():
    title_and_lyrics = dict()
    lock = Lock()  # Para garantir acesso seguro ao dicionário
    def fetch_lyrics(url, title):
        nonlocal title_and_lyrics
        lyrics = get_lyrics(url)
        with lock:
            title_and_lyrics[title] = lyrics
    
    songs_urls = get_songs_urls().songs.items()
    threads = []
    for title, url in songs_urls:
        thread = Thread(target=fetch_lyrics, args=(url, title))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return title_and_lyrics
