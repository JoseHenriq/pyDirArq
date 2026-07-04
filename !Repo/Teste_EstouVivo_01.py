import sys
import time
import threading

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
        i     = 0
        while self._ativo:
            elapsed = time.time() - self._inicio
            sys.stdout.write(f'\r⏳ Processando... {chr(chars[i % 4])}  [{elapsed:.0f}s]')
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
            sys.stdout.write(f'\r⏳ Processando{pontos:<6} [{elapsed:.0f}s]')
            sys.stdout.flush()
            time.sleep(0.4)
            i += 1
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()

    def iniciar(self, mensagem='Processando'):
        """Ativa o indicador. Retorna o próprio objeto para uso com 'with'."""
        self._inicio = time.time()
        self._ativo = True
        metodo = self._spinner if self.estilo == 'spinner' else self._pontos
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
        print(f'⏹️  Estou vivo DESATIVADO — {elapsed:.1f}s decorridos')

    # Suporte ao gerenciador de contexto (with)
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.parar()

# ============================================================================
# TESTE 1 — Spinner (padrão)
# ============================================================================
print('\n' + '=' * 50)
print('TESTE 1 — Spinner giratório')
print('=' * 50)

with EstouVivo(estilo='spinner').iniciar('Simulando download de 50 itens'):
    for i in range(50):
        time.sleep(0.1)  # simula trabalho

print('✅ Teste 1 concluído!\n')

# ============================================================================
# TESTE 2 — Pontos progressivos
# ============================================================================
print('=' * 50)
print('TESTE 2 — Pontos progressivos')
print('=' * 50)

with EstouVivo(estilo='pontos').iniciar('Extraindo e processando imagens'):
    for i in range(30):
        time.sleep(0.2)  # simula trabalho

print('✅ Teste 2 concluído!\n')

# ============================================================================
# TESTE 3 — Uso manual (iniciar / parar)
# ============================================================================
print('=' * 50)
print('TESTE 3 — Uso manual')
print('=' * 50)

vivo = EstouVivo(estilo='spinner')
vivo.iniciar('Gerando relatório')

total = 0
for i in range(20):
    time.sleep(0.15)
    total += i

vivo.parar()
print(f'✅ Teste 3 concluído! Soma calculada: {total}\n')

# ============================================================================
# TESTE 4 — Simulando um loop real do Resumo003
# ============================================================================
print('=' * 50)
print('TESTE 4 — Simulação de download + análise')
print('=' * 50)

with EstouVivo(estilo='pontos').iniciar('Baixando página e extraindo conteúdo'):
    # Simula: requests.get, BeautifulSoup, download de imagens
    time.sleep(2)   # download da página
    time.sleep(1.5) # parsing
    time.sleep(3)   # download de 10 imagens (0.3s cada)

print('✅ Relatório salvo em analise.md\n')
print('🎯 Todos os testes finalizados com sucesso!')