#===================================================================================================
# Programa : pyDirArq_v1.0.4.py
# Descrição: salva arquivos e subdiretórios de um diretorio totalizando o tamanho dos arquivos e
# subdiretórios.
#---------------------------------------------------------------------------------------------------
# Data : 23/06/2026 ter
#---------------------------------------------------------------------------------------------------
# Utilização: 
# 
#---------------------------------------------------------------------------------------------------
# Versão 1.0.4 - apresenta a raíz a cada iteração do loop for: 
# 'for raiz, dirs, arquivos in os.walk(pathDir_)'; usa "Estou vivo";
# Versão 1.0.3 - apresenta os subdiretórios e arquivos de todos os níveis;
# Versão 1.0.2 - apresenta os subdiretórios e arquivos do Nível1;
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

from colorama import Back, Fore, Style, init
init()    # Initialize colorama (required for Windows)

#-------------------------------------------------------------------------------
# Instancializações e inicializações
#-------------------------------------------------------------------------------
flag_debug = True #False

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

#===================================================================================================
# Função principal
#===================================================================================================
def main(pathDir_, pathDirRels_):

    total_geral = 0
    intNivel    = 1

    flag_debug_Raiz = True
    if (flag_debug_Raiz):
        msgDebug   = ""
        #total_Raiz = 1

    elif flag_debug:
        printStyled(f'\n{"TAMANHO":>12}  {"SUBDIRETÓRIO"}\n{"="*50}', fg='CYAN')

    printStyled(f'\n{"Aguarde o escaneamento ...\n"}', fg='GREEN')

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

        if (flag_debug and not flag_debug_Raiz):

            printStyled(f'nivel = {intNivel} - {raiz}', fg='GREEN')

            printStyled(f'-Qtidd Subdir   = {len(dirs)}', fg='YELLOW')
            print (f'dirs     = {dirs}')
            printStyled(f'-Qtidd Arquivos = {len(arquivos)}', fg='YELLOW')
            print (f'arquivos = {arquivos}\n')

        elif flag_debug_Raiz:

            #total_Raiz += {len(raiz)}
            msgTmp      = f'\nnivel = {intNivel} - {raiz}'
            msgDebug   += msgTmp

        intNivel += 1

    #--- Finalização do escaneamento
    if (flag_debug and not flag_debug_Raiz):
        printStyled(f'{"="*50}', fg='CYAN')
        printStyled(f'{total_geral:>12,} bytes  TOTAL ({pathDir_})', fg='CYAN')
    elif flag_debug_Raiz:
        printStyled(f'Raízes a cada nível:\n{msgDebug}', fg='YELLOW')

#===================================================================================================
# Ponto de entrada do programa
#===================================================================================================
if __name__ == '__main__':

    strDir  = filedialog.askdirectory(title = "Selecione o diretório a ser processado:").replace('/', '\\')
    printStyled (f"\nDiretório a ser processado: strDir = '{strDir}'", fg='GREEN')
    pathDir = Path(strDir)

    strDirRels = filedialog.askdirectory(title = "Selecione o diretório para salvar os arquivos-relatórios:").replace('/', '\\')
    printStyled (f"Diretório para salvar os arquivos-relatórios: strDirRels = '{strDirRels}'", fg='GREEN')
    pathDirRels = Path(strDirRels)

    #----------------------------
    main(pathDir, pathDirRels)
    #----------------------------

# Fim do programa

#===================================================================================================
# Fim do arquivo pyDirArq_v1.0.4.py