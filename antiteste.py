import numpy as np
from sklearn.ensemble import IsolationForest

class AnalisadorIA:
    def __init__(self):
        # contamination maior para ser sensível a mudanças rápidas
        self.modelo = IsolationForest(contamination=0.3, random_state=42)

    def verificar_integridade(self, historico_cliques):
        # Pegamos apenas os ÚLTIMOS 10 cliques para a análise não ficar viciada no passado
        janela_recente = historico_cliques[-10:]
        
        if len(janela_recente) < 6:
            return "COLETANDO DADOS...", (255, 255, 255)

        tempos = []
        for i in range(1, len(janela_recente)):
            dt = janela_recente[i][2] - janela_recente[i-1][2]
            tempos.append([dt])

        X = np.array(tempos)

        # Treinamos com a amostra recente
        self.modelo.fit(X)
        pred = self.modelo.predict(X[-1].reshape(1, -1))
        
        media = np.mean(X)
        desvio = np.std(X)
        
        print(f"[IA] Média Recente: {media:.3f} | Desvio Recente: {desvio:.3f}")

        # REGRA DE BANIMENTO INSTANTÂNEO PARA A DEMO:
        # Se os últimos cliques forem rápidos demais OU muito constantes (desvio baixo)
        if (media < 0.45) or (desvio < 0.05):
            return "BANIDO", (255, 50, 50)

        return "SEGURO", (50, 255, 50)