"""
author: sp3rtah
purpose: Batch rename files based on regex input
depenencies: None
"""
import os
import sys, re

changes = [1]

def rollback():
    print('\t<rolling back changes>',end=' ')
    for change in changes:
        os.rename(change[1],change[0])
    print('[done]')

def rename(files):
    pat = str(input('Enter regex pattern: ')).strip()
    replacer = str(input('Replace with: ')).strip()
    try:
        pat = re.compile(pat)
        for file in files:
            found = re.search(pat,file)
            if not found:
                continue
            span = found.span()
            ## not match
            if span[0] == span[1]:
                continue
            to_replace = file[span[0]:span[1]]
            result = file.replace(to_replace,replacer)
            print(f'[renaming]: <{file[:6]}> --> <{result[:6]}>',end=' ')
            os.rename(file,result)
            changes.append((file,result))
            print('[done]')
    except re.error as e:
        print(f'RegexError: {e}')
        return
    except Exception as e:
        print(e)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("[usage]:\n$ batr <files>")
    else:
        files = [f for f in sys.argv[1:] if os.path.exists(f)]
        if not files:
            print('Warning: No files found!')
            exit(1)
        try:
            rename(files)
        except KeyboardInterrupt:
            if changes:
                opt = input(str(f'\n>> Rollback {len(changes)} changes?\t'))
                if opt.lower() not in 'no':
                    rollback()
        print('[Done...]')
