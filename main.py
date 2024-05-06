import lyrics_scrapping as ts
import time

def main():
    title_and_lyrics = ts.get_songs_dict()
    ts.write_lyrics(title_and_lyrics)
    ts.write_songs_titles(title_and_lyrics.keys())
    print('processo finalizado')
    
if __name__ == '__main__':
    main()
