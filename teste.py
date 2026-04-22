import pyautogui
import time
import os

print("XIT DE MEMÓRIA ATIVADO")

while True:
    try:
        # Tenta achar a janela do jogo na tela
        janela = pyautogui.getWindowsWithTitle("Seminário: IA em Jogos (AntiCheat)")
        
        if janela and os.path.exists("alvo.txt"):
            with open("alvo.txt", "r") as f:
                dados = f.read().split(",")
                if len(dados) == 2:
                    # Posição da bola RELATIVA à janela
                    rel_x = int(dados[0])
                    rel_y = int(dados[1])
                    
                    # Posição REAL na tela (Janela + Relativo)
                    # Somamos 30 no Y por causa da barra de título da janela
                    final_x = janela[0].left + rel_x
                    final_y = janela[0].top + rel_y + 30
                    
                    pyautogui.click(final_x, final_y)
                    open("alvo.txt", "w").close() 
                    
        time.sleep(0.01)
    except Exception as e:
        pass