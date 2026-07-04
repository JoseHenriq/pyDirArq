#===================================================================================================
# Programa : pyDirArq_v1.0.2.py
# Descrição: salva arquivos e subdiretórios de um diretorio totalizando o tamanho dos arquivos e
# subdiretórios.
#---------------------------------------------------------------------------------------------------
# Data : 23/06/2026 ter
#---------------------------------------------------------------------------------------------------
# Utilização: 
# 
#---------------------------------------------------------------------------------------------------
# Versão 1.0.2 - apresenta os subdiretórios e arquivos conforme C# DirArq;
# Versão 1.0.1 - apresenta os subdiretórios e arquivos;
# Versão 1.0.0 - versão inicial;
#===================================================================================================

#===================================================================================================
# Imports
#===================================================================================================
import os
import datetime
from pathlib import Path
from tkinter import filedialog
import locale

from colorama import Back, Fore, Style, init
init()    # Initialize colorama (required for Windows)

#-------------------------------------------------------------------------------
# Instancializações e inicializações
#-------------------------------------------------------------------------------
flag_debug = True #False

largura_msg = 80
largura_d1  = 30
largura_d2  = 24

#===================================================================================================
# Funções 
#===================================================================================================
#-------------------------------------------------------------------------------
# Função : lê a data e hora do sistema e formata para o padrão brasileiro
# entrada: formatoDataHora; ex: '%d/%m/%y %H:%M:%S %a' "17/10/23 Ter 06:27:00" 
# (%a = dia da semana abreviado, ex: Ter)
# saída  : data e hora formatada
#-------------------------------------------------------------------------------
def PreparaDataHora(formatoDataHora):
    
    # Dicionário para converter o dia da semana de inglês para português
    dias_da_semana = {
        'Mon': 'Seg',
        'Tue': 'Ter',
        'Wed': 'Qua',
        'Thu': 'Qui',
        'Fri': 'Sex',
        'Sat': 'Sáb',
        'Sun': 'Dom'
    }

    #---------------------------------------------------------------------
    data_hora_atual = datetime.datetime.now().strftime(formatoDataHora)
    #---------------------------------------------------------------------

    # Se o formato da data e hora contiver o dia da semana (%a), substitui o dia da semana em inglês pelo dia da semana em português
    if ('%a' in formatoDataHora) :
        dia_da_semana   = data_hora_atual[-3:]                   # extrai os últimos 3 caracteres (%a)
        dia_da_semana   = dias_da_semana [dia_da_semana]         # converte para o dia da semana em português
        data_hora_atual = data_hora_atual[:-3] + dia_da_semana   

    if ('%f' in formatoDataHora) :
        data_hora_atual = data_hora_atual[:-3]

    return data_hora_atual

#-------------------------------------------------------------------------------
# Apresentação das mensagens com estilos ajustáveis
#-------------------------------------------------------------------------------
def printStyled(text, fg=None, bg=None, bold=False, underline=False):

    """
    Prints styled colored text to the terminal.
    Args:
        text (str) : Text to print;
        fg (str)   : Foreground color: 'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE'. Default: 'WHITE'.
        bg (str)   : Background color: same options as fg. Default: None (no change).
        bold (bool): If True, text is bold.
        underline (bool): If True, text is underlined.
    """

    #--- Color maps
    # Foreground
    COLORS_FG = {
        'BLACK'  : Fore.BLACK,
        'RED'    : Fore.RED,
        'GREEN'  : Fore.GREEN,
        'YELLOW' : Fore.YELLOW,
        'BLUE'   : Fore.BLUE,
        'MAGENTA': Fore.MAGENTA,
        'CYAN'   : Fore.CYAN,
        'WHITE'  : Fore.WHITE,
    }
    # Background
    COLORS_BG = {
        'BLACK'  : Back.BLACK,
        'RED'    : Back.RED,
        'GREEN'  : Back.GREEN,
        'YELLOW' : Back.YELLOW,
        'BLUE'   : Back.BLUE,
        'MAGENTA': Back.MAGENTA,
        'CYAN'   : Back.CYAN,
        'WHITE'  : Back.WHITE,
    }

    # Defaults
    fg_code = COLORS_FG.get(fg, Fore.WHITE)
    bg_code = COLORS_BG.get(bg, '')
    style_code = ''
    if bold:
        style_code += Style.BRIGHT
    if underline:
        # ANSI underline is not well supported in all terminals, but we can try
        style_code += '\033[4m'

    # Print styled text
    #-----------------------------------------------------------------
    print(f"{bg_code}{fg_code}{style_code}{text}{Style.RESET_ALL}")
    #-----------------------------------------------------------------

    largura_msg = 80
    largura_d1  = 30
    largura_d2  = 24

