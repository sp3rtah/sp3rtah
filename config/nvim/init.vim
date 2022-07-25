syntax enable

set wrap!
set tabstop=4
set expandtab
set autoindent
set noswapfile
" set cursorline
set scrolloff=6
set shiftwidth=4
set softtabstop=4
set encoding=utf-8
set fileformat=unix
set number relativenumber
set backspace=indent,eol,start

source $HOME/.config/nvim/keymap.vim

call plug#begin('~/.config/nvim/autoload/plugged')

Plug 'neoclide/coc.nvim', {'branch':'release'}
Plug 'anuvyklack/pretty-fold.nvim'
Plug 'mhartington/oceanic-next'
Plug 'vim-airline/vim-airline'
Plug 'karb94/neoscroll.nvim'
Plug 'jiangmiao/auto-pairs'
Plug 'tpope/vim-commentary'
Plug 'sheerun/vim-polyglot'
Plug 'cocopon/iceberg.vim'
Plug 'scrooloose/NERDTree'
Plug 'alvan/vim-closetag'
Plug 'morhetz/gruvbox'
Plug 'jacoborus/tender.vim'
Plug 'savq/melange'

call plug#end()

colorscheme tender
let g:NERDTreeMinimal =1
let NERDTreeQuitOnOpen =0
let g:closetag_shortcut = '>'
let g:airline_theme='oceanicnext'
let g:oceanic_next_terminal_bold = 0
let g:oceanic_next_terminal_italic = 0
let g:closetag_filenames = '*.html,*.xhtml'

nmap <F2> :NERDTreeToggle<CR>
