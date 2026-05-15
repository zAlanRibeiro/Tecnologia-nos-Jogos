import numpy as np
from sklearn.ensemble import IsolationForest

class AnalisadorIA:
    def __init__(self):
        # Baixa contaminação para focar no que é realmente estranho
        self.modelo = IsolationForest(contamination=0.01, random_state=42)
        self.treinado = False
        self.amostras_treino = []
        self.limite_treino = 15  # Base de aprendizado
        self.media_humana = 0
        self.contador_anomalias = 0

    def verificar_integridade(self, historico_cliques):
        if len(historico_cliques) < 2:
            return "INICIALIZANDO...", (255, 255, 255)

        # Delta time entre o clique atual e o anterior
        dt = historico_cliques[-1][2] - historico_cliques[-2][2]
        
        # --- FASE 1: APRENDIZADO (ESTABELECENDO O PADRÃO) ---
        if not self.treinado:
            self.amostras_treino.append([dt])
            progresso = len(self.amostras_treino)
            
            if progresso >= self.limite_treino:
                X_treino = np.array(self.amostras_treino)
                self.modelo.fit(X_treino)
                self.media_humana = np.mean(X_treino)
                self.treinado = True
                print(f"\n[IA] Padrao Estabelecido! Media: {self.media_humana:.3f}s")
                return "✅ PADRÃO MAPEADO", (50, 255, 50)
            
            return f"APRENDENDO RITMO ({progresso}/{self.limite_treino})", (255, 255, 0)

        # --- FASE 2: VIGILÂNCIA (DETECÇÃO POR DESVIO DE PADRÃO) ---
        X_novo = np.array([[dt]])
        predicao = self.modelo.predict(X_novo)
        
        # Cálculo de variância dos últimos 4 cliques (para pegar a perfeição do bot)
        ultimos_deltas = [historico_cliques[i][2] - historico_cliques[i-1][2] 
                          for i in range(-1, -min(len(historico_cliques), 5), -1)]
        variancia = np.std(ultimos_deltas) if len(ultimos_deltas) > 1 else 1

        print(f"[IA] Atual: {dt:.3f}s | Media Treino: {self.media_humana:.3f}s | Score: {predicao[0]}")

        # CRITÉRIOS DE BANIMENTO:
        # 1. O tempo atual é muito menor que a média aprendida (ex: menos de 50% do tempo humano)
        # 2. OU a IA detectou uma anomalia estatística (Score -1) E o tempo é menor que o treino
        # 3. OU a variância é quase zero (ritmo mecânico)
        
        flag_anomalia = False
        
        if dt < (self.media_humana * 0.5): # Caiu pela metade do tempo do treino
            flag_anomalia = True
        elif predicao[0] == -1 and dt < self.media_humana:
            flag_anomalia = True
        elif variancia < 0.008:
            flag_anomalia = True

        if flag_anomalia:
            self.contador_anomalias += 1
            if self.contador_anomalias >= 3: # Tolerância para 3 "flags" seguidas
                return "BANIDO", (255, 50, 50)
        else:
            # Recuperação gradual de confiança
            if self.contador_anomalias > 0:
                self.contador_anomalias -= 1

        return "✅ SEGURO", (50, 255, 50)