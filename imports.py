try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
        raise
except:
    print("[ERR] Python: Error importando las librerias de python ")
    raise

# Colores
NEGRO = (0,0,0)
BLANCO = (255,255,255)
AZUL = (0,0,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
AMARILLO = (255,255,0)

#control de velocidad en el cambio de imagenes
control = 10
# Dimensiones pantalla
ANCHO=800
ALTO=600

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

def espejo(imagen):
    imagen=pygame.transform.flip(imagen,180,0)
    return imagen

class Bullet(pygame.sprite.Sprite): #Hereda de la clase sprite
    nivel=None
    def __init__(self, img_name, x,y, direccion): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(img_name).convert_alpha()
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.tipo = "bala"
        self.speed = 1
        self.relative_pos = [x,y]
        self.eliminar=False
        self.bloqueado=False
        self.direccion = direccion

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x = x
    	self.rect.y = y


    def update(self):
        for elemento in self.nivel.plataforma_lista:
            if(checkCollision(self,elemento)):
                self.nivel.elementos_lista.remove(self)
        for en in self.nivel.enemigos_lista:
            if(checkCollision(self,en)):
                self.nivel.elementos_lista.remove(self)
                en.vida-=random.randrange(10,20)

        if(self.relative_pos[0] > ANCHO):
            self.eliminar=True
        if(self.relative_pos[1] > ALTO):
            self.eliminar=True

        if(self.direccion == "derecha"): #derecha
            self.relative_pos[0]+=self.speed
            self.rect.x += self.speed
        if(self.direccion == "izquierda"):#izquierda
            self.relative_pos[0]-=self.speed
            self.rect.x -= self.speed
        if(self.direccion == "arriba"):#arriba
            self.relative_pos[1]-=self.speed
            self.rect.y -= self.speed
        if(self.direccion == "abajo"):#abajo
            self.relative_pos[0]+=self.speed
            self.rect.y += self.speed

class Enemigo(pygame.sprite.Sprite):
    nivel = None
    caminando=[]
    def __init__(self, x,y, rango):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/armorwalk_1.png").convert_alpha(),(50,100))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.rango = rango
        self.vida = 100
        self.direccion="derecha"
        self.control_imagenes=0

    def escalar_sprite(self,sprite):
        sprite=pygame.transform.scale(sprite,(50,100))
        return sprite

class Enemigo1(Enemigo):
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
        self.vida = 150
        for i in range(1,7):
            self.caminando.append(pygame.image.load("data/images/enemy/redwalk_"+str(i)+".png").convert_alpha())
        self.conta=True
        self.relative_pos = x
        self.speed =2
    def update(self):
        if(self.i >= len(self.caminando)-1):
            self.i=0

        if(self.relative_pos > self.rango[1]):
            self.conta=False
        else:
            if(self.relative_pos < self.rango[0]):
                self.conta=True

        if(self.control_imagenes == 0):

            if(self.direccion=="derecha"):
                self.image = self.escalar_sprite(self.caminando[self.i])
                self.i+=1
            else:
                self.image = espejo(self.escalar_sprite(self.caminando[self.i]))
                self.i+=1
            self.control_imagenes+=1
        else:
            if(self.control_imagenes >= control):
                self.control_imagenes = 0
            else:
                self.control_imagenes += 1

        if(self.conta):
            self.direccion="derecha"
            self.rect.x+=self.speed
            self.relative_pos+=self.speed
        else:
            self.direccion="izquierda"
            self.rect.x-=self.speed
            self.relative_pos-=self.speed

class Bullet_en(pygame.sprite.Sprite):
    nivel=None
    i=0
    i2=0
    def __init__(self, x,y, pos_p): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.transform.scale(pygame.image.load("data/images/nave.png").convert_alpha(),(50,50))
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 1
        self.cont = 0
        self.tipo = "bala_en"
        self.moves = []
        self.bloqueado=False

    def go(self,pos):
        p = [[self.rect.x,self.rect.y],pos]
        x0 = p[0][0]
        y0 = p[0][1]
        x1 = p[1][0]
        y1 = p[1][1]
        res = []
        dx = (x1 - x0)
        dy = (y1 - y0)
        if (dy < 0) :
            dy = -1*dy
            stepy = -1
        else :
            stepy = 1
        if (dx < 0) :
            dx = -1*dx
            stepx = -1
        else :
            stepx = 1
        x = x0
        y = y0
        if(dx>dy) :
            p = 2*dy - dx
            incE = 2*dy
            incNE = 2*(dy-dx)
            while (x != x1) :
                x = x + stepx
                if (p < 0) :
                    p = p + incE
                else :
                    y = y + stepy
                    p = p + incNE
                p_new = [x, y]
                res.append(p_new)
        else :
            p = 2*dx - dy
            incE = 2*dx
            incNE = 2*(dx-dy)
            while (y != y1) :
                y = y + stepy
                if (p < 0) :
                    p = p + incE
                else :
                    x = x + stepx
                    p = p + incNE

                p_new = [x, y]
                res.append(p_new)
        self.moves=res
        self.i = 0

    def update(self):
        if(checkCollision(self,jugador)):
            self.nivel.elementos_lista.remove(self)
            jugador.vida-=random.randrange(10,20)

        for elemento in self.nivel.elementos_lista:
            if(checkCollision(self,elemento) and elemento.tipo == "bala"):
                self.nivel.elementos_lista.remove(self)
                self.nivel.elementos_lista.remove(elemento)

        for plat in self.nivel.plataforma_lista:
            if(checkCollision(self,plat)):
                self.nivel.elementos_lista.remove(self)

        if(self.cont == 0):
            if(self.i < len(self.moves)):
                self.rect.x,self.rect.y = self.moves[self.i][0],self.moves[self.i][1]
                self.i += 1
            else:
                self.i=0


class Enemigo2(Enemigo):
    nivel = None
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
        self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/grayfire_6.png").convert_alpha(),(50,100))
        self.conta=True
        self.relative_pos = x


    def update(self):
        if(self.control_imagenes == 0):
            bl = Bullet_en(self.rect.x,self.rect.y, [jugador.rect.x,jugador.rect.y])
            bl.nivel = self.nivel
            bl.image = pygame.transform.scale(pygame.image.load("data/images/nave.png").convert_alpha(),(50,50))
            bl.go((jugador.rect.x,jugador.rect.y))
            self.nivel.elementos_lista.add(bl)
            self.control_imagenes+=1
        else:
            if(self.control_imagenes >= 500):
                self.control_imagenes = 0
            else:
                self.control_imagenes += 1

        if(not jugador.rect.x < self.rect.x):
            self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/grayfire_6.png").convert_alpha(),(50,100))
        else:
            self.image = espejo(pygame.transform.scale(pygame.image.load("data/images/enemy/grayfire_6.png").convert_alpha(),(50,100)))

class Enemigo3(Enemigo):
    nivel = None
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
        self.vida=120
        self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/bluefire_6.png").convert_alpha(),(50,100))
        self.conta=True
        self.relative_pos = x


    def update(self):
        if(self.control_imagenes == 0):
            bl = Bullet_en(self.rect.x,self.rect.y, [jugador.rect.x,jugador.rect.y])
            bl.nivel = self.nivel
            bl.image = pygame.transform.scale(pygame.image.load("data/images/bone.png").convert_alpha(),(50,50))
            bl.go((jugador.rect.x,jugador.rect.y))
            self.nivel.elementos_lista.add(bl)
            self.control_imagenes+=1
        else:
            if(self.control_imagenes >= 200):
                self.control_imagenes = 0
            else:
                self.control_imagenes += 1

        if(not jugador.rect.x < self.rect.x):
            self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/bluefire_6.png").convert_alpha(),(50,100))
        else:
            self.image = espejo(pygame.transform.scale(pygame.image.load("data/images/enemy/bluefire_6.png").convert_alpha(),(50,100)))



class Enemigo4(Enemigo):
    img= []
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
        self.vida = 300
        for i in range(1,7):
            self.img.append(pygame.image.load("data/images/enemy/armorwalk_"+str(i)+".png").convert_alpha())
        self.conta=True
        self.relative_pos = x

    def update(self):
        speed = 4
        if(self.i >= len(self.img)-1):
            self.i=0

        if(self.relative_pos > self.rango[1]):
            self.conta=False
        else:
            if(self.relative_pos < self.rango[0]):
                self.conta=True

        if(self.control_imagenes == 0):

            if(self.direccion=="derecha"):
                self.image = self.escalar_sprite(self.img[self.i])
                self.i+=1
            else:
                self.image = espejo(self.escalar_sprite(self.img[self.i]))
                self.i+=1
            self.control_imagenes+=1
        else:
            if(self.control_imagenes >= control):
                self.control_imagenes = 0
            else:
                self.control_imagenes += 1

        if(self.conta):
            self.direccion="derecha"
            self.rect.x+=speed
            self.relative_pos+=speed
        else:
            self.direccion="izquierda"
            self.rect.x-=speed
            self.relative_pos-=speed

class Boss(Enemigo):
    nivel=None
    camino=[]
    ataque=[]
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
        self.vida = 400
        for i in range(1,7):
            self.camino.append(pygame.image.load("data/images/enemy/predatormaskwalk_"+str(i)+".png").convert_alpha())
        self.ataque.append(pygame.image.load("data/images/enemy/predatormaskattack_1.png"))
        self.conta=True
        self.relative_pos = x
        self.shot=0

    def update(self):
        speed = 4

        if(self.shot == 0):
            bl = Bullet_en(self.rect.x,self.rect.y, [jugador.rect.x,jugador.rect.y])
            bl.nivel = self.nivel
            bl.image = pygame.image.load("data/images/bala_j.png").convert_alpha()
            bl.go((jugador.rect.x,jugador.rect.y))
            self.nivel.elementos_lista.add(bl)
            self.shot+=1
        else:
            if(self.shot >= 100):
                self.shot = 0
            else:
                self.shot += 1

        if(self.i >= len(self.camino)-1):
            self.i=0

        if(self.relative_pos > self.rango[1]):
            self.conta=False
        else:
            if(self.relative_pos < self.rango[0]):
                self.conta=True

        if(self.control_imagenes == 0):

            if(self.direccion=="derecha"):
                self.image = self.escalar_sprite(self.camino[self.i])
                self.i+=1
            else:
                self.image = espejo(self.escalar_sprite(self.camino[self.i]))
                self.i+=1
            self.control_imagenes+=1
        else:
            if(self.control_imagenes >= control):
                self.control_imagenes = 0
            else:
                self.control_imagenes += 1

        if(self.conta):
            self.direccion="derecha"
            self.rect.x+=speed
            self.relative_pos+=speed
        else:
            self.direccion="izquierda"
            self.rect.x-=speed
            self.relative_pos-=speed


class Jugador(pygame.sprite.Sprite):
    # Atributos
    # velocidad del jugador
    vel_x = 0
    vel_y = 0
    # Lista de elementos con los cuales chocar
    nivel = None
    caminando= []
    saltox=[]
    muerte=[]
    hurt=[]
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # creamos el bloque
        ancho = 40
        alto = 60
        for i in range(1,7):
            self.caminando.append(pygame.image.load("data/images/player/Walk"+str(i)+".png"))
        for i in range(1,8):
            self.saltox.append(pygame.image.load("data/images/player/Jump"+str(i)+".png"))
        for i in range(1,9):
            self.muerte.append(pygame.image.load("data/images/player/Dead"+str(i)+".png"))
        for i in range(1,6):
            self.hurt.append(pygame.image.load("data/images/player/Hurt"+str(i)+".png"))
        self.image = pygame.transform.scale(pygame.image.load("data/images/player/Walk1.png").convert_alpha(),(50,100))
        self.ataque = pygame.transform.scale(pygame.image.load("data/images/player/Attack1.png").convert_alpha(),(50,100))
        self.rect = self.image.get_rect()
        self.i=0
        self.conta_salto=0
        self.direccion = "derecha"
        self.direccion_o = "derecha"
        self.vida = 100
        self.bones = 7
        self.conta_hurt=0
        self.pos_hurt = 0
        self.hongo = False
    def escalar_sprite(self,sprite):
        sprite=pygame.transform.scale(sprite,(50,100))
        return sprite

    def update(self):
        for element in self.nivel.elementos_lista:
            if(checkCollision(self,element) and element.tipo == "hongo"):
                self.hongo=True
                self.nivel.elementos_lista.remove(element)

        for enemigo in self.nivel.enemigos_lista:
            if(checkCollision(self,enemigo)):
                self.vida-=random.randrange(2,5)

        if(self.bones <= 0):
            for i in range(1,5):
                self.image = self.escalar_sprite(self.hurt[i])
            if(self.conta_hurt > 500):
                self.bones=7
                self.conta_hurt=0
            else:
                banderita=True
                for plat in self.nivel.plataforma_lista:
                    if(checkCollision(self,plat)):
                        banderita=False
                        jugador.rect.y-=2
                if(banderita):
                    if(jugador.rect.y <= ALTO-100):
                        self.rect.y+=5
                self.conta_hurt+=1
        else:
            self.choque=False
            self.calc_grav()
            if(self.i>len(self.caminando)-1):
                self.i=0
            # Mover izq/der
            if(self.vel_x>0):
                self.direccion="derecha"
                self.direccion_o = "derecha"
                self.image = self.escalar_sprite(self.caminando[self.i])
                self.i+=1
            elif(self.vel_x<0):
                self.direccion="izquierda"
                self.direccion_o = "izquierda"
                self.image = self.escalar_sprite(espejo(self.caminando[self.i]))
                self.i+=1
            self.rect.x += self.vel_x

            bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
            for bloque in bloque_col_list:
                if self.vel_x > 0:
                    self.rect.right = bloque.rect.left
                elif self.vel_x < 0:
                    self.rect.left = bloque.rect.right

            bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, True)
            for bloque in bloque_col_list:
                self.vida-=10
            # Mover arriba/abajo
            self.rect.y += self.vel_y

            # Revisamos si chocamos
            bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
            for bloque in bloque_col_list:
                # Reiniciamos posicion basado en el arriba/bajo del objeto
                if self.vel_y > 0:
                    self.rect.bottom = bloque.rect.top
                elif self.vel_y < 0:
                    self.rect.top = bloque.rect.bottom
                self.vel_y = 0

    def animar_salto(self):
        if(self.conta_salto>3):
            self.conta_salto=3
        if(self.direccion=="derecha"):
            self.image=self.escalar_sprite(self.saltox[self.conta_salto])
            self.conta_salto+=1
        else:
            self.image = self.escalar_sprite(espejo(self.saltox[self.conta_salto]))
            self.conta_salto+=1
    def calc_grav(self):
        if self.vel_y == 0:
            self.vel_y = 1

        else:
            self.vel_y += .35


        # Revisamos si estamos en el suelo
        if self.rect.y >= ALTO - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = ALTO - self.rect.height
        else:
            self.animar_salto()

    def salto(self):
        self.direccion_o = "arriba"
        self.rect.y += 2
        plataforma_col_lista = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
        self.rect.y -= 2
        if len(plataforma_col_lista) > 0 or self.rect.bottom >= ALTO:
            self.vel_y = -12

    def ir_izq(self):
        self.vel_x = -6

    def ir_der(self):
        self.vel_x = 6

    def no_mover(self):
        self.vel_x = 0

