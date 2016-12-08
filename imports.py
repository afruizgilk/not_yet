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
BLANCO=(255, 255, 255)
AZUL=(0,0,255)
ROJO=(255,0,0)
VERDE=(0, 255,0)

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

    def __init__(self, img_name, x,y, direccion): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(img_name).convert_alpha()
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 1
        self.direccion = direccion
    def update(self):

        if(self.direccion == "derecha"): #derecha
            self.rect.x += self.speed
        if(self.direccion == "izquierda"):#izquierda
            self.rect.x -= self.speed
        if(self.direccion == "arriba"):#arriba
            self.rect.y -= self.speed
        if(self.direccion == "abajo"):#abajo
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
        self.direccion="derecha"
        self.control_imagenes=0

    def escalar_sprite(self,sprite):
        sprite=pygame.transform.scale(sprite,(50,100))
        return sprite

class Enemigo1(Enemigo):
    def __init__(self,x,y,rango):
        Enemigo.__init__(self,x,y,rango)
        self.i=0
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
        self.tipo = ""
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
    fondo=pygame.transform.scale(pygame.image.load("data/images/background_1.png"), (3000,600))
    mov_fondo=0

    def __init__(self, jugador):
        self.plataforma_lista = pygame.sprite.Group()
        self.enemigos_lista = pygame.sprite.Group()
        self.jugador = jugador

    # Actualizamos elementos en el nivel
    def update(self):
        """ Actualiza todo lo que este en este nivel."""
        self.plataforma_lista.update()
        self.enemigos_lista.update()

    def draw(self, pantalla):
        """ Dibuja lo que se encuentre en el nivel. """

        # Dibujamos fondo
        pantalla.fill(AZUL)

        pantalla.blit(self.fondo, (0,0))
        self.plataforma_lista.draw(pantalla)
        self.enemigos_lista.draw(pantalla)

    def Mover_fondo(self, mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.plataforma_lista:
            plataforma.rect.x += mov_x
        for enemigo in self.enemigos_lista:
            enemigo.rect.x += mov_x


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
                 ]
        enemigos_config = [
                    [1060,20,1080,1336, "Enemigo1"]
                ]

        for enemigo in enemigos_config:
            if(enemigo[4] == "Enemigo1"):
                en=Enemigo1(enemigo[0],enemigo[1],[enemigo[2],enemigo[3]])
                self.enemigos_lista.add(en)

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.tipo=plataforma[2]
            bloque.get_from_tipo()
            bloque.jugador = self.jugador
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

def game():
    """ Programa principal """
    pygame.init()

    # Set the height and width of the screen
    tam = [ANCHO, ALTO]
    pantalla = pygame.display.set_mode(tam)
    #tam = pygame.display.list_modes()[0]
    #pantalla = pygame.display.set_mode(tam,pygame.FULLSCREEN)


    pygame.display.set_caption("Ejemplo de juego de plataforma")

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
        reloj.tick(60)
        pygame.display.flip()
