"""
author: sp3rtah
purpose: Batch convert m4a and mp4 media files to mp3
dependancies: ffmpeg
"""

import os
from concurrent.futures import ProcessPoolExecutor as PPE

def work_this(work: str):
    os.system(work)

def transcode(files: list):
    transcode_path = 'transcoded'
    if not os.path.exists(dest:=transcode_path):
        os.mkdir(dest)
    cmd = 'ffmpeg -i "{input_name}" "{output_name}.mp3"'
    works = set()
    for f in files:
        out_name = f.split('.m4a')[0].replace('.',' ').strip()
        works.add(cmd.format(input_name=f,output_name=os.path.join(transcode_path,out_name)))
    with PPE() as executor:
        executor.map(work_this,works)

if __name__ == '__main__':
    os.chdir(os.path.join('C:\\','Users','The Alchemist','Desktop','Transcode'))
    files = [f.name for f in os.scandir('.') if f.is_file() if f.name.split('.')[-1] in ['m4a','mp4']]
    if not files:
        print('No valid files found!')
        exit(1)
    transcode(files)