class Plataforma(pygame.sprite.Sprite):
    matriz=cargar_fondo("data/images/tiles_spritesheet.png",72,72,True)
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.matriz[0][0]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.saved = (x,y)
        self.tipo = ""
        self.bloqueado=False

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect.x=self.saved[0]
        self.rect.y=self.saved[1]

    def get_from_tipo(self):
        if(self.tipo == "caja"):
            self.image=self.matriz[0][6]
        elif(self.tipo == "caja_x"):
            self.image=self.matriz[0][11]
        elif(self.tipo == "muro_verde"):
            self.image=self.matriz[1][5]
        elif(self.tipo == "caja_adv"):
            self.image=self.matriz[0][2]
        else:
            self.image = self.matriz[0][0]

class Nivel(object):

    # Lista de sprites usada en todos los niveles. Add or remove
    plataforma_lista = None
    enemigos_lista = None
    balas_lista = None
    fondo=pygame.transform.scale(pygame.image.load("data/images/background_1.png"), (3000,600))
    mov_fondo=0

    def __init__(self, jugador):
        self.plataforma_lista = pygame.sprite.Group()
        self.enemigos_lista = pygame.sprite.Group()
        self.elementos_lista = pygame.sprite.Group()
        self.jugador = jugador

    # Actualizamos elementos en el nivel
    def update(self):
        """ Actualiza todo lo que este en este nivel."""
        self.plataforma_lista.update()
        self.enemigos_lista.update()
        self.elementos_lista.update()

    def draw(self, pantalla):
        # Dibujamos fondo
        pantalla.fill(AZUL)

        pantalla.blit(self.fondo, (0,0))
        self.plataforma_lista.draw(pantalla)
        self.enemigos_lista.draw(pantalla)
        self.elementos_lista.draw(pantalla)

    def Mover_fondo(self, mov_x, mov_y):
        self.mov_fondo += mov_x
        for plataforma in self.plataforma_lista:
            plataforma.rect.x += mov_x
        for enemigo in self.enemigos_lista:
            enemigo.rect.x += mov_x

        self.mov_fondo += mov_y
        for plataforma in self.plataforma_lista:
            plataforma.rect.y += mov_y
        for enemigo in self.enemigos_lista:
            enemigo.rect.y += mov_y
        for elemento in self.elementos_lista:
            if(not elemento.bloqueado):
                elemento.rect.y += mov_y


