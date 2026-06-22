#===================================================================================================
# Programa : pyDirArq_v1.0.0.py
# Descrição: apresenta arquivos e subdiretórios de um diretorio totalizando o tamanho dos arquivos e
# subdiretórios.
#---------------------------------------------------------------------------------------------------
# Data : 22/06/2026 dom
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
from os.path import exists
import datetime

from pathlib import Path

import tkinter.filedialog as filedialog
import pandas as pd
import csv

#-------------------------------------------------------------------------------
# Instancializações e inicializações
#-------------------------------------------------------------------------------
global strDir, strArqTst2, pathDir, pathArqTst2

totalFileSize = 0.0
flag_debug    = True #False

#===================================================================================================
# Funções 
#===================================================================================================
#-------------------------------------------------------------------------------
# Função : lê a data e hora do sistema e formata para o padrão brasileiro
# entrada: nada 
# saída  : conf o arg formatoDataHora; ex: '%d/%m/%y %H:%M:%S %a' "17/10/23 Ter 06:27:00"
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
# Função : formata um número com separadores de milhar
# entrada: número a ser formatado
# saída  : número formatado
#-------------------------------------------------------------------------------
def formataNrMilhares(NrRaw):

    # Convertendo o número float para um inteiro
    int_NrRaw = int(NrRaw)
    # Formatando o inteiro com separadores de milhar
    nrFrm = "{:,}".format(int_NrRaw)
    nrFrm.replace(',', '.')

    return nrFrm

#-------------------------------------------------------------------------------
# Função : gera os dados de um arquivo
# entrada: path do arquivo
# saída  : array [nome do arquivo, tamanho do arquivo, data de modificação]
#-------------------------------------------------------------------------------
def generate_file_data(file_path):

    try:
        tryNr      = 1
        file_stats = os.stat(file_path)

        tryNr      = 2
        file_size  = file_stats.st_size

        tryNr      = 3
        try:
            timestamp = file_stats.st_mtime / 1000 
            last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%y %H:%M:%S')
        except:
            print(f"--> Invalid timestamp: {file_stats.st_mtime}")
            last_modified = "25/01/24 00:00:00"

        tryNr     = 4
        #datasFile = [os.path.basename(file_path), file_size, last_modified]
        datasFile = [file_path, file_size, last_modified]
        
        return datasFile

    except OSError as e:

        print(f"--> Skipping file {file_path}, try = {tryNr} due to error: {e}")
        return "25/01/24 00:00:00"

#------------------------------------------------------------------------------------
# Função : gera os dados de um subdiretório
# entrada: path do subdiretório
# saída  : array [nome do subdiretorio, soma do tam de seus arquivos, data de modificação]
#------------------------------------------------------------------------------------
def generate_directory_data(directory_path):

    try:

        directory_size = sum(os.path.getsize(os.path.join(directory_path, file)) 
                             for file in os.listdir(directory_path) 
                                if os.path.isfile(os.path.join(directory_path, file)))
        directory_size_frm = formataNrMilhares(directory_size)
        last_modified      = datetime.datetime.fromtimestamp(os.path.getmtime(directory_path)).strftime('%d/%m/%y %H:%M:%S.%f')[:-3]
        
        #return [os.path.basename(directory_path), directory_size_frm, last_modified]
        return [directory_path, directory_size_frm, last_modified]
    
    except Exception as e:
        print(f"--> Um erro ocorreu: {e}")

#-------------------------------------------------------------------------------
# Função : salva dados lidos
# entrada: dados, path do arquivo
# saída  : nada
#-------------------------------------------------------------------------------
def salvarDados(dados, file_path):

    modo = 'w' if not exists(file_path) else 'a'
    try: 
        with open(file_path, modo, encoding='utf-8') as file: file.write(dados)
        
    except Exception as e: print (f"--> Erro ao salvar arquivo {file_path}: {e}")

#-------------------------------------------------------------------------------
# Função : salva dados em  (pack: import csv)
# entrada: dados, header do csv, path do arquivo
# saída  : nada
#-------------------------------------------------------------------------------
def salvarDados_CSV(data, headerCSV, file_path):

    try:

        with open(file_path, 'w', newline='', encoding='utf-8') as file:

            #--- Instancia o escritor
            #----------------------------
            writer = csv.writer(file)
            #----------------------------

            #--- Header
            writer.writerow(headerCSV)

            #--- Dados
            writer.writerows(data[0:])

    except Exception as e:

        print (f"--> Erro ao salvar arquivo CSV: {e}")

