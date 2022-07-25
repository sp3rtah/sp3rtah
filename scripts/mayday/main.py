import cv2
import lzma
import os, sys
import argparse
import numpy as np


class Mayday:
    def __init__(self, keyimage:str, dataimage:str, folder:str) -> None:
        def get_path(fname: str) -> str:
            return os.path.join(folder, fname)
        # 
        stream_delimiter = b'#shenzi#'

        if folder:
            files = [file.name for file in os.scandir(folder) if file.is_file()]
            keyfile = [i for i in [key for key in files if 'rsa' in key] if i]
            if not keyfile:
                print('Private key is missing!')
                sys.exit(1)
            #
            keyfile = keyfile[0]
            files = [f for f in files if '.zip' in f]
            with open(get_path(keyfile), 'rb') as kf:
                kimage = cv2.imread(keyimage)
                print('Encoding ssh key...')
                Mayday.encodeData(kimage, kf.read())
                cv2.imwrite(get_path(keyimage), kimage)
            # 
            payload = b''
            for file in files:
                with open(get_path(file),'rb') as infile:
                    payload += infile.read() + stream_delimiter + file.encode('utf8') + stream_delimiter
            if not payload:
                print('No payload found!')
                sys.exit(1)
            enc = lzma.compress(payload)
            print(f'payload size: {len(payload)}\ncompressed size: {len(enc)}')
            dimage = cv2.imread(dataimage)
            print('Encoding payload...')
            Mayday.encodeData(dimage,enc)
            cv2.imwrite(get_path(dataimage),dimage)
        else:
            kimage = cv2.imread(keyimage)
            dimage = cv2.imread(dataimage)
            with open('id_rsa','wb') as kf:
                print('Decoding ssh key...')
                kf.write(ssh_key:=Mayday.decodeData(kimage))
            if not ssh_key:
                return
            print('Decoding payload...')
            payload = lzma.decompress(Mayday.decodeData(dimage))
            data = [i for i in payload.split(stream_delimiter) if i]
            for i in range(len(data)):
                if i % 2 == 0:
                    continue
                with open(data[i],'wb') as outfile:
                    outfile.write(data[i-1])

    @classmethod
    def toBits(cls, data):
        if type(data) == str:
            return ''.join([f'{ord(i):08b}' for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            return [f'{i:08b}' for i in data]
        elif type(data) == int or type(data) == np.uint8:
            return f'{data:08b}'
        print('Data type not supported!')
        sys.exit(1)

    @classmethod
    def decodeData(cls, image: np.ndarray) -> bytes:
        out = ''
        stopflag = Mayday.toBits('#.ke.#')
        for value in image:
            for pixel in value:
                b,g,r = Mayday.toBits(pixel)
                if b[-1] == '0':
                    out += g[-1]
                else:
                    out += r[-1]
        out = out.split(stopflag)[0]
        out = [int(out[i:i+8],2) for i in range(0,len(out),8)]
        return bytearray(out)

    @classmethod
    def encodeData(cls,image: np.ndarray, secret: bytes):
        stopflag = '#.ke.#'
        secret_bits = ''.join(Mayday.toBits(secret)) + Mayday.toBits(stopflag)
        ###
        h, w, channels = image.shape
        if channels != 3:
            print(f'Invalid channel count in image! {channels}')
            sys.exit(1)
        # 
        pixels = h * w
        bit_len = len(secret_bits)
        max_bit_len = pixels * (channels-1)
        #
        if bit_len > max_bit_len:
            print(f'Not enough bits! extra required: {len(secret_bits)-max_bit_len}')
            sys.exit(1)
        
        bit_index = 0
        for value in image:
            for pixel in value:
                b,g,r = Mayday.toBits(pixel)
                if b[-1] == '0':
                    if bit_index < bit_len:
                        pixel[1] = int(g[:-1] + secret_bits[bit_index],2)
                        bit_index += 1
                elif bit_index < bit_len:
                    pixel[2] = int(r[:-1] + secret_bits[bit_index],2)
                    bit_index += 1
            if bit_index > bit_len:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='folder',help='Folder with id_rsa and *.zip backup file')
    parser.add_argument('keyimage')
    parser.add_argument('dataimage')
    args = parser.parse_args()
    Mayday(args.keyimage,args.dataimage,args.folder)

