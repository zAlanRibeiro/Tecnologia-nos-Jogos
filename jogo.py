import pygame
import random
import time
import sys
import ctypes # Para o Pop-up do Windows
from antiteste import AnalisadorIA

LARGURA, ALTURA = 800, 600
RAIO_BOLA = 20

def mostrar_popup_ban():
    # Cria uma caixa de mensagem do Windows que trava a execução até clicar em OK
    ctypes.windll.user32.MessageBoxW(0, "O sistema Anti-Cheat detectou o uso de auxiliares externos (Bots). Sua conta foi suspensa.", "DETECÇÃO DE TRAPAÇA", 0x10 | 0x0)

def iniciar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Seminário: IA em Jogos (AntiCheat)")
    fonte = pygame.font.SysFont("Arial", 22)
    
    ia_seguranca = AnalisadorIA()
    bola_pos = [random.randint(50, LARGURA-50), random.randint(50, ALTURA-50)]
    historico_cliques = []
    pontuacao = 0
    rodando = True

    while rodando:
        tela.fill((30, 30, 30))
        pygame.draw.circle(tela, (255, 0, 0), bola_pos, RAIO_BOLA)
        
        # Interface
        txt_ponto = fonte.render(f"PONTOS: {pontuacao}", True, (255, 215, 0))
        tela.blit(txt_ponto, (LARGURA - 150, 20))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dist = ((mouse_x - bola_pos[0])**2 + (mouse_y - bola_pos[1])**2)**0.5
                
                if dist <= RAIO_BOLA:
                    pontuacao += 1
                    historico_cliques.append((mouse_x, mouse_y, time.time()))
                    
                    # Gera novo alvo e comunica ao XIT
                    bola_pos = [random.randint(50, LARGURA-50), random.randint(50, ALTURA-50)]
                    with open("alvo.txt", "w") as f:
                        f.write(f"{bola_pos[0]},{bola_pos[1]}")
                    
                    # Verificação da IA
                    status, _ = ia_seguranca.verificar_integridade(historico_cliques)
                    
                    if status == "BANIDO":
                        print("❌ USUÁRIO BANIDO!")
                        mostrar_popup_ban() # Abre o pop-up (isso trava o jogo)
                        pygame.quit() # Fecha o jogo após o OK
                        sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    iniciar_jogo()