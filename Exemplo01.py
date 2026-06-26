import os
from pathlib import Path
import ctypes
import sys

# ─────────────────────────────────────────────
# 1. Verificar se está executando como Admin
# ─────────────────────────────────────────────
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("=" * 60)
    print(" ATENÇÃO: Execute este script como ADMINISTRADOR!")
    print(" Clique direito no terminal → Executar como administrador")
    print("=" * 60)
    sys.exit(1)

print("✅ Executando como Administrador\n")

# ─────────────────────────────────────────────
# 2. Função para listar com tratamento de erro
# ─────────────────────────────────────────────
def listar_arquivos(caminho_base: str, recursivo: bool = True):
    """
    Lista arquivos e subpastas de um diretório,
    ignorando graciosamente acessos negados.
    """
    caminho = Path(caminho_base)

    if not caminho.exists():
        print(f"[!] Caminho não existe: {caminho_base}")
        return

    print(f"\n📁 Explorando: {caminho_base}")

    try:
        if recursivo:
            itens = caminho.rglob("*")   # recursivo — todas as subpastas
        else:
            itens = caminho.iterdir()    # apenas nível atual
    except PermissionError:
        print(f"⛔ Acesso negado ao diretório: {caminho_base}")
        return
    except Exception as e:
        print(f"[!] Erro inesperado em {caminho_base}: {e}")
        return

    contagem_arquivos = 0
    contagem_pastas = 0

    for item in itens:
        try:
            if item.is_dir():
                print(f"  📂 [PASTA]  {item}")
                contagem_pastas += 1
            elif item.is_file():
                try:
                    tamanho = item.stat().st_size
                    print(f"  📄 [{tamanho:>10,} bytes] {item}")
                except:
                    print(f"  📄 [--- bytes] {item}")
                contagem_arquivos += 1
        except PermissionError:
            # Subpasta sem permissão — pula silenciosamente
            continue
        except Exception:
            continue

    print(f"\n✅ Total: {contagem_pastas} pastas, {contagem_arquivos} arquivos")

# ─────────────────────────────────────────────
# 3. Função específica para pastas $*
# ─────────────────────────────────────────────
def listar_pastas_sistema():
    """
    Lista todas as pastas do sistema que começam com $
    na raiz C:\ e tenta acessar o conteúdo de cada uma.
    """
    print("\n" + "=" * 60)
    print(" PASTAS DO SISTEMA (prefixo $)")
    print("=" * 60)

    raiz = Path("C:/")

    for item in raiz.iterdir():
        if item.name.startswith("$") and item.is_dir():
            print(f"\n🔍 {item.name} ({item})")
            try:
                for sub in item.iterdir():
                    try:
                        tipo = "[PASTA]" if sub.is_dir() else "[ARQUIVO]"
                        print(f"    {tipo} {sub.name}")
                    except:
                        print(f"    ⚠️  Sem permissão para ler: {sub.name}")
            except PermissionError:
                print(f"    ⛔ Acesso totalmente negado (mesmo como Admin)")

# ═════════════════════════════════════════════
# EXECUÇÃO
# ═════════════════════════════════════════════

# A) Listar conteúdo da raiz C:\
listar_arquivos("C:/", recursivo=False)

# B) Tentar acessar pastas do sistema $*
listar_pastas_sistema()

# C) Exemplo: listar recursivamente uma pasta específica
# (descomente para testar)
# listar_arquivos("C:/Users/SeuUsuario/Documents", recursivo=True)