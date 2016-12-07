try:
    from imports import *
except (KeyboardInterrupt, SystemExit):
    raise
except:
    print("[ERR] File: El archivo imports no se ha podido importar, verifique sus archivos")
    raise


def start():

    if not pygame.display.get_init():
        pygame.display.init()
    if not pygame.font.get_init():
        pygame.font.init()
    global ANCHO,ALTO,pantalla
    ANCHO=800
    ALTO=600
    pantalla = pygame.display.set_mode((ANCHO,ALTO))
    pantalla.fill((51,51,51))
    m =Menu(['Iniciar juego','Controles', 'Salir'], pantalla, (ANCHO/2-150,ALTO/2+100))
    m.tam_font = 68
    m.draw_menu()
    pygame.mixer.init()
    pygame.display.update()

    pygame.mixer.init()
    sound = pygame.mixer.Sound("data/sounds/menu.ogg")
    sound.play()
    sound_play=True
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if(m.cursor >= len(m.lista)-1):
                        m.cursor=0
                    else:
                        m.cursor += 1 #here is the Menu class function
                    pantalla.fill((51,51,51))
                    m.draw_menu()

                if event.key == K_UP:
                    if(m.cursor <= 0):
                        m.cursor=len(m.lista)-1
                    else:
                        m.cursor -= 1 #here is the Menu class function
                    pantalla.fill((51,51,51))
                    m.draw_menu()
                if event.key == K_RETURN:
                    if m.cursor == 2:#here is the Menu class function
                        sys.exit(0)
                    if m.cursor == 0:
                        sound.stop()
                    if m.cursor == 1:
                        print("Menu help")
                pantalla.fill((51,51,51))
                m.draw_menu()

    return 1

if __name__ == "__main__":
    start()