#-------------------------------------------------------------------------------
# Formata para numeração br
# print(formatar_int_br(1234567))  # 1.234.567
# print(formatar_int_br(89123))    # 89.123
#-------------------------------------------------------------------------------
def formatar_float_br(valor: int) -> str:

    temp = f"{valor:,}"
    return temp.replace(",", ".")

#===================================================================================================
# Função principal
#===================================================================================================
def main(pathDir_, pathDirRels_):

    if not os.path.exists(pathDir_):
        printStyled(f" O diretório '{pathDir_}' não existe.", fg='RED')
        return
    
    if not os.path.exists(pathDirRels_):
        printStyled(f" O diretório '{pathDirRels_}' não existe.", fg='RED')
        return
        
    total_geral:float = 0

    intNivel    = 1
    #------------------------------------------------
    for raiz, dirs, arquivos in os.walk(pathDir_):
    #------------------------------------------------

        ''' Escaneia o diretório e calcula o tamanho dos arquivos e subdiretórios
        soma_Dirs = 0
        for dir in dirs:
            try:
                tam_dir    = os.path.getsize(os.path.join(raiz, dir))
                soma_Dirs += tam_dir
            except OSError:
                continue

            soma_Arq = 0
            for arq in arquivos:
                try:
                    tam_Arq   = os.path.getsize(os.path.join(raiz, arq))
                    soma_Arq += tam_Arq
                except OSError:
                    continue

                if tam_Arq > 0:
                    print(f'{arq} {tam_Arq:>12,} bytes')
                    total_geral += soma_Arq
        '''

        tam_Arq:float = 0
        tam_dir:float = 0

        total_SubDir:float = 0
        total_Arq:float    = 0
        if (intNivel == 1):

            for dir in dirs:

                try:
                    tam_dir       = os.path.getsize(os.path.join(raiz, dir))
                    total_SubDir += tam_dir
                except OSError:
                    continue

                printStyled(f'Diretorio: {dir:<{largura_d1}} {formatar_float_br(tam_dir):>{largura_d2}} bytes', fg='YELLOW')

            for arq in arquivos:
                try:
                    tam_Arq    = os.path.getsize(os.path.join(raiz, arq))
                    total_Arq += tam_Arq
                except OSError:
                    continue

                printStyled(f'Arquivo  : {arq:<{largura_d1}} {formatar_float_br(tam_Arq):>{largura_d2}} bytes', fg='WHITE')

        else:

            break

        total_geral += total_SubDir + total_Arq
        
        intNivel += 1

    printStyled(f'{"="*int(largura_msg)}', fg='CYAN')
    printStyled(f'{" "*(int(largura_d1) + 8)} TOTAL ({pathDir_}): {formatar_float_br(total_geral):>12} bytes', fg='CYAN')

#===================================================================================================
# Ponto de entrada do programa
#===================================================================================================
if __name__ == '__main__':

    strDir  = filedialog.askdirectory(title = "Selecione o diretório a ser processado:").replace('/', '\\')
    printStyled (f"\nDiretório a ser processado: strDir = '{strDir}'", fg='CYAN')
    pathDir = Path(strDir)

    strDirRels = filedialog.askdirectory(title = "Selecione o diretório para salvar os arquivos-relatórios:").replace('/', '\\')
    printStyled (f"Diretório para salvar os arquivos-relatórios: strDirRels = '{strDirRels}'", fg='CYAN')
    pathDirRels = Path(strDirRels)

    #----------------------------
    main(pathDir, pathDirRels)
    #----------------------------

    printStyled(f'{"="*int(largura_msg)}', fg='CYAN')
    printStyled(f'Fim do processamento', fg='YELLOW', bold=True)

#===================================================================================================
# Fim do arquivo pyDirArq_v1.0.2.py