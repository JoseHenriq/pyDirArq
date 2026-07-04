#===================================================================================================
# Programa : pyDirArq_v1.0.0.py
# Descrição: apresenta arquivos e subdiretórios de um diretorio totalizando o tamanho dos arquivos e
# subdiretórios.
#---------------------------------------------------------------------------------------------------
# Data : 22/06/2026 seg
#---------------------------------------------------------------------------------------------------
# Utilização: 
# 
#---------------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
# Função : analisa o diretório e apresenta o tamanho dos arquivos e subdiretórios
#-------------------------------------------------------------------------------
def analisar_diretorio(caminho):

    printStyled(f'\n{"TAMANHO":>12}  {"SUBDIRETÓRIO"}\n{"="*50}', fg='CYAN')
    total_geral = 0

    for raiz, dirs, arquivos in os.walk(caminho):
        soma_dir = 0
        for arq in arquivos:
            try:
                soma_dir += os.path.getsize(os.path.join(raiz, arq))
            except OSError:
                continue

        if soma_dir > 0:
            print(f'{soma_dir:>12,} bytes  {raiz}')
            total_geral += soma_dir

    printStyled(f'{"="*50}', fg='CYAN')
    printStyled(f'{total_geral:>12,} bytes  TOTAL ({caminho})', fg='CYAN')

#===================================================================================================
# Função principal
#===================================================================================================
def main(pathDir_, pathArqRels_): 

    #--------------------------------------
    # Instancializações e inicializações
    #--------------------------------------
    global ScriptName
    ScriptName = os.path.basename(__file__)

    ararArquivos = []
    ararSubdirs  = []

    totalFileSize   = 0.0
    totalSubdirSize = 0.0

    dataHora         = PreparaDataHora('%y%m%d%H%M%S')
    strRelatorioTxt  = f"Relatorio_{dataHora}.txt"
    pathRelatorioTxt = os.path.join(pathArqRels_, strRelatorioTxt)
    printStyled (f"Relatório a ser gerado: pathRelatorioTxt = '{pathRelatorioTxt}'", fg='YELLOW', bold=True)

    #-------------------------------------------------------------------------
    # Escaneia o diretório e armazena os arquivos e subdiretórios em listas
    #-------------------------------------------------------------------------
    try:

        if not os.path.exists(pathDir_):
            printStyled(f" O diretório '{pathDir_}' não existe.", fg='RED')
            return
        
        if not os.path.exists(pathArqRels_):
            printStyled(f" O diretório '{pathArqRels_}' não existe.", fg='RED')
            return
        
        #--------------------------------------------
        for root, dirs, files in os.walk(pathDir_):
        #--------------------------------------------    
            for file in files:
                ararArquivos.append(os.path.join(root, file))

            for dir in dirs:
                ararSubdirs.append(os.path.join(root, dir))
    
    except Exception as e:

        printStyled(f" Erro ao escanear o diretório: {e}", fg='RED')
        return  

    #----------------------------------------------------
    # Apresenta as listas dos arquivos e subdiretórios
    #----------------------------------------------------
    if flag_debug:
        printStyled(f'- tam_ararArquivos = {len(ararArquivos)} ítens', fg='CYAN')
        printStyled(f'- tam_ararSubdirs  = {len(ararSubdirs)} ítens', fg='CYAN')

    if len(ararArquivos) == 0:
        printStyled(f"O diretório '{pathDir_}' não contém arquivos.", fg='RED')
    else:
        printStyled("\n-->Arquivos encontrados em '{pathDir_}':", fg='GREEN')
        for arquivo in ararArquivos:
            print(f"  {arquivo}")

    if len(ararSubdirs) == 0:
        printStyled(f"O diretório '{pathDir_}' não contém subdiretórios.", fg='RED')
    else:
        printStyled("\n--> Subdiretórios encontrados em '{pathDir_}':", fg='GREEN')
        for subdiretorio in ararSubdirs:
            print(f"  {subdiretorio}")
  
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
    #main(pathDir, pathDirRels)
    analisar_diretorio(pathDir)
    #----------------------------

# Fim do programa

#===================================================================================================
# Fim do arquivo pyDirArq_v1.0.0.py
