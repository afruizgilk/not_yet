try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
        raise
except:
    print("[ERR] Python: Error importando las librerias de python ")
    raise


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col == True:
        return True
    else:
        return False

def cargar_fondo(archivo, ancho, alto, sin_canal=False):
    if(not sin_canal):
        imagen = pygame.image.load(archivo).convert_alpha()
    else:
        imagen = pygame.image.load(archivo)
    imagen_ancho, imagen_alto = imagen.get_size()
    tabla_fondos = []
    for fondo_x in range(0, imagen_ancho/ancho):
       linea = []
       tabla_fondos.append(linea)
       for fondo_y in range(0, imagen_alto/alto):
            cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos

def playsound(filez):
    pygame.mixer.init()
    pygame.mixer.music.load(filez)
    pygame.mixer.music.play(0,0)

class Menu:
    lista = []
    tam_font = 32
    font_path = 'data/fonts/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    start=(0,0)
    def __init__(self, datos, surface, position):
        self.lista = datos
        self.dest_surface = surface
        self.start = position
        self.color_n = (255,0,0)
        self.color_s = (0,255,0)
        self.cursor = 0
        self.imagem = pygame.image.load("data/images/main.jpg")
        self.imagem = pygame.transform.scale(self.imagem, (800, 600))


    def get_color(self):
        l_colores=[]
        for i in range(len(self.lista)):
            l_colores.append(self.color_n)
        l_colores[self.cursor] = self.color_s
        return l_colores

    def draw_menu(self):
        y=self.start[1]
        self.dest_surface.blit(self.imagem, [0,0])
        l = self.get_color()
        for i in range(len(self.lista)):
            tipo = pygame.font.Font(self.font_path, self.tam_font)
            text = tipo.render(self.lista[i] , 1 , l[i])
            self.dest_surface.blit(text, (self.start[0],y))
            y+=50
        pygame.display.flip()
