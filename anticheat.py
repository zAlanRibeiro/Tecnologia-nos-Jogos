import numpy as np

class AnalisadorIA:
    def __init__(self):
        # CONFIGURAÇÕES DE SENSIBILIDADE
        self.tempo_minimo_humano = 0.40  # 150ms (Menos que isso é reflexo de robô)
        self.variancia_minima = 0.45    # O "jitter" humano. Se for menor que 0.02, é muito constante.

    def verificar_integridade(self, historico_cliques):
        # Precisa de pelo menos 4 cliques para ter uma base de dados
        if len(historico_cliques) < 4:
            return "ANALISANDO PADRÕES...", (255, 255, 255)

        tempos_de_reacao = []
        for i in range(1, len(historico_cliques)):
            dt = historico_cliques[i][2] - historico_cliques[i-1][2]
            tempos_de_reacao.append(dt)

        # MÉTRICAS
        media_tempo = np.mean(tempos_de_reacao)
        desvio_padrao = np.std(tempos_de_reacao)

        print(f"[DEBUG IA] Média: {media_tempo:.4f}s | Desvio: {desvio_padrao:.4f}s")

        # REGRA 1: Velocidade Inumana
        if media_tempo < self.tempo_minimo_humano:
            return "❌ BANIDO: VELOCIDADE INUMANA", (255, 50, 50)

        # REGRA 2: Consistência de Robô (Baixo desvio padrão)
        # Se o robô clica sempre com 0.1s de intervalo, o desvio padrão será quase 0.
        if desvio_padrao < self.variancia_minima:
            return "❌ BANIDO: PADRÃO MECÂNICO (BOT)", (255, 50, 50)

        return "✅ JOGADOR SEGURO", (50, 255, 50)