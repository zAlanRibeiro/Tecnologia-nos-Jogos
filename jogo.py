import pygame
import random
import time
import sys
import os
from anticheat import AnalisadorIA

# Configurações
LARGURA, ALTURA = 800, 600
RAIO_BOLA = 20
COR_FUNDO = (30, 30, 30)
COR_BOLA = (255, 0, 0)
COR_TEXTO = (255, 255, 255)

def iniciar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Seminário: IA em Jogos (AntiCheat)")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Arial", 22)
    fonte_ponto = pygame.font.SysFont("Arial", 32, bold=True)

    ia_seguranca = AnalisadorIA()
    
    # Variáveis de Estado
    bola_pos = [random.randint(50, LARGURA-50), random.randint(50, ALTURA-50)]
    historico_cliques = []
    status_texto = "Aguardando cliques..."
    status_cor = COR_TEXTO
    pontuacao = 0
    rodando = True

    # Cria o arquivo de comunicação para o XIT
    with open("alvo.txt", "w") as f:
        f.write(f"{bola_pos[0]},{bola_pos[1]}")

    print("--- SISTEMA INICIADO ---")

    while rodando:
        tela.fill(COR_FUNDO)
        
        # Desenha a Bolinha
        pygame.draw.circle(tela, COR_BOLA, bola_pos, RAIO_BOLA)
        
        # Interface: Pontuação
        txt_ponto = fonte_ponto.render(f"PONTOS: {pontuacao}", True, (255, 215, 0)) # Dourado
        tela.blit(txt_ponto, (LARGURA - 180, 20))

        # Interface: Status AntiCheat
        img_status = fonte.render(f"Status AntiCheat: {status_texto}", True, status_cor)
        tela.blit(img_status, (20, 20))
        
        # Rodapé Informativo
        rodape = fonte.render("Simulação de IA Comportamental - Detecção de Bots", True, (100, 100, 100))
        tela.blit(rodape, (20, ALTURA - 30))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dist = ((mouse_x - bola_pos[0])**2 + (mouse_y - bola_pos[1])**2)**0.5
                
                if dist <= RAIO_BOLA:
                    pontuacao += 1
                    historico_cliques.append((mouse_x, mouse_y, time.time()))
                    
                    # Atualiza Alvo
                    bola_pos = [random.randint(50, LARGURA-50), random.randint(50, ALTURA-50)]
                    
                    # Escreve a nova posição para o XIT ler
                    with open("alvo.txt", "w") as f:
                        f.write(f"{bola_pos[0]},{bola_pos[1]}")
                    
                    # Analisa Integridade
                    status_texto, status_cor = ia_seguranca.verificar_integridade(historico_cliques)

        pygame.display.flip()
        clock.tick(60)

    # Limpa o arquivo ao fechar
    if os.path.exists("alvo.txt"):
        os.remove("alvo.txt")
    pygame.quit()

if __name__ == "__main__":
    iniciar_jogo()