#===================================================================================================
# Função main
#===================================================================================================
def main(pathDir_, pathArqTst): 

    global ScriptName
    ScriptName = os.path.basename(__file__)

    strPathDir = str(pathDir_)
    strArqTst  = str(pathArqTst)

    strPathDirTmp = strPathDir
    if strPathDirTmp.endswith("\\"):
        strPathDirTmp = strPathDirTmp[:-2]
    if strPathDirTmp.endswith("/"):
        strPathDirTmp = strPathDirTmp[:-1]
    if strPathDirTmp.endswith(":"):
        strPathDirTmp = strPathDirTmp[:-1]

    if (flag_debug):
        print (f"*** Script: {ScriptName} ***")
        print (f"--> Sub-diretórios e arquivos de: {strPathDir} ")
        print (f"(Início: {PreparaDataHora('%d/%m/%y %H:%M:%S %a')})")

    directory_path = strPathDir
    
    #--------------------------------------
    # Instancializações e inicializações
    #--------------------------------------
    ararArqFonte    = []
    ararSubdirFonte = []

    totalFileSize   = 0.0
    totalSubdirSize = 0.0

    dataHora        = PreparaDataHora('%y%m%d_%H%M%S')
    nomePathArqTst2 = f'DirArq2_{dataHora}'

    pathArqTst2_txt  = Path(f'{nomePathArqTst2}.txt')
    pathArqTst2_CSV  = Path(f'{nomePathArqTst2}.csv')
    pathArqTst2_xlsx = Path(f'{nomePathArqTst2}.xlsx')

    if (flag_debug):                            
        print(f"--> Arquivos de teste: {pathArqTst2_txt.name}, {pathArqTst2_CSV.name}, {pathArqTst2_xlsx.name}")  

    #--- Headers
    legColsTabela    = ["Nivel", "Path", "qtiDir", "Diretorios", "qtiArq", "Arquivos"]
    legColsTabelaStr = ""
    for (i, col) in enumerate(legColsTabela):
        legColsTabelaStr = legColsTabelaStr + col
        if i < len(legColsTabela) - 1: legColsTabelaStr = legColsTabelaStr + " , "

    #--- Header txt (string)
    if (flag_debug): 
        print (f"> txt: {legColsTabelaStr}")

    #------------------------------------------------
    salvarDados(legColsTabelaStr, pathArqTst2_txt)   
    #------------------------------------------------

    #--- Headers csv (lista; array unitário)
    legColsTabelaStr = ', '.join(legColsTabela)
    if (flag_debug): 
        print (f"> csv: [{legColsTabelaStr}]\n")

    #--- Dados
    nivel       = 0
    dadosTabCSV = []
    path_old    = ""
    for path, dirs, files in os.walk(directory_path):

        newLine = ''
        if (path_old != path):

            path_old = path
            newLine  = '\n'
            nivel   += 1

        #===========================================================================================
        # Dados para o arquivo txt
        #===========================================================================================
        #dadosSalvar = f"{nivel} , {path} , {len(dirs)} , {dirs} , {len(files)} , {files}\n"
        dadosSalvar = f"{newLine}{nivel} , {path} , {len(dirs)} , {dirs} , {len(files)} , {files}\n"
        if (flag_debug): 
            print (f"> txt: {dadosSalvar}")
        #----------------------------------------
        salvarDados(dadosSalvar , pathArqTst2)   
        #----------------------------------------

        #===========================================================================================
        # Dados para o arquivo csv
        #===========================================================================================
        dadosTabCSV.append([nivel,path,len(dirs),dirs,len(files),files])
        if (flag_debug): 
            print (f"> csv: [{nivel},{path},{len(dirs)},{dirs},{len(files)},{files}]\n")

        if nivel > 100: break

    #--- Salva dados csv
    if (flag_debug):
        print (f"--> arquivo CSV: {pathArqTst2_CSV}:\n")
        print (f"Header: {legColsTabelaStr}\n")
        print (f"Dados: {dadosTabCSV}\n")

    #--------------------------------------------------------------
    salvarDados_CSV(dadosTabCSV, legColsTabela, pathArqTst2_CSV)
    #--------------------------------------------------------------

    #--- Lê o arquivo csv
    tabela = pd.read_csv(pathArqTst2_CSV, sep=',', encoding='utf-8')
    print (f"\nTabela read_csv:\n{tabela}")

    """ Exemplo: criando um segundo DataFrame
    data2 = {
        'Produto': ['Livro', 'Caneta', 'Lápis', 'Caderno'],
        'Preço': [15.90, 1.50, 0.50, 4.90]
    }

    df2 = pd.DataFrame(data2)

    # Salvando múltiplos DataFrames em abas separadas
    with pd.ExcelWriter('nome_do_arquivo_multiplo.xlsx') as writer:
        df.to_excel (writer, sheet_name='Pessoas',  index=False)
        df2.to_excel(writer, sheet_name='Produtos', index=False)
    """

    #--- Salvando o DataFrame em um arquivo Excel
    tabela_df = pd.DataFrame(tabela)
    
    try:
        with pd.ExcelWriter(pathArqTst2_xlsx) as writer:
            tabela_df.to_excel(writer, sheet_name=dataHora, index=False)

    except Exception as e:
        print (f"--> Erro ao salvar arquivo {pathArqTst2_xlsx}: {e}")
        
    #-------------------------- 
    # Trata os subdiretórios
    #--------------------------
    QtiddSub = len(ararSubdirFonte)
    print (f"\n--> Diretórios e Subdiretórios em {directory_path}: {QtiddSub}")
    #print (ararSubdirFonte)
    totalSubdirSize = 0
    for subdir in ararSubdirFonte:
        subdirSize       = subdir[1].replace('.', '')
        totalSubdirSize += int(subdirSize)
    totalSubdirSize_frm = formataNrMilhares(totalSubdirSize)
    totalsubdirsize_frm = totalSubdirSize_frm.replace(',', '.')
    ararSubdirFonte.append(["Total", totalsubdirsize_frm, PreparaDataHora("%d/%m/%y %H:%M:%S %a")])

    #--- Salva os dados dos subdiretórios em csv  - # JH 25/01/24
    nomeSubdirCSV   = f"{directory_path}\\dadosSubdirs_{os.path.basename(directory_path)}.csv"
    headerSubdirCSV = ["Subdiretorio", "Tamanho", "Data de Modificação"]
    print (f"--> Salva os dados dos subdiretórios em {nomeSubdirCSV}")
    #------------------------------------------------------------------
    salvarDados_CSV(ararSubdirFonte, headerSubdirCSV, nomeSubdirCSV)
    #-------------------------------------------------------------------
    df_Subdir = pd.read_csv(nomeSubdirCSV, sep=',', encoding='utf-8')
    #-------------------------------------------------------------------
    print (df_Subdir)

    #-------------------------- 
    # Trata os arquivos
    #--------------------------
    QtiddArq = len(ararArqFonte)
    print (f"\n--> Arquivos em {directory_path}: {QtiddArq}")            
    totalFileSize_frm = formataNrMilhares(totalFileSize).replace(',', '.')
    ararArqFonte.append(["Total", totalFileSize_frm, PreparaDataHora("%d/%m/%y %H:%M:%S %a")])
    
    #--- Salva os dados dos arquivos em .csv
    nomeArqCSV   = f"{directory_path}\\dadosArqs_{os.path.basename(directory_path)}.csv"
    headerArqCSV = ["Arquivo", "Tamanho", "Data de Modificação"]
    print (f"--> Salva os dados dos arquivos em {nomeArqCSV}")
    #---------------------------------------------------------
    salvarDados_CSV(ararArqFonte, headerArqCSV, nomeArqCSV)
    #-------------------------------------------------------------
    df_Arq = pd.read_csv(nomeArqCSV, sep=',', encoding='utf-8')
    #-------------------------------------------------------------
    print (df_Arq)

#===================================================================================================
# Main
#===================================================================================================
if __name__ == '__main__':

    strDir  = filedialog.askdirectory(title = "Selecione o diretório a ser processado:").replace('/', '\\')
    print (f" Diretório a ser processado: strDir = '{strDir}'")
    pathDir = Path(strDir)

    strArqTst  = filedialog.askdirectory(title = "Selecione o diretório para salvar os arquivos-resultado:").replace('/', '\\')
    print (f" Diretório para salvar os arquivos-resultado: strArqTst = '{strArqTst}'")
    pathArqTst = Path(strArqTst)

    #---------------------------
    main(pathDir, pathArqTst)                                               #r"C:\Users\JOSEHENRIQ1956\AppData")
    #---------------------------

# Fim do programa

#===================================================================================================
# Fim do arquivo dadosDiretorio_v1_4.py