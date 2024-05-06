import lyrics_scrapping as ls
import time

def main():
    start = time.time()
    title_and_lyrics = ls.get_songs_dict()
    ls.write_lyrics(title_and_lyrics)
    ls.write_songs_titles(title_and_lyrics.keys())
    print('processo finalizado')
    end_time = time.time() - start
    print(f'Tempo total de execução: {end_time}')
    
if __name__ == '__main__':
    main()
