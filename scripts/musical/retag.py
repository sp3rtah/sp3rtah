"""
author: sp3rtah
purpose: Batch rename distorted music file names based on the embedded artist and song name
dependencies: music-tag, alive-progress
"""
import os
import string
import music_tag
from alive_progress import alive_bar

invalid = """
official music video audio final lyrics cover acoustic skiza vevo tv new mp3 com y2mate
"""
invalid_words = [i for i in invalid.replace('\n',' ').split(' ') if i]

def clean_name(name: str, ext: str):
    valid = '_-'
    new_name = str()
    for c in name:
        if c in string.punctuation:
            if c not in valid:
                if c == '.':
                    new_name += ' '
                continue
        new_name += c
    new_name = new_name.lower().strip('-').strip()
    for word in new_name.split(' '):
        if word.lower() in invalid_words:
            new_name = new_name.replace(word,'')
        else:
            for inner in invalid_words:
                if word.lower() in inner:
                    new_name = new_name.replace(word,'')
    new_name = new_name.replace(' '*2,' ').strip().strip('-').strip()
    return f'{new_name.title()}.{ext}'

def rename(name: str) -> bool:
    f = music_tag.load_file(name)
    new_name = str()
    extension = name.split('.')[-1]
    if f['artist']:
        new_name += str(f['artist'])
    if f['title']:
        title = str(f['title']).strip()
        if new_name.lower() in title.lower():
            new_name = str()
        if '-' not in title:
            title = f' - {title}'
        new_name += title
    if not new_name.strip():
        new_name = name
    try:
        if not os.path.exists(_new:=clean_name(new_name, extension)):
            os.rename(name,_new)
        return True
    except Exception as e:
        print(f'Failed rename: {str(e)}')
    return False

if __name__ == '__main__':
    songs_folder = os.path.join('C:\\','Users','The Alchemist','Music')
    os.chdir(songs_folder)
    songs = [f.name for f in os.scandir('.') if f.name.split('.')[-1] in ['mp3','m4a'] and f.is_file()]
    if not songs:
        print('No songs found in Music folder!')
        exit(1)
    with alive_bar(len(songs)) as bar:
        for song in songs:
            if rename(song):
                bar()
