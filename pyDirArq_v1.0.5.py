#===================================================================================================
# Programa : pyDirArq_v1.0.5.py
# Descrição: salva arquivos e subdiretórios de um diretorio totalizando o tamanho dos arquivos e
# subdiretórios.
#---------------------------------------------------------------------------------------------------
# Data : 23/06/2026 ter
#---------------------------------------------------------------------------------------------------
# Utilização: 
# 
#---------------------------------------------------------------------------------------------------
# Versão 1.0.5 - adicionado ao script 1.0.4 "EstouVivo";
# Versão 1.0.4 - apresenta a raíz a cada iteração do loop for: 
# 'for raiz, dirs, arquivos in os.walk(pathDir_)'
# Versão 1.0.3 - apresenta os subdiretórios e arquivos de todos os níveis;
# Versão 1.0.2 - apresenta os subdiretórios e arquivos do Nível1;
# Versão 1.0.1 - apresenta os subdiretórios e arquivos;
# Versão 1.0.0 - versão inicial;
#===================================================================================================
#===================================================================================================
# Imports
#===================================================================================================
import os
import sys
import time
import threading
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
# Classe EstouVivo
#===================================================================================================
class EstouVivo:
    """Indicador visual 'estou vivo' para loops demorados."""

    def __init__(self, estilo='spinner'):
        self.estilo = estilo
        self._ativo = False
        self._thread = None
        self._inicio = None

    def _spinner(self):
        # Caracteres ASCII: | (124), / (47), - (45), \ (92)
        chars = [124, 47, 45, 92]
        i = 0
        while self._ativo:
            elapsed = time.time() - self._inicio
            sys.stdout.write(f'\r⏳ Escaneando... {chr(chars[i % 4])}  [{time.strftime("%H:%M:%S", time.gmtime(elapsed))}]')
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()

    def _pontos(self):
        i = 0
        while self._ativo:
            elapsed = time.time() - self._inicio
            pontos = '.' * ((i % 6) + 1)
            sys.stdout.write(f'\r⏳ Escaneando{pontos:<6} [{elapsed:.0f}s]')
            sys.stdout.flush()
            time.sleep(0.4)
            i += 1
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()

    def iniciar(self, mensagem='Escaneando'):
        """Ativa o indicador. Retorna o próprio objeto para uso com 'with'."""
        self._inicio = time.time()
        self._ativo  = True
        metodo       = self._spinner if self.estilo == 'spinner' else self._pontos
        self._thread = threading.Thread(target=metodo, daemon=True)
        self._thread.start()
        print(f'▶️  Estou vivo ATIVADO — {mensagem}')
        return self

    def parar(self):
        """Desativa o indicador."""
        self._ativo = False
        if self._thread:
            self._thread.join(timeout=1)
        elapsed = time.time() - self._inicio
        #print(f'⏹️  Estou vivo DESATIVADO — {elapsed:.1f}s decorridos')
        sys.stdout.write(f'⏹️  Estou vivo DESATIVADO — decorridos: [{time.strftime("%H:%M:%S", time.gmtime(elapsed))}]')

    # Suporte ao gerenciador de contexto (with)
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.parar()

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
    elif flag_debug:
        printStyled(f'\n{"TAMANHO":>12}  {"SUBDIRETÓRIO"}\n{"="*50}', fg='CYAN')
    printStyled(f'\n{"Aguarde o escaneamento ...\n"}', fg='GREEN')
    
    #--- Ativa o indicador "Estou vivo" com spinner
    with EstouVivo(estilo='spinner').iniciar('Escaneando diretório'):
        #------------------------------------------------
        for raiz, dirs, arquivos in os.walk(pathDir_):
        #------------------------------------------------
            if (flag_debug and not flag_debug_Raiz):
                printStyled(f'nivel = {intNivel} - {raiz}', fg='GREEN')
                printStyled(f'-Qtidd Subdir   = {len(dirs)}', fg='YELLOW')
                print (f'dirs     = {dirs}')
                printStyled(f'-Qtidd Arquivos = {len(arquivos)}', fg='YELLOW')
                print (f'arquivos = {arquivos}\n')
            elif flag_debug_Raiz:
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
# Fim do arquivo pyDirArq_v1.0.5.py