class Nivel_01(Nivel):

    def __init__(self, jugador):
        Nivel.__init__(self, jugador)
        self.limite=-3000
        self.enemigos_lista=pygame.sprite.Group()
        nivel = [
                    [472, 410, "muro_verde"],
                    [540, 320, "muro_verde"],
                    [630, 220, "muro_verde"],
                    [1060, 120, "caja_x"],
                    [1129, 120, "caja_x"],
                    [1198, 120, "caja_x"],
                    [1267, 120, "caja_x"],
                    [1336, 120, "caja_x"],
                    [1120, 300, "caja"],
                    [2000, 200, "caja"],
                    [2150, 300, "caja"],
                    [2300, 400, "caja"],
                    [1500, ALTO-100, "caja"],
                    [1800, ALTO-100, "caja"],

                 ]

        enemigos_config = [
                    [1060,20,1080,1336, "Enemigo1"],
                    [1125,200,1120,1120, "Enemigo2"],
                    [2000,100,2000,2000, "Enemigo2"],
                    [2300,300,2300,2300, "Enemigo3"],
                    [2150,200,2150,2150, "Enemigo3"],
                    [2000,ALTO-100, 2000, 2300, "Enemigo4"]
                ]

        for enemigo in enemigos_config:
            if(enemigo[4] == "Enemigo1"):
                en=Enemigo1(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                self.enemigos_lista.add(en)
            elif(enemigo[4] == "Enemigo2"):
                en=Enemigo2(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                en.nivel = self
                self.enemigos_lista.add(en)
            elif(enemigo[4] == "Enemigo3"):
                en=Enemigo3(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                en.nivel = self
                self.enemigos_lista.add(en)
            if(enemigo[4] == "Enemigo4"):
                en=Enemigo4(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                self.enemigos_lista.add(en)

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.tipo=plataforma[2]
            bloque.get_from_tipo()
            bloque.jugador = self.jugador
            bloque.update_rect()
            self.plataforma_lista.add(bloque)

class Nivel_02(Nivel):

    def __init__(self, jugador):

        # Llamamos al padre
        Nivel.__init__(self, jugador)
        self.limite=-3000
        # Arreglo con ancho, alto, x, y de la plataforma
        nivel = [ [500, 500, "caja_adv"],
                 [200, 400, "caja_adv"],
                 [500, 250, "caja_adv"],
                 [200, 100, "caja_adv"],
                 [500, -50, "caja_adv"],
                 [250, -200, "caja_adv"],
                 [350, -380, "caja_adv"],
                 ]

        elemento = [
                    [360,-415, "hongo"]
                    ]

        boss=[[900,-70, 900, 1200, "Boss"]]

        for enemigo in boss:
            en=Boss(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
            en.nivel = self
            self.enemigos_lista.add(en)

        for element in elemento:
            bloque = Plataforma(element[0], element[1])
            bloque.tipo=element[2]
            bloque.image = pygame.transform.scale(pygame.image.load("data/images/hongo.png").convert_alpha(),(35,35))
            bloque.update_rect()
            self.elementos_lista.add(bloque)
        # Go through the array above and add platforms
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.tipo=plataforma[2]
            bloque.get_from_tipo()
            bloque.jugador = self.jugador
            bloque.update_rect()
            self.plataforma_lista.add(bloque)

def lifebars(surface, pos):
    if(jugador.vida > 75):
        color = VERDE
    elif(jugador.vida > 50):
        color = AMARILLO
    else:
        color = ROJO
    pygame.draw.rect(surface, color, (pos[0],pos[1],jugador.vida,10))


def update_status_section(sub):
    #STATS E INVENTARIO DEL JUGADOR
    tipo = pygame.font.SysFont("monospace", 15)
    tipo.set_bold(True)
    sub.fill((0,0,0))
    blood = tipo.render("Vida actual: " , 1 , (255,0,0))
    sub.blit(blood, [10,5])
    lifebars(sub, [140,8])

    items = tipo.render("Guns: " , 1 , (255,0,0))
    sub.blit(items, [300,5])
    pos1,pos2 = 370, 2
    bone = pygame.transform.scale(pygame.image.load("data/images/bone.png"),(25,25))
    #sub.blit(key, (pos1,pos2))
    for i in range(1, jugador.bones+1):
        sub.blit(bone, (pos1,pos2))
        pos1+=25

def pantalla_game_over():
    ALTO = 600
    ANCHO = 800
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
    pygame.display.set_caption(" Not Yet - Game over ", 'Spine Runtime')
    pantalla.fill((0,0,0))
    font_path = 'data/fonts/Bombing.ttf'
    font = pygame.font.Font
    tipo = pygame.font.Font(font_path, 40)


    img = pygame.image.load("data/images/game_over.png")
    img = pygame.transform.scale(img, (ANCHO, ALTO+30))
    text5 = tipo.render("Presiona ENTER para continuar !", 1 , (255,255,255))

    pantalla.blit(img, (0,0))
    pantalla.blit(text5, (70,ALTO-10))

    pygame.display.flip()
    terminar = False
    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar=True
                salir=True
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar=True
                if event.key == pygame.K_RETURN:
                    terminar=True

def final():
    ALTO = 600
    ANCHO = 800
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
    pygame.display.set_caption(" Not Yet - [History-End] ", 'Spine Runtime')
    pantalla.fill((0,0,0))
    font_path = 'data/fonts/Bombing.ttf'
    font = pygame.font.Font
    tipo = pygame.font.Font(font_path, 40)
    text = tipo.render("Tras derrotar al malvado lider " , 1 , (255,0,0))
    text1 = tipo.render("alien se logro restablecer el", 1 , (255,0,0))
    text2 = tipo.render("balance natural finalmente", 1 , (255,0,0))
    text3 = tipo.render("el alien no tenia cura. El viejo zombie ", 1 , (255,0,0))
    text4 = tipo.render("decidio seguir batallando por ", 1 , (255,0,0))
    text5 = tipo.render("la justicia para siempre.", 1 , (255,0,0))
    img = pygame.image.load("data/images/end.jpg")
    img = pygame.transform.scale(img, (ANCHO, ALTO+30))
    text5 = tipo.render("Presiona ENTER para continuar !", 1 , (255,255,255))
    pantalla.blit(img, (0,0))
    pantalla.blit(text, (10,10))
    pantalla.blit(text1, (10,50))
    pantalla.blit(text2, (10,90))
    pantalla.blit(text3, (10,130))
    pantalla.blit(text4, (10,170))
    pantalla.blit(text4, (10,220))
    pantalla.blit(text5, (70,ALTO-10))
    pygame.display.flip()
    terminar = False
    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar=True
                salir=True
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar=True
                if event.key == pygame.K_RETURN:
                    terminar=True
                    salir=True
                    sys.exit(0)

def prologo():
    ALTO = 600
    ANCHO = 800
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
    pygame.display.set_caption(" Not Yet - [History-Init] ", 'Spine Runtime')
    pantalla.fill((0,0,0))
    font_path = 'data/fonts/Bombing.ttf'
    font = pygame.font.Font
    tipo = pygame.font.Font(font_path, 40)
    text = tipo.render("Un zombie quiere vengar asesinando " , 1 , (255,0,0))
    text1 = tipo.render("al lider alien quien lo volvio", 1 , (255,0,0))
    text2 = tipo.render("de noble guerrero a zombie.finalmente", 1 , (255,0,0))
    text3 = tipo.render("el alien se convirtio en su peor enemigo", 1 , (255,0,0))
    text4 = tipo.render("el zombie no descansara hasta ", 1 , (255,0,0))
    text5 = tipo.render("lograr asesinarlo.", 1 , (255,0,0))
    img = pygame.image.load("data/images/init.jpeg")
    img = pygame.transform.scale(img, (ANCHO, ALTO+30))
    text5 = tipo.render("Presiona ENTER para continuar !", 1 , (255,255,255))
    pantalla.blit(img, (0,0))
    pantalla.blit(text, (10,10))
    pantalla.blit(text1, (10,50))
    pantalla.blit(text2, (10,90))
    pantalla.blit(text3, (10,130))
    pantalla.blit(text4, (10,170))
    pantalla.blit(text4, (10,220))
    pantalla.blit(text5, (70,ALTO-10))
    pygame.display.flip()
    terminar = False
    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar=True
                salir=True
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar=True
                if event.key == pygame.K_RETURN:
                    terminar=True

def game():
    prologo()
    pygame.init()

    # Set the height and width of the screen
    tam = [ANCHO, ALTO+30]
    pantalla = pygame.display.set_mode(tam)
    sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
    sub.fill((0,0,0))
    #tam = pygame.display.list_modes()[0]
    #pantalla = pygame.display.set_mode(tam,pygame.FULLSCREEN)


    pygame.display.set_caption("Not Yet - Game")
    global jugador
    # Creamos jugador
    jugador = Jugador()

    # Creamos los niveles
    nivel_lista = []
    nivel_lista.append( Nivel_01(jugador) )
    nivel_lista.append( Nivel_02(jugador) )

    # Establecemos nivel actual
    nivel_actual_no = 0
    nivel_actual = nivel_lista[nivel_actual_no]

    # Lista de sprites activos
    activos_sp_lista = pygame.sprite.Group()
    # Indicamos a la clase jugador cual es el nivel
    jugador.nivel = nivel_actual

    jugador.rect.x = 340
    jugador.rect.y = ALTO - jugador.rect.height
    activos_sp_lista.add(jugador)

    fin = False

    # Controlamos que tan rapido actualizamos pantalla
    reloj = pygame.time.Clock()
    pausa=False
    flag_segundo=True
    # -------- Ciclo del juego -----------
    while not fin:
        if(len(nivel_lista[1].enemigos_lista) == 0):
            fin=True
            final()
        if(jugador.vida <= 0):
            fin=True
            pantalla_game_over()

        for enemigo in nivel_actual.enemigos_lista:
            if(enemigo.vida <= 0):
                nivel_actual.enemigos_lista.remove(enemigo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fin=True
                if event.key == pygame.K_LEFT:
                    jugador.ir_izq()
                if event.key == pygame.K_RIGHT:
                    jugador.ir_der()
                if event.key == pygame.K_UP:
                    jugador.salto()
                if event.key == pygame.K_p:
                    if(pausa):
                        pausa=False
                    else:
                        pausa=True
                if event.key == pygame.K_SPACE:
                    if(jugador.bones > 0):
                        bl = Bullet("data/images/bone.png",jugador.rect.x,jugador.rect.y+20,jugador.direccion_o)
                        bl.nivel = nivel_actual
                        bl.image = pygame.transform.scale(pygame.image.load("data/images/bone.png").convert_alpha(),(35,35))
                        bl.update_rect(jugador.rect.x,jugador.rect.y+20)
                        nivel_actual.elementos_lista.add(bl)
                        jugador.bones-=1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and jugador.vel_x < 0:
                    jugador.no_mover()
                if event.key == pygame.K_RIGHT and jugador.vel_x > 0:
                    jugador.no_mover()

        #  Si el jugador se aproxima al limite derecho de la pantalla (-x)
        if(nivel_actual_no==0):
            if jugador.rect.x >= 500:
                dif = jugador.rect.x - 500
                jugador.rect.x = 500
                nivel_actual.Mover_fondo(-dif,0)

            # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
            if jugador.rect.x <= 120:
               dif = 120 - jugador.rect.x
               jugador.rect.x = 120
               nivel_actual.Mover_fondo(dif,0)

        if(nivel_actual_no==1 and not jugador.hongo):
            if(flag_segundo):
                font_path = 'data/fonts/coders_crux.ttf'
                font = pygame.font.Font
                tipo = pygame.font.Font(font_path, 80)
                text = tipo.render(" Nivel 2 " , 1 , (255,0,0))
                jugador.rect.x,jugador.rect.y = 500, 400
                flag_segundo=False
                nivel_actual.draw(pantalla)
                pantalla.blit(text, (ANCHO/2-100,ALTO/2))
                pygame.display.flip()
                time.sleep(2)

            if jugador.rect.y <= 100:
                dif = jugador.rect.y - 100
                jugador.rect.y = 100
                nivel_actual.Mover_fondo(0,-dif/2)
            # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
            if jugador.rect.y >= ALTO-100:
                fin=True
                pantalla_game_over()
        else:
            if jugador.rect.x >= 500:
                dif = jugador.rect.x - 500
                jugador.rect.x = 500
                nivel_actual.Mover_fondo(-dif,0)

            # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
            if jugador.rect.x <= 120:
               dif = 120 - jugador.rect.x
               jugador.rect.x = 120
               nivel_actual.Mover_fondo(dif,0)


        #Si llegamos al final del nivel
        pos_actual=jugador.rect.x + nivel_actual.mov_fondo
        if pos_actual < nivel_actual.limite:
           jugador.rect.x=120
           if nivel_actual_no < len(nivel_lista)-1:
              nivel_actual_no += 1
              nivel_actual = nivel_lista[nivel_actual_no]
              jugador.nivel=nivel_actual

        if(not pausa):
            # Dibujamos y refrescamos
            # Actualizamos al jugador.
            activos_sp_lista.update()
            nivel_actual.update()
            #nivel_actual.enemigos_lista.update()
            nivel_actual.enemigos_lista.draw(pantalla)
            nivel_actual.draw(pantalla)
            activos_sp_lista.draw(pantalla)
            update_status_section(sub)
        else:
            font_path = 'data/fonts/coders_crux.ttf'
            font = pygame.font.Font
            tipo = pygame.font.Font(font_path, 80)
            text = tipo.render(" Pausa " , 1 , (255,0,0))
            pantalla.blit(text, (ANCHO/2-100,ALTO/2))
        reloj.tick(60)
        pygame.display.flip()
