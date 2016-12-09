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
        self.image = pygame.transform.scale(pygame.image.load("data/images/enemy/armor__0006_walk_1.png").convert_alpha(),(50,100))
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

    def update(self):
        speed = 2
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
            self.rect.x+=speed
            self.relative_pos+=speed
        else:
            self.direccion="izquierda"
            self.rect.x-=speed
            self.relative_pos-=speed

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
        self.image = pygame.transform.scale(pygame.image.load("data/images/player/Walk1.png").convert_alpha(),(50,100))
        self.ataque = pygame.transform.scale(pygame.image.load("data/images/player/Attack1.png").convert_alpha(),(50,100))
        self.rect = self.image.get_rect()
        self.i=0
        self.conta_salto=0
        self.direccion = "derecha"
        self.direccion_o = "derecha"
        self.vida = 100

    def escalar_sprite(self,sprite):
        sprite=pygame.transform.scale(sprite,(50,100))
        return sprite

    def update(self):
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

    def Mover_fondo(self, mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.plataforma_lista:
            plataforma.rect.x += mov_x
        for enemigo in self.enemigos_lista:
            enemigo.rect.x += mov_x
        """for elemento in self.elementos_lista:
            elemento.rect.x += mov_x"""


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
                    [2300,300,2300,2300, "Enemigo2"],
                    [2150,200,2150,2150, "Enemigo2"]
                ]

        for enemigo in enemigos_config:
            if(enemigo[4] == "Enemigo1"):
                en=Enemigo1(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                self.enemigos_lista.add(en)
            elif(enemigo[4] == "Enemigo2"):
                en=Enemigo2(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                en.nivel = self
                self.enemigos_lista.add(en)

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.tipo=plataforma[2]
            bloque.get_from_tipo()
            bloque.jugador = self.jugador
            bloque.update_rect()
            self.plataforma_lista.add(bloque)

class Nivel_02(Nivel):
    """ Definicion para el nivel 2. """

    def __init__(self, jugador):
        """ Creamos nivel 2. """

        # Llamamos al padre
        Nivel.__init__(self, jugador)
        self.limite=-3000
        # Arreglo con ancho, alto, x, y de la plataforma
        nivel = [ [210, 50, 500, 500],
                 [210, 50, 200, 400],
                 [210, 50, 1000, 520],
                 [210, 50, 1200, 300],
                 ]

        # Go through the array above and add platforms
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.jugador = self.jugador
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

def game():
    """ Programa principal """
    pygame.init()

    # Set the height and width of the screen
    tam = [ANCHO, ALTO+30]
    pantalla = pygame.display.set_mode(tam)
    sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
    sub.fill((0,0,0))
    #tam = pygame.display.list_modes()[0]
    #pantalla = pygame.display.set_mode(tam,pygame.FULLSCREEN)


    pygame.display.set_caption("Ejemplo de juego de plataforma")
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

    # -------- Ciclo del juego -----------
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador.ir_izq()
                if event.key == pygame.K_RIGHT:
                    jugador.ir_der()
                if event.key == pygame.K_UP:
                    jugador.salto()
                if event.key == pygame.K_SPACE:
                    bl = Bullet("data/images/bone.png",jugador.rect.x,jugador.rect.y+20,jugador.direccion_o)
                    bl.nivel = nivel_actual
                    bl.image = pygame.transform.scale(pygame.image.load("data/images/bone.png").convert_alpha(),(35,35))
                    bl.update_rect(jugador.rect.x,jugador.rect.y+20)
                    nivel_actual.elementos_lista.add(bl)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and jugador.vel_x < 0:
                    jugador.no_mover()
                if event.key == pygame.K_RIGHT and jugador.vel_x > 0:
                    jugador.no_mover()

        #  Si el jugador se aproxima al limite derecho de la pantalla (-x)
        if jugador.rect.x >= 500:
            dif = jugador.rect.x - 500
            jugador.rect.x = 500
            nivel_actual.Mover_fondo(-dif)

        # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
        if jugador.rect.x <= 120:
           dif = 120 - jugador.rect.x
           jugador.rect.x = 120
           nivel_actual.Mover_fondo(dif)

        #Si llegamos al final del nivel
        pos_actual=jugador.rect.x + nivel_actual.mov_fondo
        if pos_actual < nivel_actual.limite:
           jugador.rect.x=120
           if nivel_actual_no < len(nivel_lista)-1:
              nivel_actual_no += 1
              nivel_actual = nivel_lista[nivel_actual_no]
              jugador.nivel=nivel_actual

        # Dibujamos y refrescamos
        # Actualizamos al jugador.
        activos_sp_lista.update()
        nivel_actual.update()
        #nivel_actual.enemigos_lista.update()
        nivel_actual.enemigos_lista.draw(pantalla)
        nivel_actual.draw(pantalla)
        activos_sp_lista.draw(pantalla)
        update_status_section(sub)
        reloj.tick(60)
        pygame.display.flip()
