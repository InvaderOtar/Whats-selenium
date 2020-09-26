import os
import pygame                  #importamos la paqueteria PYGAME  (SIRVE PARA DESPLEGAR LA INTERFAZ GRAFICA)
from pygame.locals import *    #### NO LO SE 
import RPi.GPIO as GPIO        # IMPORTAMOS RPI.GPIO Y SE LE ASIGNA EL NOMBRE GPIO  (SIRVE PARA INTERACTUAR CON LOS PUERTOS DE LA RASPBERRY PI)
import sys                     #### IMPORTAMOS SYS SIRVE PAR AMANDAR A LLAMAR (SINTETIZADOR DE VOZ) 
import subprocess              #### IMPORTAMOS SYS SIRVE PAR AMANDAR A LLAMAR (SINTETIZADOR DE VOZ) 
import time 
import serial
import MySQLdb

GPIO.setmode(GPIO.BCM)        # NUMERACION QUE SE LE ASIGNA A LOS PINES DE LA RASPBERRY PI (BCM), SE PUEDE USAR LA OPCION GPIO.BOARD
GPIO.setwarnings(False)       # EVITA DIALOGOS DE "ADVERTENCIA EN GPIO"
GPIO.setup(21, GPIO.IN,GPIO.PUD_DOWN) # SE CONFIGURA EL GPIO 21 (BCM) "Pin 36"COMO ENTRADA Y CON UNA RESISTENCIA PULLDOWNS
SCREEN_WIDTH = 1280   #CREAMOS UNA CONSTATE QUE DARA EL ANCHO DE NUESTRA VENTANA 
SCREEN_HEIGHT = 720   #CREAMOS UNA CONSTATE QUE DARA EL ALTO DE NUESTRA VENTANA
global Prediccion1
global Prediccion2
global Prediccion3
Prediccion1=" "
Prediccion2=" "
Prediccion3=" "

#############################################################################################################################
#############################################################################################################################
###########################################                        ###########################################################
###########################################      PREDICTOR         #############################################################
###########################################                        ##################################################################################
###########################################                        ###########################################################
#############################################################################################################################
#############################################################################################################################
        
class DataBase:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='holabb',
            db='Diccionario'
            
            )
        self.cursor = self.connection.cursor()
        print("Conexion establecida" + "\n")
        

    def Busqueda(self,Dato):
        global Prediccion
        global vista
        global PalabrasEncontradas
        print ("DATO A EVALUAR=",Dato)
        if Dato !=[]:
            print ("Dentro de if")
            print("inicio de busqueda")
            sql="SELECT Palabras,Contador from 1000Palabras WHERE Palabras like "
            Datoingresado= "'"+Dato+"%'"
            ORDEN="ORDER BY Contador DESC LIMIT 0,3"
            try:
                self.cursor.execute(sql+Datoingresado+ORDEN)
                vista = self.cursor.fetchall()
                print("Se termino la busqueda")
                ResultadoBusqueda=len(vista)
                PalabrasEncontradas=int(ResultadoBusqueda)
                print("Número de Palabras Encontradas= ",PalabrasEncontradas)
                for columna in vista :
                    Prediccion=columna[0]
                    print("Palabra:",columna[0])
                    print("Contador:",columna[1])
                    print("_____________\n")
        
            except Exception as e:
                raise
        else:
            PalabrasEncontradas = 0
            print ("Fuera de if")
        

    def CerrarBD(self):
        self.connection.close()              

    def PrediccionPalabra(self):
        global Prediccion1
        global Prediccion2
        global Prediccion3
        global frase
        global PalabrasEncontradas
        global UltimaFraseIngresada
        database = DataBase()
        dato=UltimaFraseIngresada
        database.Busqueda(dato)
        database.CerrarBD()
        
        if PalabrasEncontradas == 0:
            Tupla1=("-")
            Tupla2=("-")
            Tupla3=("-")
            
        elif PalabrasEncontradas == 1:
            Tupla1=vista[0]
            Tupla2=("-")
            Tupla3=("-")
            
        elif PalabrasEncontradas == 2:
            Tupla1=vista[0]
            Tupla2=vista[1]
            Tupla3=("-")
            
        elif PalabrasEncontradas == 3:
            Tupla1=vista[0]
            Tupla2=vista[1]
            Tupla3=vista[2]
            
        else:
            Tupla1=("-")
            Tupla2=("-")
            Tupla3=("-")

 
        Prediccion1=Tupla1[0]
        Prediccion2=Tupla2[0]
        Prediccion3=Tupla3[0]

        print(Prediccion1,Prediccion2,Prediccion3)
        
    def BusquedaParaActualizacion(self,Dato):
        global ExistePalabra
        global Palabra_Busqueda
        global Contador_Busqueda
        ExistePalabra=""

        sql="SELECT ID,Palabras,Contador from 1000Palabras WHERE Palabras like "
        try:
            self.cursor.execute(sql+"'"+Dato+"'")
            
            Busqueda_del_elemento = self.cursor.fetchall()
           
            for Palabras_frase in Busqueda_del_elemento :
                ExistePalabra="Si"
                Palabra_Busqueda=Palabras_frase[1]
                Contador_Busqueda=Palabras_frase[2]
                int(Contador_Busqueda)
                print("Palabra:",Palabras_frase[1])
                print("Contador:",Palabras_frase[2])
                print("¿La palabra existe?=",ExistePalabra)
            
                
            if ExistePalabra != "Si":
                print("Posicion de la palabra que no existe")
                ExistePalabra="No"
                print("¿La palabra existe?=",ExistePalabra)
            else:
                None
        except Exception as e:           
            raise

            
    def Actualizar(self):
        global Palabra_Busqueda
        global Contador_Busqueda
        Contador_Busqueda=Contador_Busqueda+1
        Contador_Busqueda=str(Contador_Busqueda)
        sql1="UPDATE 1000Palabras SET Contador="+"'"+Contador_Busqueda+"' "
        sql2="WHERE Palabras ="+"'"+ Palabra_Busqueda +"'"
        sql=sql1+sql2
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise
             
    def AgregarNuevaPalabra(self,palabras):
        sql1="INSERT INTO 1000Palabras (Palabras,Contador)"
        sql2="VALUES ('"+palabras+"',1);" 
        sql=sql1+sql2
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("Se añadio al diccionario la palabra",palabras)
        except Exception as e:
            raise          
   
    def ActualizacionDatos(self):
        global frase
        database = DataBase()
        pre=frase
        DivisionPorPalabra=pre.split()
        for Palabras_De_Frase in DivisionPorPalabra :
            print("Division de palabra:",Palabras_De_Frase)
            database.BusquedaParaActualizacion(Palabras_De_Frase)
            if ExistePalabra=="Si":
               print(Palabra_Busqueda)
               print("Contador +1")
               database.Actualizar()
               print("Número de palabra procesada",DivisionPorPalabra)
            else:
               print("Se agrega palabra al diccionario") 
               database.AgregarNuevaPalabra(Palabras_De_Frase) 
            print("_____________\n")
        database.CerrarBD()

#############################################################################################################################
#############################################################################################################################
##################################################################################################################################################################################################################################
#############################################################################################################################



def main():
#######################################################################   Colores    ######################################################################################################   
    def Color():
        global ColorDeFondo
        
        if ColorDeFondo == "Azul":
           ColorDeFondo = Azul
           
        elif ColorDeFondo == "Rosa":
             ColorDeFondo = Rosa
             
        elif ColorDeFondo == "Blanco":
             ColorDeFondo = Blanco
             
        elif ColorDeFondo == "Cafe":
             ColorDeFondo = Cafe
             
        elif ColorDeFondo == "Verde":
             ColorDeFondo = Verde
        else:
            None
                        
    Cafe=[121,85,72]
    Blanco=[240,240,240]
    Rosa=[250,168,208]
    Verde=[46,204,113]
    Azul=[0,191,255]  
    Negro=[0,0,0]
    rojo=[255,0,0]
    lima=[0,255,0]
    amarillo=[255,255,0]
    cian=[0,255,255]
    magenta=[255,0,255]
    naranja=[255,215,0]
    morado=[147,112,219]
    beige=[255,228,181]  
##########################################################################  Plantilla de carga   #############################################################################    
    pygame.init()                                                                    #INICIA TODOS LOS MODULOS DE PYGAME
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))                  #SE CREA UNA VARIABLE LLAMADA SCREEN A LA CUAL SE LE CARGARA LA INSTRUCCION DE CREAR LA PNATALLA DE 720P
    pygame.display.set_caption("Sistema Aumentativo y Alternativo de Comunicación")  #SE INSSERTA EL TITULO EN LA VENTANA QUE SE CREO ANTEIRORMENTE
    screen.fill(Negro)
    fuente = pygame.font.Font(None, 250)                             
    mensaje = fuente.render("Cargando...", 1, (Blanco))                         
    screen.blit(mensaje, (220, 300))              
    pygame.display.flip()
##########################   IMAGENES PARA INTERFAZ PICTOGRAFICA  ##########################################################################################################  
    Ubicacion="/home/pi/Documents/SistemaAumentativo/"
    Bebidas=pygame.image.load(Ubicacion+"Bebidas.png")
    Brazo=pygame.image.load(Ubicacion+"Brazo.png")
    Cabeza1=pygame.image.load(Ubicacion+"Cabeza1.png")
    Cabeza2Com=pygame.image.load(Ubicacion+"Cabeza2Comezon.png")
    Cabeza2Dol=pygame.image.load(Ubicacion+"Cabeza2Dolor.png")
    Cabeza2Lim=pygame.image.load(Ubicacion+"Cabeza2Limpieza.png")
    Configuraciones=pygame.image.load(Ubicacion+"Conf.png")
    ConfSintetizador=pygame.image.load(Ubicacion+"ConfSin.png") 
    ConfSinTono=pygame.image.load(Ubicacion+"ConfSinTono.png")
    ConfSinIdioma=pygame.image.load(Ubicacion+"ConfSinIdioma.png")
    ConfSinTipo=pygame.image.load(Ubicacion+"ConfSinTipo.png")
    ConfRestaurar=pygame.image.load(Ubicacion+"ConfiguracionRestaurar.png") 
    ConfCursor=pygame.image.load(Ubicacion+"ConfCur.png")
    ConfCurSonido=pygame.image.load(Ubicacion+"ConfCurSon.png")   
    ConfColor=pygame.image.load(Ubicacion+"ConfiguracionColor.png")
    ConfVelocidad=pygame.image.load(Ubicacion+"ConfSinVel.png")
    CurPrinCuadroPequeño=pygame.image.load(Ubicacion+"CursorPrincial.png").convert_alpha()
    CurSecCuadroPequeño=pygame.image.load(Ubicacion+"CursorSecundario.png").convert_alpha()      
    DedosManos=pygame.image.load(Ubicacion+"DedosManos.png")
    DedosPies=pygame.image.load(Ubicacion+"DedosPies.png")
    Direccion=pygame.image.load(Ubicacion+"Direccion.png")
    Familia1=pygame.image.load(Ubicacion+"Familia1.png")
    Familia2=pygame.image.load(Ubicacion+"Familia2.png")
    Familia3=pygame.image.load(Ubicacion+"Familia3.png")
    Higiene1=pygame.image.load(Ubicacion+"Higiene1.png")
    Higiene2=pygame.image.load(Ubicacion+"Higiene2.png")
    Higiene3=pygame.image.load(Ubicacion+"Higiene3.png")
    Intensidad=pygame.image.load(Ubicacion+"Intensidad.png")
    Malestar1=pygame.image.load(Ubicacion+"Malestar1.png")
    Malestar2=pygame.image.load(Ubicacion+"Malestar2.png")
    Malestar3=pygame.image.load(Ubicacion+"Malestar3.png")
    PartesdelCuerpo=pygame.image.load(Ubicacion+"PartesdelCuerpo.png")
    Personal=pygame.image.load(Ubicacion+"Personal.png")
    Peticiones1=pygame.image.load(Ubicacion+"Peticiones1.png")
    Peticiones2=pygame.image.load(Ubicacion+"Peticiones2.png")
    Peticiones3=pygame.image.load(Ubicacion+"Peticiones3.png")
    Peticiones4=pygame.image.load(Ubicacion+"Peticiones4.png")
    Piernas=pygame.image.load(Ubicacion+"Piernas.png")
    Posicion1=pygame.image.load(Ubicacion+"Posicion1.png")
    Posicion2=pygame.image.load(Ubicacion+"Posicion2.png")
    Preguntas1=pygame.image.load(Ubicacion+"Preguntas1.png")
    Preguntas2=pygame.image.load(Ubicacion+"Preguntas2.png")
    Sentimientos1=pygame.image.load(Ubicacion+"Sentimientos1.png")
    Sentimientos2=pygame.image.load(Ubicacion+"Sentimientos2.png")
    Sujeto=pygame.image.load(Ubicacion+"Sujeto.png")
    Temperatura=pygame.image.load(Ubicacion+"Temperatura.png")
    Torso1=pygame.image.load(Ubicacion+"Torso1.png")
    Torso2=pygame.image.load(Ubicacion+"Torso2.png")
    Volumen=pygame.image.load(Ubicacion+"Volumen.png")
    Yo=pygame.image.load(Ubicacion+"Yo.png")
    PictoRegreso=pygame.image.load(Ubicacion+"PictoRegreso.png")
    Alimentos=pygame.image.load(Ubicacion+"Alimentos.png")
    Carne=pygame.image.load(Ubicacion+"Carnes.png")
    Cena1=pygame.image.load(Ubicacion+"Cena1.png")
    Cena2=pygame.image.load(Ubicacion+"Cena2.png")
    Comida1=pygame.image.load(Ubicacion+"Comida1.png")
    Comida2=pygame.image.load(Ubicacion+"Comida2.png")
    ComidaRapida=pygame.image.load(Ubicacion+"ComRapida.png")
    Desayuno1=pygame.image.load(Ubicacion+"Desayuno1.png")
    Desayuno2=pygame.image.load(Ubicacion+"Desayuno2.png")
    Fruta1=pygame.image.load(Ubicacion+"Fruta1.png")
    Fruta2=pygame.image.load(Ubicacion+"Fruta2.png")
    Lacteos1=pygame.image.load(Ubicacion+"Lacteos1.png")
    Lacteos2=pygame.image.load(Ubicacion+"Lacteos2.png")
    Lugares=pygame.image.load(Ubicacion+"Lugares.png")
    LugaresCasa=pygame.image.load(Ubicacion+"LugaresCasa.png")
    LugaresEntretenimiento1=pygame.image.load(Ubicacion+"Entretenimiento1.png")
    LugaresEntretenimiento2=pygame.image.load(Ubicacion+"Entretenimiento2.png")
    Postre=pygame.image.load(Ubicacion+"Postre.png")
    PrincipalCasa=pygame.image.load(Ubicacion+"plantillacasa1.png")
    PrincipalCasa2=pygame.image.load(Ubicacion+"plantillacasa2.png")    
    Saludos=pygame.image.load(Ubicacion+"Saludos.png")
    Snack=pygame.image.load(Ubicacion+"Snack.png")
    Varios=pygame.image.load(Ubicacion+"Varios.png")
    Verdura1=pygame.image.load(Ubicacion+"Verduras1.png")
    Verdura2=pygame.image.load(Ubicacion+"Verduras2.png") 
######################################### Imagenes para Repeticion de frase #############################################################################
    RepetirFrases=pygame.image.load(Ubicacion+"RepFrase.png").convert_alpha()
    CuaRepetirFrase=pygame.image.load(Ubicacion+"RepFraCua.png").convert_alpha()
    CuaRepetirFraseInicio=pygame.image.load(Ubicacion+"CursorRepInicio.png").convert_alpha()
######################################### Imagenes para Alfabetico #############################################################################
    Numeros=pygame.image.load(Ubicacion+"Numeros.png").convert_alpha()
    CuaLetra=pygame.image.load(Ubicacion+"CuaLetABC.png").convert_alpha()
    CuaNumero=pygame.image.load(Ubicacion+"CuaNumABC.png").convert_alpha()
    CuaFilaNumeros=pygame.image.load(Ubicacion+"CuaFi1NumABC.png").convert_alpha()
    CuaFila1=pygame.image.load(Ubicacion+"CuaFi1ABC.png")
    CuaFila2=pygame.image.load(Ubicacion+"CuaFi2ABC.png").convert_alpha()
    CuaRegresar=pygame.image.load(Ubicacion+"CuaRegABC.png").convert_alpha()
    CuaEspacio=pygame.image.load(Ubicacion+"CuaEspABC.png").convert_alpha()
    CuaBorrar=pygame.image.load(Ubicacion+"CuaBorABC.png").convert_alpha()
    CuaNuevaFrase=pygame.image.load(Ubicacion+"CuaNuefraABC.png").convert_alpha()
    CuaVoz=pygame.image.load(Ubicacion+"CuaVozABC.png").convert_alpha()
    CuaInicio=pygame.image.load(Ubicacion+"CuaIniABC.png").convert_alpha()
##################################   IMAGENES PARA INTERFAZ GRAFICA  ############################################################################################################
    SeleccionPictografica=pygame.image.load(Ubicacion+"SelecciondeInterfazPictografica.png").convert_alpha()
    SeleccionInterfaz=pygame.image.load(Ubicacion+"SelInt.png").convert_alpha()
    CuaAlfa=pygame.image.load(Ubicacion+"CuaSelInt.png").convert_alpha()    
    Abecedario=pygame.image.load(Ubicacion+"ABC.png").convert_alpha() 
    CuaPredictor=pygame.image.load(Ubicacion+"CuaPreABC.png").convert_alpha()
####################################################################################  Carga archivo de sonido ##############################################################################################
    pygame.mixer.music.load(Ubicacion+"s-click.wav")
############################################################################### Métodos Parametros de Configuracion ###################################################################################
    def InformacionSintetizador():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 115)
           Negrita = pygame.font.Font(None, 52)
           Fuente = pygame.font.Font(None, 52)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Opciones de Sintetizador", 1, (Negro))
           PrimerParametro = Negrita.render("Tono: Modifica la el tono (masculino o femenino) de voz del sintetizador." ,1, (Negro))
           TercerParametro = Negrita.render("Idioma: Modifica el acento del sintetizador (solo funciona en modo alfabé",1, (Negro))
           TercerParametroB = Fuente.render("tico).",1, (Negro))
           CuartoParametro = Negrita.render("Tipo de voz: Modifica el sonido de voz del sintetizador (agudo o grave).",1, (Negro))
           CuartoParametroB = Fuente.render("o grave).",1, (Negro))
           QuintoParametro = Negrita.render("Restaurar: Se restablecen los valores predeterminados del sintetizador",1, (Negro))
           QuintoParametroB = Fuente.render("de voz.",1, (Negro))     
           screen.blit(TituloInformacion, (110, 15)) 
           screen.blit(PrimerParametro, (20, 220))
           screen.blit(TercerParametro, (20, 290))
           screen.blit(TercerParametroB, (25, 330))
           screen.blit(CuartoParametro, (20, 400))
           screen.blit(QuintoParametro, (20, 470))
           screen.blit(QuintoParametroB, (20, 510))
           pygame.display.flip()

        
    def InformacionSintetizadorTono():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 160)
           Negrita = pygame.font.Font(None, 80)
           Fuente = pygame.font.Font(None, 80)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Tono", 1, (Negro))
           PrimerParametro = Negrita.render("Masculino: El sintetizador emulará un tono de" ,1, (Negro))
           PrimerParametroB = Fuente.render("voz masculino.",1, (Negro))          
           CuartoParametro = Negrita.render("Femenino: El sintetizador emulará un tono de",1, (Negro))
           CuartoParametroB = Fuente.render("voz femenino.",1, (Negro))      
           screen.blit(TituloInformacion, (550, 15))
           screen.blit(PrimerParametro, (20, 190))
           screen.blit(PrimerParametroB, (20, 250))           
           screen.blit(CuartoParametro, (20, 380))
           screen.blit(CuartoParametroB, (20, 440))
           pygame.display.flip()


    def InformacionSintetizadorIdioma():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 160)
           Negrita = pygame.font.Font(None, 72)
           Fuente = pygame.font.Font(None, 72)
           Nota =  pygame.font.Font(None, 50)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Idioma", 1, (Negro))
           PrimerParametro = Negrita.render("Español: El sintetizador toma un acento español," ,1, (Negro))
           PrimerParametroB = Fuente.render("para procesar oraciones en ese idioma.",1, (Negro))                
           SegundoParametro = Negrita.render("Inglés: El sintetizador toma un acento inglés,",1, (Negro))
           SegundoParametroB = Fuente.render("para procesar oraciones en ese idioma.",1, (Negro))
           Nota = Nota.render("Nota: El idioma inglés solo esta habilitado para la interfaz alfabética.",1, (Negro))
           screen.blit(TituloInformacion, (520, 15))
           screen.blit(PrimerParametro, (20, 190))
           screen.blit(PrimerParametroB, (20, 250))           
           screen.blit(SegundoParametro, (20, 350))
           screen.blit(SegundoParametroB, (20, 410))
           screen.blit(Nota, (60, 510))
           pygame.display.flip()


    def InformacionSintetizadorTipodevoz():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 160)
           Negrita = pygame.font.Font(None, 73)
           Fuente = pygame.font.Font(None, 73)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Tipo de voz", 1, (Negro))
           PrimerParametro = Negrita.render("Masculino 1-2: Modifica el tono de voz (Masculino)." ,1, (Negro))         
           CuartoParametro = Negrita.render("Femenino 1-2: Modifica el tono de voz (Femenino).",1, (Negro))      
           screen.blit(TituloInformacion, (300, 15))
           screen.blit(PrimerParametro, (20, 250))           
           screen.blit(CuartoParametro, (20, 400))
           pygame.display.flip()


    def InformacionSintetizadorRestauraciondesintetizador():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 122)
           Negrita = pygame.font.Font(None, 73)
           Fuente = pygame.font.Font(None, 73)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Restauración de Sintetizador", 1, (Negro))
           PrimerParametro = Negrita.render("Si: Se reinician los parámetros del sintetizador" ,1, (Negro))         
           PrimerParametroB = Negrita.render("de voz (Tono, Velocidad, Idioma y Tipo de voz)." ,1, (Negro)) 
           CuartoParametro = Negrita.render("No: No reinicia ningún parámetro.",1, (Negro))      
           screen.blit(TituloInformacion, (20, 15))
           screen.blit(PrimerParametro, (20, 250))
           screen.blit(PrimerParametroB, (20, 310))           
           screen.blit(CuartoParametro, (20, 425))
           pygame.display.flip()

#    def InformacionSelecciondeInterfazPictografica():
#           ConfiguracionColor("Restaurar")
#           TituloFuente = pygame.font.Font(None, 122)
#           Negrita = pygame.font.Font(None, 65)
#           Fuente = pygame.font.Font(None, 73)
#           screen.fill(Azul)
#           screen.blit(PictoRegreso, (0, 0))
#           screen.blit(CuadritoPeque, (0, 0)) 
#           TituloInformacion = TituloFuente.render("Interfaz Pictográfica", 1, (Negro))
#           PrimerParametro = Negrita.render("Casa: Habilita las plantillas (Lugares, Alimento y Saludos)" ,1, (Negro))
#           PrimerParametroB = Negrita.render("y deshabilita la plantilla (Personal)." ,1, (Negro)) 
#           CuartoParametro = Negrita.render("Hospital: Habilita la plantilla (Personal) y deshabilita las",1,(Negro)) 
#           CuartoParametroB = Negrita.render("plantillas (Lugares, Alimento y Saludos).",1,(Negro)) 
#           screen.blit(TituloInformacion, (250, 15))
#           screen.blit(PrimerParametro, (20, 220))
#           screen.blit(PrimerParametroB, (20, 280))           
#           screen.blit(CuartoParametro, (20, 390))
#           screen.blit(CuartoParametroB, (20, 450))
#           pygame.display.flip()
#           pygame.time.delay(VelocidadCursor)

    def InformacionCursorVelocidad():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 115)
           Negrita = pygame.font.Font(None, 62)
           Fuente = pygame.font.Font(None, 62)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Velocidad", 1, (Negro))
           PrimerParametro = Negrita.render("Aumentar: El cursor se desplazará más rápido.(Recomendado" ,1, (Negro))
           PrimerParametroB = Fuente.render("para usuarios experimentados).",1, (Negro))
           TercerParametro = Negrita.render("Disminuir: El cursor se desplazára más lento.(Recomendado",1, (Negro))
           TercerParametroB = Negrita.render("para usuarios que no pueden seleccionar el pictograma o le",1, (Negro))
           TercerParametroC = Negrita.render("tra deseado debido al desplazamiento del cursor.",1, (Negro))
           screen.blit(TituloInformacion, (450, 15))
           screen.blit(PrimerParametro, (20, 205))
           screen.blit(PrimerParametroB, (20, 255))    
           screen.blit(TercerParametro, (20, 360))  
           screen.blit(TercerParametroB, (20, 410))
           screen.blit(TercerParametroC, (20, 460))
           pygame.display.flip()


    def InformacionCursorSonido():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 122)
           Negrita = pygame.font.Font(None, 70)
           Fuente = pygame.font.Font(None, 70)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Sonido", 1, (Negro))
           PrimerParametro = Negrita.render("Habilitar: Se reproduce un sonido de un 'Click' cada" ,1, (Negro))         
           PrimerParametroB = Negrita.render("vez que se selecciona un pictograma o letra." ,1, (Negro)) 
           SegundoParametro = Negrita.render("Desabilitar: No se reproduce el sonido de selección," ,1, (Negro))         
           SegundoParametroB = Negrita.render("pero el sonido de la síntesis de voz sigue activa." ,1, (Negro))       
           screen.blit(TituloInformacion, (470, 15))
           screen.blit(PrimerParametro, (20, 220))
           screen.blit(PrimerParametroB, (20, 280))           
           screen.blit(SegundoParametro, (20, 410))
           screen.blit(SegundoParametroB, (20, 470)) 
           pygame.display.flip()


    def InformacionCursorRestauracion():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 122)
           Negrita = pygame.font.Font(None, 85)
           Fuente = pygame.font.Font(None, 85)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Restauración de Cursor", 1, (Negro))
           PrimerParametro = Negrita.render("Si: Se reinician los parámetros del cursor" ,1, (Negro))         
           PrimerParametroB = Negrita.render("(Velocidad y Sonido)." ,1, (Negro)) 
           CuartoParametro = Negrita.render("No: No reinicia ningún parámetro.",1, (Negro))      
           screen.blit(TituloInformacion, (150, 15))
           screen.blit(PrimerParametro, (35, 230))
           screen.blit(PrimerParametroB, (35, 290))           
           screen.blit(CuartoParametro, (35, 425))
           pygame.display.flip()


    def InformacionCursor():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 122)
           Negrita = pygame.font.Font(None, 67)
           Fuente = pygame.font.Font(None, 67)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Opciones de Cursor", 1, (Negro))
           PrimerParametro = Negrita.render("Velocidad: Modifica la velocidad con la que se desplaza" ,1, (Negro))
           PrimerParametroB = Negrita.render("el cursor." ,1, (Negro))
           SegundoParametro = Negrita.render("Sonido: Activa o desactiva el 'Click' de selección." ,1, (Negro)) 
           TercerParametro = Negrita.render("Restaurar: Se restablecen los valores predeterminados",1, (Negro))
           TercerParametroB = Negrita.render("de cursor.",1, (Negro))
           screen.blit(TituloInformacion, (180, 15))
           screen.blit(PrimerParametro, (20, 210))
           screen.blit(PrimerParametroB, (20, 260))
           screen.blit(SegundoParametro, (20, 350))           
           screen.blit(TercerParametro, (20, 460))
           screen.blit(TercerParametroB, (20, 510))
           pygame.display.flip()


    def InformacionRestauracionSistema():
           ConfiguracionColor("Restaurar")
           TituloFuente = pygame.font.Font(None, 130)
           Negrita = pygame.font.Font(None, 72)
           Fuente = pygame.font.Font(None, 72)
           screen.fill(Azul)
           screen.blit(PictoRegreso, (0, 0))
           screen.blit(CuadritoPeque, (0, 0)) 
           TituloInformacion = TituloFuente.render("Restauración de sistema", 1, (Negro))
           PrimerParametro = Negrita.render("El sistema borra los ajustes realizados y carga los" ,1, (Negro))         
           PrimerParametroB = Negrita.render("parámetros de configuración predeterminados." ,1, (Negro)) 
           screen.blit(TituloInformacion, (100, 15))
           screen.blit(PrimerParametro, (20, 250))
           screen.blit(PrimerParametroB, (20, 350))
           pygame.display.flip()


    def VentanaDeConfirmacionSintTono(Mod):
           fuente = pygame.font.Font(None, 150)                             
           mensaje = fuente.render("Cambio de tono de voz", 1, (Blanco))
           mensaje2 = fuente.render("a género "+Mod+".",1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (170, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)
           
    def VentanaDeConfirmacionSintIdioma(Mod):
           fuente = pygame.font.Font(None, 135)                             
           mensaje = fuente.render("Sintesis de voz en "+Mod, 1, (Blanco))
           mensaje2 = fuente.render("para la interfaz alfabética.",1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (50, 230))
           screen.blit(mensaje2, (50, 370))
           pygame.display.flip()
           pygame.time.delay(5000)
           
    def VentanaDeConfirmacionSintTipo(Mod):
           fuente = pygame.font.Font(None, 150)                             
           mensaje = fuente.render("Cambio de tipo de voz", 1, (Blanco))
           mensaje2 = fuente.render("a "+Mod+".",1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (270, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)

    def VentanaDeConfirmacionInterfaz(Mod,posx):
           fuente = pygame.font.Font(None, 163)                             
           mensaje = fuente.render("Interfaz pictográfica ", 1, (Blanco))
           mensaje2 = fuente.render(Mod,1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (posx, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)
           
    def VentanaDeConfirmacionCurSon(Mod,posx):
           fuente = pygame.font.Font(None, 163)                             
           mensaje = fuente.render("Sonido de selección ", 1, (Blanco))
           mensaje2 = fuente.render(Mod,1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (posx, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)
           
    def VentanaDeConfirmacionCurRest():
           fuente = pygame.font.Font(None, 163)                             
           TituloInformacion = TituloFuente.render("Restauración de cursor", 1, (Negro))
           PrimerParametro = Negrita.render("El sistema carga los ajustes predeterminados" ,1, (Negro))         
           PrimerParametroB = Negrita.render("del cursor." ,1, (Negro)) 
           screen.blit(TituloInformacion, (100, 15))
           screen.blit(PrimerParametro, (20, 250))
           screen.blit(PrimerParametroB, (20, 350))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (200, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)
                  
    def VentanaDeConfirmacionColor(Mod):
           fuente = pygame.font.Font(None, 200)                             
           mensaje = fuente.render("Cambio de fondo", 1, (Blanco))
           mensaje2 = fuente.render("a color "+Mod+".",1, (Blanco))
           screen.fill(Negro) 
           screen.blit(mensaje, (70, 200))
           screen.blit(mensaje2, (220, 380)) 
           pygame.display.flip()
           pygame.time.delay(5000)
                 
    def CargarParametros():
        global Tono
        global Idioma
        global SeleccionPlantillaPictografica
        global VelocidadCursor
        global Sonido
        global ColorDeFondo
        abrirDoc = open(Ubicacion+"Tono.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        Tono=lecturaDeLinea    
        abrirDoc = open(Ubicacion+"Idioma.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        Idioma=lecturaDeLinea
        abrirDoc = open(Ubicacion+"TipodeInterfazPictografica.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        SeleccionPlantillaPictografica=lecturaDeLinea
        abrirDoc = open(Ubicacion+"VelocidadCursor.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        VelocidadCursor=int (lecturaDeLinea)
        abrirDoc = open(Ubicacion+"Sonido.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        Sonido=lecturaDeLinea
        abrirDoc = open(Ubicacion+"ColorDeFondo.txt", "r")
        lecturaDeLinea=abrirDoc.readline()
        ColorDeFondo=lecturaDeLinea
        Color()
        abrirDoc.close()
############################################################################### Métodos para reinicizar los parametros de Configuracion ###################################################################################
    def RestaurarSistema():
        abrirDoc = open(Ubicacion+"Tono.txt", "w")
        abrirDoc.write("m1")
        abrirDoc = open(Ubicacion+"Idioma.txt", "w")
        abrirDoc.write("-ves+")
        abrirDoc = open(Ubicacion+"VelocidadCursor.txt", "w")
        abrirDoc.write("1000")
        abrirDoc = open(Ubicacion+"Sonido.txt", "w")
        abrirDoc.write("Activado")
        abrirDoc = open(Ubicacion+"TipodeInterfazPictografica.txt", "w")
        abrirDoc.write("PlantillaCasa")
        abrirDoc = open(Ubicacion+"ColorDeFondo.txt", "w")
        abrirDoc.write("Azul")   
        abrirDoc.close()
############################################################################### Métodos para restaurar parametros o ingresar nuevo valor de Sintetizador ###################################################################################
    def ConfiguracionSintetizador(NuevoParametro,ArchivoDeTexto=" "):
        if NuevoParametro == "Restaurar":    
           abrirDoc = open(Ubicacion+"Tono.txt", "w")
           abrirDoc.write("m1")
           abrirDoc = open(Ubicacion+"VelocidadSintetizador.txt", "w")
           abrirDoc.write("130")
           abrirDoc = open(Ubicacion+"Idioma.txt", "w")
           abrirDoc.write("-ves+")        
        else:
            abrirDoc = open(Ubicacion+ArchivoDeTexto, "w")
            abrirDoc.write(NuevoParametro)
        abrirDoc.close()
        CargarParametros()
############################################################################### Métodos para restaurar parametros o ingresar nuevo valor de Cursor ###################################################################################
    def ConfiguracionCursor(NuevoParametro,ArchivoDeTexto=" "):
        if NuevoParametro == "Restaurar":        
           abrirDoc = open(Ubicacion+"VelocidadCursor.txt", "w")
           abrirDoc.write("1000")
           abrirDoc = open(Ubicacion+"Sonido.txt", "w")
           abrirDoc.write("Activado")
        else:
            abrirDoc = open(Ubicacion+ArchivoDeTexto, "w")
            abrirDoc.write(NuevoParametro)
        abrirDoc.close()
        CargarParametros()
############################################################################### Métodos para configurar intefa pictografica ###################################################################################
    def ConfiguracionaInterfazPictografica(NuevoParametro):
        abrirDoc = open(Ubicacion+"TipodeInterfazPictografica.txt", "w")
        abrirDoc.write(NuevoParametro)
        abrirDoc.close()
        CargarParametros()
############################################################################### Métodos para restaurar parametros o ingresar nuevo valor de Color ###################################################################################
    def ConfiguracionColor(NuevoParametro):   
        abrirDoc = open(Ubicacion+"ColorDeFondo.txt", "w")
        if NuevoParametro == "Restaurar":
           abrirDoc.write("Azul")
        else:
           abrirDoc.write(NuevoParametro)
           abrirDoc.close() 
        abrirDoc.close()
        CargarParametros()
####################################################################################### Inicia todoas las variables   #############################################################################################
    global frase
    global TamLet
    global PosYCuaTex
    global PosXCuaTex
    global PlantillaNumerica
    global SeleccionPlantillaPictografica
    global ColorDeFondo
    global CursorPrincipalPictografico
    global CursorSecundarioPictografico
    frase=""
    TamLet=""
    PosYCuaTex=""
    PosXCuaTex=""
    SeleccionPlantillaPictografica=""
    PlantillaNumerica=""
####################################################################################### Inicia todoas las variables   #############################################################################################
    CursorPrincipalPictografico = CurPrinCuadroPequeño
    CursorSecundarioPictografico = CurSecCuadroPequeño
    Cuadrito = CursorPrincipalPictografico
    CuadritoPeque = CursorSecundarioPictografico    
##########################################################################  Metodo para Menu de interfaces   ###########################################################################   
    def seleccion(plantilla,Cuadro,posx,posy):     
        global VelocidadCursor
        global PosiciondeTitulo        
        screen.fill(ColorDeFondo)                                                   
        screen.blit(plantilla, (0, 0))                                      
        pygame.display.flip()                                                 
        screen.blit(Cuadro, (posx, posy))                                     
        pygame.display.flip()                                                 
     
################################################################ Metodo para Ajustar el cuadro de texto Principal  ##############################################################################################
    def ProcesamientoDeTextoPrincipal():
        global frase
        global TamLet
        global PosYCuaTex
        global PosXCuaTex
        minus=(frase.lower())
        w =(minus.count("w"))
        m =(minus.count("m"))
        NumCarac=len(frase) + m + w
        if frase == "Borrar todo":
            TamLet=100
            PosYCuaTex=330
            espacio = NumCarac * 15
            PosXCuaTex=590 - espacio
        elif NumCarac >= 1 and NumCarac <=21:
            TamLet=100
            PosYCuaTex=330
            espacio = NumCarac * 15
            PosXCuaTex=590 - espacio
        elif NumCarac >=22 and NumCarac <=26 :
            TamLet=87
            PosYCuaTex=340
            espacio = NumCarac * 13
            PosXCuaTex=590 - espacio
        elif NumCarac >=27 and NumCarac <=31:
            TamLet=74
            PosYCuaTex=345
            PosXCuaTex=200
            espacio = NumCarac * 11.8
            PosXCuaTex=610 - espacio
        elif NumCarac >=32 and NumCarac <=35 :
            TamLet=66
            PosYCuaTex=345
            espacio = NumCarac * 10.9
            PosXCuaTex=590 - espacio
            
        elif NumCarac >=36 and NumCarac <=40:
            TamLet=60
            PosYCuaTex=345
            espacio = NumCarac * 9.9
            PosXCuaTex=590 - espacio

        elif NumCarac >=41 and NumCarac <=43:
            TamLet=55
            PosYCuaTex=345
            espacio = NumCarac * 8.8
            PosXCuaTex=590 - espacio

        elif NumCarac >=44 and NumCarac <=47:
            TamLet=47
            PosYCuaTex=350
            espacio = NumCarac * 7.5
            PosXCuaTex=590 - espacio

        elif NumCarac >=48 and NumCarac <=51:
            TamLet=45
            PosYCuaTex=353
            espacio = NumCarac * 7
            
            PosXCuaTex=590 - espacio
            
        elif NumCarac == 0:
            TamLet=100
            PosYCuaTex=330
            espacio = NumCarac * 15
            PosXCuaTex=590 - espacio

        else:
            TamLet=70
            PosYCuaTex=345
            PosXCuaTex=215   
            frase="Se excedió el número de caracteres"


###########################################  Metodo para Ajustar el cuadro de texto Predictor de textos   ###########################################################################

    def ProcesamientoDeTextoPredictor(palabra,mitadposX):
        global TamLet
        global PosYCuaTex
        global PosXCuaTex              
        global PalabrasEncontradas
        w =(palabra.count("w"))
        m =(palabra.count("m"))
        NumCarac=len(palabra) + m + w

        if NumCarac >= 1 and NumCarac <=5:
            TamLet=72
            PosYCuaTex=443
            espacio = NumCarac * 12
            PosXCuaTex=mitadposX - espacio
            
            
        elif NumCarac >=6 and NumCarac <=10:
            TamLet=67
            PosYCuaTex=448
            espacio = NumCarac * 10.9
            PosXCuaTex=mitadposX - espacio
            
        elif NumCarac >=11 and NumCarac <=14:
            TamLet=56
            PosYCuaTex=450
            espacio = NumCarac * 9.2
            PosXCuaTex=mitadposX - espacio

        elif NumCarac >=15 and NumCarac <=18 :
            TamLet=48
            PosYCuaTex=452
            espacio = NumCarac * 8.4
            PosXCuaTex=mitadposX - espacio

        elif NumCarac >=19 and NumCarac <=23 :
            TamLet=37
            PosYCuaTex=460
            espacio = NumCarac * 5.8
            PosXCuaTex=mitadposX - espacio
            
            
        elif NumCarac == 0:
            TamLet=100
            PosYCuaTex=330
            espacio = NumCarac * 15
            PosXCuaTex=mitadposX - espacio

        else:
            TamLet=70
            PosYCuaTex=345
            PosXCuaTex=215   
            frase="Se exedio el número de caracteres"

###############################################################   Metodo para interfaz pictografica   ################################################################################################            

    def cambio(plantilla,posx,posy,text=" "):         #SE CREA EL METODO "cambio" con los parametros "plantilla,posx,posy,texto=" "---se  ---,posxT=300 ---si no hay parametro se le asigna el valor de 300 --- letraTam=100 ---si no hay parametro  ---"       
        
        global frase
        global TamLet
        global PosYCuaTex
        global PosXCuaTex
        
        frase=text
        ProcesamientoDeTextoPrincipal()
        screen.fill(ColorDeFondo)                                           
        screen.blit(plantilla, (0, 0))                                        #SE CARGA LA PLANTILLA DEL ARGUMENTO  EN LA POSICION (0,0)
        pygame.draw.rect(screen,Negro,(200,595,915,100))                      #SE DIBUJA UN RECUADRO DE COLOR Negro  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO) 
        pygame.draw.rect(screen,Blanco,(205,600,905,90))                      #SE DIBUJA UN RECUADRO DE COLOR Blanco  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO)
        fuente = pygame.font.Font(None, TamLet)                               #SE CREA "fuente" QUE CONTIENE EL TAMAÑO DE LA FUENTE
        mensaje = fuente.render(frase, 1, (0, 0, 0))                          #SE CREA "mensaje" INSERTA "texto" DE COLOR Negro
        screen.blit(mensaje, (PosXCuaTex+50, PosYCuaTex+275))                 #SE INSERTA MENSAJE EN LA POSICION (POSXT= EJE X "DEPENDIENDO EL LARGO DE LA FRASE") Y EN UNA POSICION 603 QUE SERA CONSTANTE
        pygame.display.flip()                                                 #SE REFRESCA EL CONTENIDO DE LA PANTALLA
        screen.blit(Cuadrito, (posx, posy))                                   #SE CARGA IMAGEN tux EN POSICION "posx","posy"
        pygame.display.flip()                                                 #SE REFRESCA EL CONTENIDO DE LA PANTALLA
                                   #SE REALIZA UN DELAY

        
###############################################################   Metodo para regresar a la plantilla previa   ################################################################################################       
                                                                            
    def regreso(plantilla,posX=550,texto="Anterior"):                         #SE CREA EL METODO "regreso" con los parametros "plantilla,posx=550,texto="Anterior"
        screen.fill(ColorDeFondo)
        screen.blit(plantilla, (0, 0))                                        #SE CARGA LA PLANTILLA DEL ARGUMENTO  EN LA POSICION (0,0)
        screen.blit(CuadritoPeque, (0, 0))                                    #SE CARGA LA PLANTILLA DEL ARGUMENTO  EN LA POSICION (0,0)
        pygame.draw.rect(screen,Negro,(200,595,915,100))                      #SE DIBUJA UN RECUADRO DE COLOR Negro  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO)
        pygame.draw.rect(screen,Blanco,(205,600,905,90))                      #SE DIBUJA UN RECUADRO DE COLOR Blanco  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO)
        fuente = pygame.font.Font(None, 100)                                  #SE CREA "fuente" QUE CONTIENE EL TAMAÑO DE LA FUENTE
        mensaje = fuente.render(texto, 1, (0, 0, 0))                          #SE CREA "mensaje" INSERTA "texto" DE COLOR Negro
        screen.blit(mensaje, (posX, 603))                                     #SE INSERTA MENSAJE EN LA POSICION (POSXT= EJE X "DEPENDIENDO EL LARGO DE LA FRASE") Y EN UNA POSICION 603 QUE SERA CONSTANTE
        pygame.display.flip()                                                 #SE REFRESCA EL CONTENIDO DE LA PANTALLA
        
###############################################################   Metodo para entrar a una nueva polantilla con el mismo tema ################################################################################################   
                                                                   
    def siguiente(plantilla):
        screen.fill(ColorDeFondo)                                             #SE CREA EL METODO "siguiente" CON EL PARAMETRO "plantilla"
        screen.blit(plantilla, (0, 0))                                        #SE CARGA LA PLANTILLA DEL ARGUMENTO  EN LA POSICION (0,0)
        screen.blit(CuadritoPeque, (1085,0))                                  #SE CARGA LA PLANTILLA DEL "cuaPe" EN LA POSICION (1090,-22)      
        pygame.draw.rect(screen,Negro,(200,595,915,100))                      #SE DIBUJA UN RECUADRO DE COLOR Negro  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO)
        pygame.draw.rect(screen,Blanco,(205,600,905,90))                      #SE DIBUJA UN RECUADRO DE COLOR Negro  (INCICIO EN X, INCICIO EN Y , LARGO, ANCHO)
        fuente = pygame.font.Font(None, 100)                                  #SE CREA "fuente" QUE CONTIENE EL TAMAÑO DE LA FUENTE
        mensaje = fuente.render("Siguiente", 1, (0, 0, 0))                    #SE CREA "mensaje" INSERTA  EL TEXTO "Siguiente" DE COLOR Negro
        screen.blit(mensaje, (530, 603))                                      #SE INSERTA MENSAJE EN LA POSICION (530,603)
        pygame.display.flip()                                                 #SE REFRESCA EL CONTENIDO DE LA PANTALLA
                                              #SE REALIZA UN DELAY DE 2 S

###############################################################   Metodo para la sintesis de voz   ################################################################################################
        
    def voz(oracion):
        global frase
        global TamLet
        global PosYCuaTex
        global PosXCuaTex
        global SeleccionPlantillaPictografica
        global PlantillaNumerica
        global PlantillaAlfabetica
        global Tono
        global Idioma
        global Sonido


        ProcesamientoDeTextoPrincipal()
        if Sonido=="Activado":
            pygame.mixer.music.play()                                             
            pygame.time.delay(1000)
        else:
            None             

        if PlantillaNumerica=="Activa":
           print("PlantillaNumerica = "+PlantillaNumerica) 
           PosYCuaTex=PosYCuaTex+300
           marcoNegro = pygame.draw.rect(screen,Negro,(170,625,900,90))                    
           lienzoBlanco = pygame.draw.rect(screen,Blanco,(175,630,890,80))
           if frase=="":
               PosXCuaTex=PosXCuaTex-250
               oracion="Escribe una frase"
               marcoNegro         
               lienzoBlanco
               fuente = pygame.font.Font(None, TamLet)
               oracion=oracion.capitalize()
               mensaje = fuente.render(oracion, 1, (0, 0, 0))
               screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))                                    
               pygame.display.flip()                                                              
               pygame.time.delay(2500)
               interfazNumerica()         
           else:
               None
               
        elif PlantillaAlfabetica=="Activada":
           print("PlantillaNumerica = "+PlantillaNumerica)
           print("PlantillaPictografica = "+SeleccionPlantillaPictografica)
           PosYCuaTex=PosYCuaTex+300
           marcoNegro = pygame.draw.rect(screen,Negro,(170,625,900,90))                    
           lienzoBlanco = pygame.draw.rect(screen,Blanco,(175,630,890,80))
           if frase=="":
               PosXCuaTex=PosXCuaTex-250
               oracion="Escribe una frase"
               marcoNegro         
               lienzoBlanco
               fuente = pygame.font.Font(None, TamLet)
               oracion=oracion.capitalize()
               mensaje = fuente.render(oracion, 1, (0, 0, 0))
               screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))                                    
               pygame.display.flip()                                                              
               pygame.time.delay(2500)
               interfazAlfabetica()
               
           else:
               None         
           
        else:
           print("PlantillaPictografica = "+SeleccionPlantillaPictografica) 
           PosXCuaTex=PosXCuaTex+50
           PosYCuaTex=PosYCuaTex+275
           marcoNegro = pygame.draw.rect(screen,Negro,(200,595,915,100))                    
           lienzoBlanco = pygame.draw.rect(screen,Blanco,(205,600,905,90))
           
        
        marcoNegro         
        lienzoBlanco
        fuente = pygame.font.Font(None, TamLet)
        oracion=oracion.capitalize()
        mensaje = fuente.render(oracion, 1, (0, 0, 0))
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))                                    
        pygame.display.flip()
        union = ("espeak "+ Idioma + Tono + " '" + frase  + "' --stdout|aplay")
        print(union)
        os.system(union)
        pygame.time.delay(VelocidadCursor)
        print(union)
        print("Fin de voz")

###############################################################   Metodo para emitir un sonido al seleccionar un objeto ###########################################################################################
        
    def sonidoSeleccion():
        global Sonido
        if Sonido=="Activado":
            pygame.mixer.music.play()                                            
            pygame.time.delay(700)
        else:
            None
            
###############################################################   Metodo para previsualizar el borrado de una letra ################################################################################################
            
    def preborrar(palabra):
        global prefrase
        frase=palabra[:len(palabra)-1]
        prefrase=frase+"-"
        
###############################################################   Metodo para borrar una letra ####################################################################################################################
        
    def borrar(palabra):
        global frase
        frase=palabra[:len(palabra)-1]
        
################################################################   Metodo para Repetir Frase   #####################################################################################################################

    def Repetir(cuadro,posx,posy):
        global frase
        global TamLet
        global PosYCuaTex
        global PosXCuaTexglobal
        global Tono        
        global Predictor1
        global Predictor2
        global Predictor3
        
        ProcesamientoDeTextoPrincipal()         
            
        screen.fill(ColorDeFondo)                                                   
        screen.blit(RepetirFrases, (0, 0))
        pygame.draw.rect(screen,Negro,(170,325,900,90))                    
        pygame.draw.rect(screen,Blanco,(175,330,890,80))
        
        if posx==796:
            
            fuente = pygame.font.Font(None, 100)
            mensaje = fuente.render("Nueva frase", 1, (0, 0, 0))                         
            screen.blit(mensaje, (450, 330))
            pygame.display.flip()                                                 
            screen.blit(cuadro, (0, 0))                                     
            pygame.display.flip()                                                 


        elif cuadro==CuaRegresar:
            
            fuente = pygame.font.Font(None, 100)
            mensaje = fuente.render("Anterior", 1, (0, 0, 0))                         
            screen.blit(mensaje, (530, 330))
            pygame.display.flip()                                                 
            screen.blit(cuadro, (posx, posy))                                     
            pygame.display.flip()                                                 


        else:
        
            fuente = pygame.font.Font(None, TamLet)
          
            primerCaracter=frase[0]
            
            if primerCaracter=="¿":
               None
            else:
               frase=frase.capitalize()
                
            mensaje = fuente.render(frase, 1, (0, 0, 0))                         
            screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))
            pygame.display.flip()                                                 
            screen.blit(cuadro, (posx, posy))                                     
            pygame.display.flip()                                                 


################################################################   Metodo para colocar la frasse en la interfaz numerica   #####################################################################################################################

    def previsualizacionNumerica(pre,Cuadrito=CuaLetra,posx=0,posy=0):
        global TamLet
        global PosYCuaTex
        global PosXCuaTex
        
        if pre =="Borrar todo":
           TamLet=100
           PosYCuaTex=327
           PosXCuaTex=450
        else:
           ProcesamientoDeTextoPrincipal()

        screen.fill(ColorDeFondo)
        screen.blit(Numeros, (0, 0))                          
        pygame.draw.rect(screen,Negro,(170,625,900,90))                    
        pygame.draw.rect(screen,Blanco,(175,630,890,80))               
        fuente = pygame.font.Font(None, TamLet)


        pre=pre.capitalize()
        mensaje = fuente.render(pre, 1, (0, 0, 0))                          
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex+300))                                    
        screen.blit(Cuadrito, (posx, posy))
        pygame.display.flip()


################################################################   Metodo para colocar nombre de contacto telefonico    #####################################################################################################################
# 
#     def Telefonico(pre,Cuadrito=CuaLetra,posx=623,posy=-111,):
#         global TamLet
#         global PosYCuaTex
#         global PosXCuaTex
#         
#         if pre =="Borrar todo":
#           TamLet=100
#           PosYCuaTex=327
#           PosXCuaTex=450
#         else:
#           ProcesamientoDeTextoPrincipal()
#           
#         screen.fill(ColorDeFondo)
#         screen.blit(PlanAlfTelefono, (0, 0))   
#         pygame.draw.rect(screen,Negro,(170,625,900,90))                    
#         pygame.draw.rect(screen,Blanco,(175,630,890,80))               
#         fuente = pygame.font.Font(None, TamLet)
#         pre=pre.capitalize()
#         mensaje = fuente.render(pre, 1, (0, 0, 0))                          
#         screen.blit(mensaje, (PosXCuaTex, PosYCuaTex + 300))                                    
#         screen.blit(Cuadrito, (posx, posy))
#         pygame.display.flip()
#         pygame.time.delay(VelocidadCursor)

##########################################################################  Metodos para interfaz alfabetica   ###########################################################################                                                                             


    def previsualizacion(pre,Cuadrito=CuaLetra,posx=623,posy=-111):
        global Prediccion1
        global Prediccion2
        global Prediccion3
        global TamLet
        global PosYCuaTex
        global PosXCuaTex

        screen.fill(ColorDeFondo)
        screen.blit(Abecedario, (0, 0))
        
        ProcesamientoDeTextoPredictor(Prediccion1,243)
        pygame.draw.rect(screen,Negro,(100,437,300,70))                    
        pygame.draw.rect(screen,Blanco,(105,442,290,60))
        fuente = pygame.font.Font(None, TamLet)
        Prediccion1=Prediccion1.capitalize()
        mensaje = fuente.render(Prediccion1, 1, (0, 0, 0))                         
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))
        Prediccion1=Prediccion1
        
        ProcesamientoDeTextoPredictor(Prediccion2,603)
        pygame.draw.rect(screen,Negro,(460,437,300,70))                    
        pygame.draw.rect(screen,Blanco,(465,442,290,60))
        fuente = pygame.font.Font(None, TamLet)
        Prediccion2=Prediccion2.capitalize()
        mensaje = fuente.render(Prediccion2, 1, (0, 0, 0))                         
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))
        Prediccion2=Prediccion2
        
        ProcesamientoDeTextoPredictor(Prediccion3,1003)
        pygame.draw.rect(screen,Negro,(860,437,300,70))                    
        pygame.draw.rect(screen,Blanco,(865,442,290,60))
        fuente = pygame.font.Font(None, TamLet)
        Prediccion3=Prediccion3.capitalize()
        mensaje = fuente.render(Prediccion3, 1, (0, 0, 0))                         
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex))
        Prediccion3=Prediccion3

        if pre =="Borrar todo":
          TamLet=100
          PosYCuaTex=327
          PosXCuaTex=450
        else:
          ProcesamientoDeTextoPrincipal()
          
        pygame.draw.rect(screen,Negro,(170,625,900,90))                    
        pygame.draw.rect(screen,Blanco,(175,630,890,80))               
        fuente = pygame.font.Font(None, TamLet)
        pre=pre.capitalize()
        mensaje = fuente.render(pre, 1, (0, 0, 0))                          
        screen.blit(mensaje, (PosXCuaTex, PosYCuaTex + 300))                                    
        screen.blit(Cuadrito, (posx, posy))
        pygame.display.flip()




    def TiempoEspera(Interfaz_A_Desplegar):
        x=0
        while x <= VelocidadCursor :
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Interfaz_A_Desplegar()
            time.sleep(0.01)
            x=x+10


    
#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                              #######################################################################
####################################################################   SELECCION DE INTERFAZ      #######################################################################
####################################################################                              #######################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################
 


    def Selecciondeinterfaz():
        CargarParametros()
        global SeleccionPlantillaPictografica
        global PlantillaPictografica
        global PlantillaNumerica
        global PlantillaAlfabetica
        global PlantillaConfiguracion
        global frase
        global Idioma

        
        seleccion(SeleccionInterfaz,CuaAlfa,0,0)
        x=0
        while x <= VelocidadCursor :
            if GPIO.input(21)== GPIO.HIGH:
               PlantillaNumerica="Desactivada"
               PlantillaPictografica="Desactivada"
               PlantillaAlfabetica="Activada"
               sonidoSeleccion()
               frase=""
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
            

        seleccion(SeleccionInterfaz,CuaAlfa,427,0)
        
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Idioma="-ves+"
               PlantillaNumerica="Desactivada"
               PlantillaAlfabetica="Desactivada"
               PlantillaPictografica="Activada"
               SelecciondeinterfazPictografica()
            time.sleep(0.01)
            x=x+10         
                      
         

        seleccion(SeleccionInterfaz,CuaAlfa,850,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               PlantillaNumerica="Desactivada"
               PlantillaAlfabetica="Desactivada"
               PlantillaConfiguraction="Activada"
               frase=""
               Idioma="-ves+"
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10

        Selecciondeinterfaz()

#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                              #######################################################################
####################################################################   SELECCION PICTOGRAFICA     #######################################################################
####################################################################                              #######################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################


    def SelecciondeinterfazPictografica():
        CargarParametros()
        global SeleccionPlantillaPictografica
        global PlantillaPictografica
        global PlantillaNumerica
        global PlantillaAlfabetica
        global PlantillaConfiguracion
        global frase
        global Idioma

        
        seleccion(SeleccionPictografica,CuaAlfa,220,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               PlantillaNumerica="Desactivada"
               PlantillaPictografica="Activada"
               PlantillaAlfabetica="Desactivada"
               sonidoSeleccion()
               ConfiguracionaInterfazPictografica("PlantillaCasa")
               if SeleccionPlantillaPictografica=="PlantillaCasa":
                  interfazGraficaCasa()           
               else:
                   interfazGrafica()
            time.sleep(0.01)
            x=x+10
            
            


        seleccion(SeleccionPictografica,CuaAlfa,630,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Idioma="-ves+"
               PlantillaNumerica="Desactivada"
               PlantillaAlfabetica="Desactivada"
               PlantillaPictografica="Activada"
               
               ConfiguracionaInterfazPictografica("PlantillaHospital")
               if SeleccionPlantillaPictografica=="PlantillaCasa":
                  interfazGraficaCasa()           
               else:
                   interfazGrafica()
            time.sleep(0.01)
            x=x+10
            
               
        seleccion(SeleccionPictografica,CuadritoPeque,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Selecciondeinterfaz()
            time.sleep(0.01)
            x=x+10
    
             

        SelecciondeinterfazPictografica()
        
#############################################################################################################################################################
#############################################################################################################################################################
########################################################                                #####################################################################
########################################################  INTERFAZ DE CONFIGURACION     #####################################################################
########################################################                                #####################################################################
#############################################################################################################################################################
#############################################################################################################################################################

    def interfazConfiguracion():
            
        seleccion(Configuraciones,Cuadrito,0,0)
        TiempoEspera(interfazConfiguracionSintetizador)
        
        seleccion(Configuraciones,Cuadrito,428,0)
        TiempoEspera(interfazConfiguracionColor)

           
        seleccion(Configuraciones,Cuadrito,853,0)
        TiempoEspera(interfazConfiguracionCursor)
           
        seleccion(Configuraciones,Cuadrito,0,290)
        TiempoEspera(ConfiguracionRestaurar)
                     
        seleccion(Configuraciones,CuadritoPeque,0,0)
        TiempoEspera(Selecciondeinterfaz)
    
        interfazConfiguracion()
        
##################################################################################################################################################################################
##########################################################################  CONFIGURACION DE SINTETIZADOR    #####################################################################
##################################################################################################################################################################################
        
    def interfazConfiguracionSintetizador():
            
        seleccion(ConfSintetizador,Cuadrito,0,0)
        TiempoEspera(ConfiguracionSintetizadorTono)

        seleccion(ConfSintetizador,Cuadrito,428,0)
        TiempoEspera(ConfiguracionSintetizadorIdioma)
           
        seleccion(ConfSintetizador,Cuadrito,853,0)
        TiempoEspera(ConfiguracionSintetizadorTipo)
           
        seleccion(ConfSintetizador,Cuadrito,0,290)
        TiempoEspera(ConfiguracionSintetizadorRestaurar)

        seleccion(ConfSintetizador,Cuadrito,428,290)
        TiempoEspera(ConfiguracionSintetizadorInformacion)
          
        seleccion(ConfSintetizador,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracion)
    
        interfazConfiguracionSintetizador()
        
##########################################################################  Configuracion de SINTETIZADOR (TONO)  #####################################################################
 
    def ConfiguracionSintetizadorTono():
        global Tono
        global Idioma

        seleccion(ConfSinTono,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("m1","Tono.txt")
               union = ("espeak -ves+"+ Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTono("masculino")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10
            
         
           
        seleccion(ConfSinTono,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("f4","Tono.txt")
               union = ("espeak -ves+" + Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTono("femenino")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10
               
        seleccion(ConfSinTono,Cuadrito,853,0)
        TiempoEspera(InfSinTono)

           
        seleccion(ConfSinTono,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionSintetizador)
        
                      
        ConfiguracionSintetizadorTono()
        
##########################################################################  Configuracion de SINTETIZADOR (TONO INFORMACION)   ################################################################

    def InfSinTono():

        InformacionSintetizadorTono()
        TiempoEspera(ConfiguracionSintetizadorTono)        
                      
        InfSinTono()

##########################################################################  Configuracion de SINTETIZADOR  (IDIOMA)   #####################################################################      
    
    def ConfiguracionSintetizadorIdioma():
        global Idioma
        global Tono
        
        seleccion(ConfSinIdioma,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("-ves+","Idioma.txt")
               union = ("espeak -ves+" + Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintIdioma("español")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10
                
        seleccion(ConfSinIdioma,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("-ven+","Idioma.txt")
               union = ("espeak -ven+" + Tono +  " 'This is my voice'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintIdioma("inglés")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10
                       
        seleccion(ConfSinIdioma,Cuadrito,853,0)                                      
        TiempoEspera(InfSinIdioma) 

                      
        seleccion(ConfSinIdioma,CuadritoPeque,0,0)                                      
        TiempoEspera(interfazConfiguracionSintetizador)

                      
        ConfiguracionSintetizadorIdioma()
        
##########################################################################  Configuracion de SINTETIZADOR  (DIOMA INFORMACION)   #########################################################
        
    def InfSinIdioma():

        InformacionSintetizadorIdioma()
        TiempoEspera(ConfiguracionSintetizadorIdioma)
                      
        InfSinIdioma()
        
##########################################################################  Configuracion de SINTETIZADOR  (TIPO)   #####################################################################  

    def ConfiguracionSintetizadorTipo():  
        seleccion(ConfSinTipo,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("m1","Tono.txt")
               pygame.time.delay(500)
               union = ("espeak -ves+" + Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTipo("Masculino 1")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10

        seleccion(ConfSinTipo,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("m2","Tono.txt")
               pygame.time.delay(500)
               union = ("espeak -ves+" + Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTipo("Masculino 2")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10

           
        seleccion(ConfSinTipo,Cuadrito,853,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("f4","Tono.txt")
               pygame.time.delay(500)
               union = ("espeak -ves+" + Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTipo("Femenino 1")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10
            
           
        seleccion(ConfSinTipo,Cuadrito,0,290)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("f2","Tono.txt")
               pygame.time.delay(500)
               union = ("espeak -ves+"+ Tono +  " 'Esta sera mi nueva vos'" +  " --stdout|aplay")
               os.system(union)
               VentanaDeConfirmacionSintTipo("Femenino 2")
               interfazConfiguracionSintetizador()
            time.sleep(0.01)
            x=x+10

        seleccion(ConfSinTipo,Cuadrito,428,290)
        TiempoEspera(InfSinTipo)
                      
        seleccion(ConfSinTipo,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionSintetizador)

                      
        ConfiguracionSintetizadorTipo()
        
##########################################################################  Configuracion de SINTETIZADOR (TIPO INFORMACION)   #########################################################
        
    def InfSinTipo():

        InformacionSintetizadorTipodevoz()
        TiempoEspera(ConfiguracionSintetizadorTipo)
        
        InfSinTipo()
        
##########################################################################  Configuracion de SINTETIZADOR (RESTAURACION)   ############################################################

    def ConfiguracionSintetizadorRestaurar():
            
        seleccion(ConfRestaurar,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionSintetizador("Restaurar")
               fuente = pygame.font.Font(None, 163)                             
               mensaje = fuente.render("Restauración exitosa", 1, (Blanco))
               mensaje2 = fuente.render("del sintetizador.",1, (Blanco))
               screen.fill(Negro) 
               screen.blit(mensaje, (70, 200))
               screen.blit(mensaje2, (200, 380)) 
               pygame.display.flip()
               pygame.time.delay(5000)
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            

           
        seleccion(ConfRestaurar,Cuadrito,428,0)
        TiempoEspera(interfazConfiguracionSintetizador)

           
        seleccion(ConfRestaurar,Cuadrito,853,0)
        TiempoEspera(InfSinRestaurar)

                      
        seleccion(ConfRestaurar,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionSintetizador)

                      
        ConfiguracionSintetizadorRestaurar()

        
    def InfSinRestaurar():
        InformacionSintetizadorRestauraciondesintetizador()
        TiempoEspera(ConfiguracionSintetizadorRestaurar)
        
        InfSinRestaurar()
        

    def ConfiguracionSintetizadorInformacion():
            
        InformacionSintetizador()
        TiempoEspera(interfazConfiguracionSintetizador)
        
        ConfiguracionSintetizadorInformacion()
        

#    def InfConfPicto():
#
#        InformacionSelecciondeInterfazPictografica()                                      
#        if GPIO.input(21) == GPIO.HIGH:
#           sonidoSeleccion()
#           interfazConfiguracionSelecciondeInterfazPictografica()
#                      
#        InfConfPicto()

##################################################################################################################################################################################
##########################################################################  CONFIGURACION DE INTERFAZ PICTOGRAFICA   #########################################################################
##################################################################################################################################################################################

#    def interfazConfiguracionSelecciondeInterfazPictografica():
#        seleccion(ConfInterfazPicto,Cuadrito,0,0)                                      
#        if GPIO.input(21) == GPIO.HIGH:
#           sonidoSeleccion()
#           ConfiguracionaInterfazPictografica("PlantillaCasa")
#           VentanaDeConfirmacionInterfaz("casera activada.",160)
#           interfazConfiguracion()
#
#
#        seleccion(ConfInterfazPicto,Cuadrito,428,0)                                      
#        if GPIO.input(21) == GPIO.HIGH:
#           sonidoSeleccion()
#           ConfiguracionaInterfazPictografica("PlantillaHospital")
#           VentanaDeConfirmacionInterfaz("hospitalaria activada.",60)
#           interfazConfiguracion()
#           
#        seleccion(ConfInterfazPicto,Cuadrito,853,0)                                      
#        if GPIO.input(21) == GPIO.HIGH:
#           sonidoSeleccion()
#           InfConfPicto()
#                     
#        seleccion(ConfInterfazPicto,CuadritoPeque,0,0)                                      
#        if GPIO.input(21) == GPIO.HIGH:
#           sonidoSeleccion()
#           interfazConfiguracion()
#           
#        interfazConfiguracionSelecciondeInterfazPictografica()



       
##########################################################################  CONFIGURACION CURSOR    ####################################################################3######################################################

    def interfazConfiguracionCursor():     
        seleccion(ConfCursor,Cuadrito,0,0)
        TiempoEspera(ConfiguracionCursorVelocidad)

        seleccion(ConfCursor,Cuadrito,428,0)
        TiempoEspera(ConfiguracionCursorSonido)
        
        seleccion(ConfCursor,Cuadrito,853,0)
        TiempoEspera(ConfiguracionCursorRestaurar)
        
        seleccion(ConfCursor,Cuadrito,0,290)
        TiempoEspera(ConfiguracionCursorInformacion)

        seleccion(ConfCursor,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracion)
            
        interfazConfiguracionCursor()

####################################################################### Falata bloque de informacion
    def ConfiguracionCursorVelocidad():
        global VelocidadCursor
       
        seleccion(ConfVelocidad,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               if VelocidadCursor == 250:
                   VelocidadCursor="250"
                   ConfiguracionCursor(VelocidadCursor,"VelocidadCursor.txt")
                   CadenaVelocidadCursor = str (VelocidadCursor)
                   fuente = pygame.font.Font(None, 115)                             
                   mensaje = fuente.render("Velocidad maxima = " + CadenaVelocidadCursor+" ms", 1, (Negro))                         
                   screen.blit(mensaje, (65, 400))              
                   pygame.display.flip()
                   pygame.time.delay(5000)
                
               else:      
                   VelocidadCursor = int (VelocidadCursor) - 250
                   VelocidadCursor = str (VelocidadCursor)
                   ConfiguracionCursor(VelocidadCursor,"VelocidadCursor.txt")
                   CadenaVelocidadCursor = str (VelocidadCursor)
                   fuente = pygame.font.Font(None, 115)                             
                   mensaje = fuente.render("Velocidad del cursor = "+ CadenaVelocidadCursor +" ms", 1, (Negro))                         
                   screen.blit(mensaje, (65, 400))              
                   pygame.display.flip()
                   pygame.time.delay(5000)
            time.sleep(0.01)
            x=x+10
                       
           
        seleccion(ConfVelocidad,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               VelocidadCursor = int (VelocidadCursor) + 250
               VelocidadCursor = str (VelocidadCursor)
               ConfiguracionCursor(VelocidadCursor,"VelocidadCursor.txt")
               CadenaVelocidadCursor = str (VelocidadCursor)
               fuente = pygame.font.Font(None, 115)                             
               mensaje = fuente.render("Velocidad del cursor = "+ CadenaVelocidadCursor+" ms", 1, (Negro))                         
               screen.blit(mensaje, (65, 400))              
               pygame.display.flip()
               pygame.time.delay(5000)
            time.sleep(0.01)
            x=x+10
            
           
        seleccion(ConfVelocidad,Cuadrito,853,0)
        TiempoEspera(InfCurVelocidad)        

                                 
        seleccion(ConfVelocidad,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionCursor)

                      
        ConfiguracionCursorVelocidad()


    def InfCurVelocidad():
        InformacionCursorVelocidad()
        TiempoEspera(ConfiguracionCursorVelocidad)        
        InfCurVelocidad()


    def ConfiguracionCursorSonido():
        global Sonido
                
        seleccion(ConfCurSonido,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Sonido="Activado"
               ConfiguracionCursor("Activado","Sonido.txt")
               VentanaDeConfirmacionCurSon("Activado",400)
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            


        seleccion(ConfCurSonido,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Sonido="Desactivado"
               ConfiguracionCursor("Desactivado","Sonido.txt")
               VentanaDeConfirmacionCurSon("Desactivado",330)
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10     
           
        seleccion(ConfCurSonido,Cuadrito,853,0)
        TiempoEspera(InfCurSonido)           
                              
        seleccion(ConfCurSonido,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionCursor) 
                      
        ConfiguracionCursorSonido()
        
    def InfCurSonido():
        InformacionCursorSonido()
        TiempoEspera(ConfiguracionCursorSonido)       
        InfCurSonido()



    def ConfiguracionCursorRestaurar():
            
        seleccion(ConfRestaurar,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionCursor("Restaurar")
               fuente = pygame.font.Font(None, 170)                             
               mensaje = fuente.render("Restauración exitosa", 1, (Blanco))
               mensaje2 = fuente.render("del cursor.",1, (Blanco))
               screen.fill(Negro) 
               screen.blit(mensaje, (70, 200))
               screen.blit(mensaje2, (365, 380)) 
               pygame.display.flip()
               pygame.time.delay(5000)
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            
        seleccion(ConfRestaurar,Cuadrito,428,0)
        TiempoEspera(interfazConfiguracionCursor)

           
        seleccion(ConfRestaurar,Cuadrito,853,0)
        TiempoEspera(InfCurRestauracion)

                      
        seleccion(ConfRestaurar,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracionCursor)
                          
        ConfiguracionCursorRestaurar()

    def InfCurRestauracion():
        InformacionCursorRestauracion()
        TiempoEspera(interfazConfiguracionCursor)      
        InfCurRestauracion()


    def ConfiguracionCursorInformacion():   
        InformacionCursor()
        TiempoEspera(interfazConfiguracionCursor)                        
        ConfiguracionCursorInformacion()


###################################################################################  Configuracion de Color   ####################################################################################################################

    def interfazConfiguracionColor():
        global ColorDeFondo   
        seleccion(ConfColor,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ColorDeFondo = Azul
               ConfiguracionColor("Azul")
               VentanaDeConfirmacionColor("azul")
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            
        
        seleccion(ConfColor,Cuadrito,428,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ColorDeFondo = Rosa
               ConfiguracionColor("Rosa")
               VentanaDeConfirmacionColor("rosa")
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
        

           
        seleccion(ConfColor,Cuadrito,853,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ColorDeFondo = Blanco
               ConfiguracionColor("Blanco")
               VentanaDeConfirmacionColor("blanco")
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            

           
        seleccion(ConfColor,Cuadrito,0,290)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ColorDeFondo = Cafe
               ConfiguracionColor("Cafe")
               VentanaDeConfirmacionColor("café")
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            
           
        seleccion(ConfColor,Cuadrito,428,290)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ColorDeFondo = Verde
               ConfiguracionColor("Verde")
               VentanaDeConfirmacionColor("verde")
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            
           
        seleccion(ConfColor,Cuadrito,853,290)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               ConfiguracionColor("Restaurar")
               fuente = pygame.font.Font(None, 170)                             
               mensaje = fuente.render("Restauración exitosa", 1, (Blanco))
               mensaje2 = fuente.render("de color.",1, (Blanco))
               screen.fill(Negro) 
               screen.blit(mensaje, (70, 200))
               screen.blit(mensaje2, (380, 380)) 
               pygame.display.flip()
               pygame.time.delay(5000)
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            

           
        seleccion(ConfColor,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracion)

    
        interfazConfiguracionColor()

##########################################################################  Configuracion de Restaurar Sistema    #####################################################################

    def ConfiguracionRestaurar():
            
        seleccion(ConfRestaurar,Cuadrito,0,0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               RestaurarSistema()
               CargarParametros()
               fuente = pygame.font.Font(None, 170)                             
               mensaje = fuente.render("Restauración exitosa", 1, (Blanco))
               mensaje2 = fuente.render("del sistema.",1, (Blanco))
               screen.fill(Negro) 
               screen.blit(mensaje, (70, 200))
               screen.blit(mensaje2, (320, 380)) 
               pygame.display.flip()
               pygame.time.delay(5000)
               Selecciondeinterfaz()
               interfazConfiguracion()
            time.sleep(0.01)
            x=x+10
            

        seleccion(ConfRestaurar,Cuadrito,428,0)
        TiempoEspera(interfazConfiguracion)

           
        seleccion(ConfRestaurar,Cuadrito,853,0)                                      
        TiempoEspera(ConfiguracionRestaurarInformacion)
       
                      
        seleccion(ConfRestaurar,CuadritoPeque,0,0)
        TiempoEspera(interfazConfiguracion)

                      
        ConfiguracionRestaurar()
        

    def ConfiguracionRestaurarInformacion():
        
        InformacionRestauracionSistema()
        TiempoEspera(ConfiguracionRestaurar)
                      
        ConfiguracionRestaurarInformacion()

                                          
#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                              #######################################################################
####################################################################      INTERFAZ ALFABETICA     #######################################################################
####################################################################                              #######################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################


##########################################################################  Recorrido de columna    #####################################################################

    def interfazAlfabetica():
        global frase
        global FraseIngresada
        global contacto
        global Prediccion1
        global Prediccion2
        global Prediccion3
        global UltimaFraseIngresada
        
        if frase!='':
#             dato=frase
#             database.PrediccionPalabra()
            NuevaFrase=frase.split()
            CantidadDePalabras=len(NuevaFrase)
            if CantidadDePalabras==0:
                print(NuevaFrase)
                print(CantidadDePalabras,"\n")
                UltimaFraseIngresada=NuevaFrase
                print("Palabra a buscar= ",UltimaFraseIngresada,"\n")
            else:
                print(NuevaFrase)
                print(CantidadDePalabras,"\n")
                UltimaFraseIngresada=NuevaFrase[CantidadDePalabras-1]
                print("Palabra a buscar=",UltimaFraseIngresada,"\n")
            database.PrediccionPalabra()
                        
        else:
            None
            
        previsualizacion(pre= frase,Cuadrito=CuaFila1,posx=0,posy=0)
        TiempoEspera(interfazFila1)

                                                      
        previsualizacion(pre= frase,Cuadrito=CuaFila2,posx=0,posy=0) 
        TiempoEspera(interfazFila2)
           
                                                                                                                     
        previsualizacion(pre= frase,Cuadrito=CuaFila2,posx=0,posy=100) 
        TiempoEspera(interfazFila3)
           
        previsualizacion(pre= frase,Cuadrito=CuaFila2,posx=0,posy=200) 
        TiempoEspera(interfazFila4)
           
        previsualizacion(pre= frase,Cuadrito=CuaFila2,posx=0,posy=310) 
        TiempoEspera(interfazFila5)
           
        previsualizacion(pre= frase,Cuadrito=CuaFila2,posx=0,posy=400) 
        TiempoEspera(interfazFila6)
           
        previsualizacion(pre= frase,Cuadrito=CuaRegresar,posx=0,posy=5)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=""
               Prediccion1=""
               Prediccion2=""
               Prediccion3=""
               Selecciondeinterfaz()
            time.sleep(0.01)
            x=x+10


        interfazAlfabetica()

##########################################################################  Fila 1   #####################################################################

    def interfazFila1():
        global frase
       
        previsualizacion(pre= frase + "a",posx=280,posy=-111)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "a"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10


           
        previsualizacion(pre= frase + "e",posx=385,posy=-111)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "e"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "i",posx=495,posy=-111)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "i"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre= frase + "o",posx=610,posy=-111)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "o"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
          
        previsualizacion(pre= frase + "u",posx=720,posy=-111)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "u"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)
           
        interfazFila1()
    

##########################################################################  Fila 2   #####################################################################

    def interfazFila2():
        global frase
        
        previsualizacion(pre= frase + "s",posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "s"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        
        previsualizacion(pre= frase + "r",posx=134,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "r"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
            
        previsualizacion(pre= frase + "l",posx=272,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "l"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        
        previsualizacion(pre= frase + "t",posx=415,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "t"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
          
        
        previsualizacion(pre= frase + "m",posx=554,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "m"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        
        previsualizacion(pre= frase + "y",posx=720,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "y"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        
        previsualizacion(pre= frase + "q",posx=870,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "q"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        
        previsualizacion(pre= frase + "f",posx=998,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "f"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)
           
        interfazFila2()

##########################################################################      Fila 3   #####################################################################

    def interfazFila3():
        global frase
        
        previsualizacion(pre= frase + "n",posx=0,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "n"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "d",posx=134,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "d"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "c",posx=272,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "c"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre= frase + "p",posx=415,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "p"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
          
        previsualizacion(pre= frase + "h",posx=554,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "h"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre= frase + "g",posx=724,posy=103)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "g"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10()
           
        previsualizacion(pre= frase + "z",posx=870,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "z"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "x",posx=998,posy=95)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "x"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)
           
        interfazFila3()

##########################################################################  Fila 4   ####################################################################  

    def interfazFila4():
        global frase
        
        previsualizacion(pre=frase,posx=0,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + " "
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        preborrar(frase)   
        previsualizacion(pre=prefrase,posx=137,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               borrar(frase)
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10


           
        previsualizacion(pre= frase + "b",posx=272,posy=193)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "b"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "v",posx=418,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "v"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
            
        previsualizacion(pre= frase + "j",posx=554,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "j"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
          
        previsualizacion(pre= frase + "ñ",posx=720,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "ñ"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
            
           
        previsualizacion(pre= frase + "k",posx=870,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "k"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacion(pre= frase + "w",posx=1000,posy=195)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "w"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

        previsualizacion(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)
           
        interfazFila4()
        
##########################################################################  Fila 5   ######################################################################     

    def interfazFila5():
        global frase
        global Prediccion1
        global Prediccion2
        global Prediccion3
        global frase1
        global frase2
        global frase3
        global UltimaFraseIngresada
        global OracionPrediccion
        
        reserva=frase
        PreFrasePrediccion=frase.split()
        CantidadDePalabras=len(PreFrasePrediccion)
        print("CantidadDePalabras=",CantidadDePalabras)
        if CantidadDePalabras==1:
           F1=Prediccion1.capitalize()
           F2=Prediccion2.capitalize()
           F3=Prediccion3.capitalize()
           frase1=F1+" "
           frase2=F2+" "
           frase3=F3+" "
        else:
           print("SEGUNDA CONDICION=",CantidadDePalabras)
           NuevaFrase=frase.split()
           Conteo=len(NuevaFrase)
           Recorte=NuevaFrase[0:(Conteo -1 )]
           OracionPrediccion=' '.join(Recorte)
           print("OracionPrediccion",OracionPrediccion)
           frase1=OracionPrediccion+" "+Prediccion1+ " "
           frase2=OracionPrediccion+" "+Prediccion2+ " "
           frase3=OracionPrediccion+" "+Prediccion3+ " "
           print(frase1,frase2,frase3) 
        
        
        frase=frase1
        previsualizacion(pre=frase1,Cuadrito=CuaPredictor,posx=7,posy=-7) #(135)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase1
               Prediccion1=""
               Prediccion2=""
               Prediccion3=""
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10

           
        frase=frase2
        previsualizacion(pre=frase2,Cuadrito=CuaPredictor,posx=364,posy=-7) #(495)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase2
               Prediccion1=""
               Prediccion2=""
               Prediccion3=""
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
        frase=frase3
        previsualizacion(pre=frase3,Cuadrito=CuaPredictor,posx=766,posy=-7) #(895)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase3
               Prediccion1=""
               Prediccion2=""
               Prediccion3=""
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
            
        frase=reserva
        previsualizacion(pre=reserva, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)       
           
        interfazFila5()

##########################################################################  Fila 6   ########################################################################

    def interfazFila6():
        global frase
        global prefrase
        global PlantillaAlfabetica 
        global Prediccion1
        global Prediccion2
        global Prediccion3
        global UltimaFraseIngresada
        
        previsualizacion(pre=frase,Cuadrito=CuaNumero,posx=0,posy=0) 
        TiempoEspera(interfazNumerica)
        
    
        previsualizacion(pre="Borrar todo",Cuadrito=CuaNuevaFrase,posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=""
               Prediccion1=""
               Prediccion2=""
               Prediccion3=""
               UltimaFraseIngresada=""
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10


        previsualizacion(pre=frase,Cuadrito=CuaVoz,posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               database.ActualizacionDatos() 
               voz(frase)
               RepetirFrase(interfazAlfabetica) 
            time.sleep(0.01)
            x=x+10
         
                 
        previsualizacion(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazAlfabetica)
           
        interfazFila6()

#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                              #######################################################################
####################################################################      INTERFAZ NUMERICA       #######################################################################
####################################################################                              #######################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################


##########################################################################  Recorrido de columna    #####################################################################

    def interfazNumerica():
        global frase
        global SeleccionPlantillaPictografica
        global PlantillaAlfabetica
        global PlantillaNumerica
        PlantillaNumerica="Activa"
 
        previsualizacionNumerica(pre= frase,Cuadrito=CuaFilaNumeros,posx=0,posy=0)
        TiempoEspera(interfazFila1Num)        

        
                                                      
        previsualizacionNumerica(pre= frase,Cuadrito=CuaFilaNumeros,posx=0,posy=210) 
        TiempoEspera(interfazFila2Num) 
           
        previsualizacionNumerica(pre= frase,Cuadrito=CuaFila2,posx=0,posy=410) 
        TiempoEspera(interfazFila3Num)
           
        previsualizacionNumerica(pre= frase,Cuadrito=CuaRegresar,posx=0,posy=5)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               
               if PlantillaAlfabetica=="Activada":
                   PlantillaNumerica="Desactivada"
                   interfazAlfabetica()

               else:
                   PlantillaNumerica="Desactivada"
                   plantillaPeticiones2()
            time.sleep(0.01)
            x=x+10



        interfazNumerica()

##########################################################################  Fila 1   #####################################################################

    def interfazFila1Num():
        global frase
        global Plantilla
        global PlantillaNumerica
        PlantillaNumerica="Activa"
        
        previsualizacionNumerica(pre= frase + "1",posx=112,posy=13)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "1"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacionNumerica(pre= frase + "2",posx=312,posy=13)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "2"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
           
        previsualizacionNumerica(pre= frase + "3",posx=512,posy=13)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "3"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10

        previsualizacionNumerica(pre= frase + "4",posx=712,posy=13)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "4"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
          
        previsualizacionNumerica(pre= frase + "5",posx=912,posy=13)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "5"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10

        previsualizacionNumerica(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazNumerica)

           
        interfazFila1Num()
    

##########################################################################  Fila 2   #####################################################################

    def interfazFila2Num():
        global frase
        global PlantillaNumerica
        PlantillaNumerica="Activa"
        previsualizacionNumerica(pre= frase + "6",posx=112,posy=227)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "6"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
           
        
        previsualizacionNumerica(pre= frase + "7",posx=312,posy=227)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "7"
               interfazAlfabetica()
            time.sleep(0.01)
            x=x+10
           
            
        previsualizacionNumerica(pre= frase + "8",posx=512,posy=227)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "8"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10

        
        previsualizacionNumerica(pre= frase + "9",posx=712,posy=227)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "9"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
          
        
        previsualizacionNumerica(pre= frase + "0",posx=912,posy=227)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + "0"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10


        previsualizacionNumerica(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        TiempoEspera(interfazNumerica)
           
        interfazFila2Num()

##########################################################################  Fila 3   #####################################################################



    def interfazFila3Num():
        global frase
        global prefrase
        global PlantillaNumerica
        PlantillaNumerica="Activa"

        previsualizacionNumerica(pre=frase,Cuadrito=CuaEspacio,posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=frase + " "
               interfazNumerica()
            time.sleep(0.01)
            x=x+10 

        preborrar(frase)   
        previsualizacionNumerica(pre=prefrase,Cuadrito= CuaBorrar,posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               borrar(frase)
               interfazNumerica()
            time.sleep(0.01)
            x=x+10

       
        previsualizacionNumerica(pre="Borrar todo",Cuadrito=CuaNuevaFrase,posx=35,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase=""
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
            


        previsualizacionNumerica(pre=frase,Cuadrito=CuaVoz,posx=25,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz(frase)
               PlantillaNumerica="Desactivada"
               RepetirFrase(interfazNumerica)
            time.sleep(0.01)
            x=x+10
            
                      
        previsualizacionNumerica(pre=frase, Cuadrito=CuaInicio,posx=0,posy=0)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               PlantillaNumerica="Desactivada"
               interfazNumerica()
            time.sleep(0.01)
            x=x+10

           
        interfazFila3Num()

#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                                       ##############################################################
####################################################################      INTERFAZ PICTOGRAFICA CASA       ##############################################################
####################################################################                                       ##############################################################
#########################################################################################################################################################################
#########################################################################################################################################################################    


    def interfazGraficaCasa():                                              #Se crea el metodo principal llamado interfazGrafica "sin parametros"                                        
        cambio(PrincipalCasa,0,0,"Yo")
        TiempoEspera(plantillaYo)                                      #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
 
           
        cambio(PrincipalCasa,428,0,"Alimentos")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaAlimentos)
        
     
           
        cambio(PrincipalCasa,853,0,"Saludos")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaSaludos)
        


        cambio(PrincipalCasa,0,290,"Lugares")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaLugares)
        

          
        cambio(PrincipalCasa,428,290,"Sí")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Sí")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(interfazGraficaCasa)
            time.sleep(0.01)
            x=x+10
        


        cambio(PrincipalCasa,853,290,"No")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("No")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(interfazGraficaCasa)
            time.sleep(0.01)
            x=x+10
           
        regreso(PrincipalCasa,410,"Tipo de interfaz")
        TiempoEspera(SelecciondeinterfazPictografica)                                        #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
                                                                                #Se realiza un VelocidadCursor de 2 S 

        siguiente(PrincipalCasa)
        TiempoEspera(interfazGraficaCasa2)

           
        interfazGraficaCasa()

        

    def interfazGraficaCasa2():                                              #Se crea el metodo principal llamado interfazGrafica "sin parametros"                                        
        cambio(PrincipalCasa2,0,0,"Familia")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaFamilia1) 
           
        cambio(PrincipalCasa2,428,0,"Preguntas")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaPreguntas1)
       
        regreso(PrincipalCasa2,550,"Regreso")                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(interfazGraficaCasa)
                                         #Se realiza un VelocidadCursor de 2 S    
        interfazGraficaCasa2()



    def plantillaSaludos():
        cambio(Saludos,0,0,"Hola")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Hola")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10
                                  #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 


        cambio(Saludos,428,0,"Adiós")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Adiós")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10
           
        cambio(Saludos,853,0,"Hasta mañana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Hasta mañana")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10                                                          #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-


        cambio(Saludos,0,290,"Buenos días")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Buenos días")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10  
          
        cambio(Saludos,428,290,"Buenas tardes")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Buenas tardes")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10  

        cambio(Saludos,853,290,"Buenas noches")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Buenas noches")  
               RepetirFrase(plantillaSaludos)
            time.sleep(0.01)
            x=x+10  
           
        regreso(Saludos,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(interfazGraficaCasa)
                                                   #Se realiza un VelocidadCursor de 2 S 

        plantillaSaludos()




    def plantillaAlimentos():
        cambio(Alimentos,0,0,"Quiero beber")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaBebidas)


        cambio(Alimentos,428,0,"Quiero desayunar")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaDesayuno1)

           
        cambio(Alimentos,853,0,"Quiero comer")
        TiempoEspera(plantillaComida1)                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
 

        cambio(Alimentos,0,290,"Quiero cenar")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaCena1)

          
        cambio(Alimentos,428,290,"Quiero un postre")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaPostre)


        cambio(Alimentos,853,290,"Quiero comer")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaVarios)

           
        regreso(Alimentos,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(interfazGraficaCasa)
                                        #Se realiza un VelocidadCursor de 2 S 

        plantillaAlimentos()



    def plantillaDesayuno1():
        global origenfruta
        origenfruta="Desayuno"
        
        cambio(Desayuno1,0,0,"Quiero desayunar fruta")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaFruta1)


        cambio(Desayuno1,428,0,"Quiero desayunar huevo")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero desayunar huevo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno1)
            time.sleep(0.01)
            x=x+10
                       
        cambio(Desayuno1,853,0,"Quiero beber jugo")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber jugo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno1)
            time.sleep(0.01)
            x=x+10


        cambio(Desayuno1,0,290,"Quiero desayunar donas")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero desayunar donas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno1)
            time.sleep(0.01)
            x=x+10

          
        cambio(Desayuno1,428,290,"Quiero beber café")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber café")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno1)
            time.sleep(0.01)
            x=x+10

        cambio(Desayuno1,853,290,"Quiero desayunar pan")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero desayunar pan")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno1)
            time.sleep(0.01)
            x=x+10
            
           
        regreso(Desayuno1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaAlimentos)
                                         #Se realiza un VelocidadCursor de 2 S 

        siguiente(Desayuno1)
        TiempoEspera(plantillaDesayuno2)

           
        plantillaDesayuno1()



    def plantillaDesayuno2():
        cambio(Desayuno2,0,0,"Quiero beber leche")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber leche")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno2) 
            time.sleep(0.01)
            x=x+10
                                   
        cambio(Desayuno2,428,0,"Quiero beber chocolate")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber chocolate")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno2)
            time.sleep(0.01)
            x=x+10
            
        cambio(Desayuno2,853,0,"Quiero desayunar galletas")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero desayunar galletas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaDesayuno2)
            time.sleep(0.01)
            x=x+10
                                                                              #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
            
        regreso(Desayuno2,550)                                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaDesayuno1)
                                                                                  #Se realiza un VelocidadCursor de 2 S 

        plantillaDesayuno2()



    def plantillaComida1():
        cambio(Comida1,0,0,"Quiero comer sopa")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer sopa")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10

        cambio(Comida1,428,0,"Quiero comer huevo")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer huevo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10
                                                                                 #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
           
        cambio(Comida1,853,0,"Quiero comer guisado")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer guisado")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10
                                                                                   #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 

        cambio(Comida1,0,290,"Quiero beber agua")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber agua")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10
                                                                                          #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
          
        cambio(Comida1,428,290,"Quiero beber refresco")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber refresco")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10


        cambio(Comida1,853,290,"Quiero beber jugo")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber jugo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida1)
            time.sleep(0.01)
            x=x+10


        regreso(Comida1,550)                                            #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaAlimentos)
                                                                              #Se realiza un VelocidadCursor de 2 S 

        siguiente(Comida1)
        TiempoEspera(plantillaComida2)
  
           
        plantillaComida1()



    def plantillaComida2():
        cambio(Comida2,0,0,"Quiero comer ensalada")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer ensalada")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida2)
            time.sleep(0.01)
            x=x+10                                                                 #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 


        cambio(Comida2,428,0,"Quiero comer embutidos")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer embutidos")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComida2)
            time.sleep(0.01)
            x=x+10
 
        cambio(Comida2,853,0,"Comida rápida")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaComidaRapida)
  
           
        regreso(Comida2,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaComida1)
                                         #Se realiza un VelocidadCursor de 2 S 
           
        plantillaComida2()



    def plantillaCena1():       
        cambio(Cena1,0,0,"Quiero cenar cereal")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cenar cereal")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena1)
            time.sleep(0.01)
            x=x+10

        cambio(Cena1,428,0,"Quiero cenar pasta")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cenar pasta")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena1)
            time.sleep(0.01)
            x=x+10

        cambio(Cena1,853,0,"Quiero cenar galletas")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cenar galletas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena1)
            time.sleep(0.01)
            x=x+10

        cambio(Cena1,0,290,"Quiero beber leche")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber leche")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena1)
            time.sleep(0.01)
            x=x+10

          
        cambio(Cena1,428,290,"Quiero beber té")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber té")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena1)
            time.sleep(0.01)
            x=x+10

        cambio(Cena1,853,290,"Quiero cenar pan")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cenar pan")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena)
            time.sleep(0.01)
            x=x+10
        

        regreso(Cena1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(interfazGraficaCasa)
                                          #Se realiza un VelocidadCursor de 2 S 

        siguiente(Cena1)
        TiempoEspera(plantillaCena2)

           
        plantillaCena1()


    def plantillaCena2():
        global origenverdura
        origenverdura="Cena"
        
        cambio(Cena2,0,0,"Quiero cenar yogur")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cenar yogur")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCena2)
            time.sleep(0.01)
            x=x+10
            
        cambio(Cena2,428,0,"Quiero cenar verdura")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaVerdura1)
           
        regreso(Cena2,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaCena1)
                                        #Se realiza un VelocidadCursor de 2 S 
           
        plantillaCena2()

    def plantillaPostre():
        cambio(Postre,0,0,"Quiero comer pastel")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pastel")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
  
        cambio(Postre,428,0,"Quiero comer pay")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pay")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
  
  
        cambio(Postre,853,0,"Quiero comer helado")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer helado")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
   
   
        cambio(Postre,0,290,"Quiero comer flan")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer flan")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
   
   
        cambio(Postre,428,290,"Quiero comer chocolate")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer chocolate")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
            
 

        cambio(Postre,853,290,"Quiero comer natilla")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer natilla")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaPostre)
            time.sleep(0.01)
            x=x+10
                                                                #n sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
           
        regreso(Postre,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaAlimentos)                                   #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
                                         #Se realiza un VelocidadCursor de 2 S 
           
        plantillaPostre()

    def plantillaVarios():
        global origenverdura
        origenverdura="Varios"
        global origenfruta
        origenfruta="Varios"
        
        cambio(Varios,0,0,"Quiero lacteos")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaLacteos1)


        cambio(Varios,428,0,"Quiero carne")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaCarne)
        
                                                  #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    

        cambio(Varios,853,0,"Quiero fruta")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaFruta1)

        
        cambio(Varios,0,290,"Quiero verdura")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaVerdura1)
          
          
        cambio(Varios,428,290,"Quiero snacks")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaSnack)
        
              
        regreso(Varios,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaAlimentos)
                                         #Se realiza un VelocidadCursor de 2 S 
           
        plantillaVarios()

    def plantillaCarne():
        cambio(Carne,0,0,"Quiero comer carne de puerco")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer carne de puerco")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10

        cambio(Carne,428,0,"Quiero comer pescado")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pescado")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10

        cambio(Carne,853,0,"Quiero comer pollo")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pollo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10
 
        cambio(Carne,0,290,"Quiero comer carne de res")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer carne de res")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10
        
        cambio(Carne,428,290,"Quiero comer carne de oveja")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer carne de oveja")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10


        cambio(Carne,853,290,"Quiero comer conejo")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer conejo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaCarne)
            time.sleep(0.01)
            x=x+10

        regreso(Carne,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaVarios)

           
        plantillaCarne()

    def plantillaComidaRapida():
        cambio(ComidaRapida,0,0,"Quiero comer pizza")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pizza")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10



        cambio(ComidaRapida,428,0,"Quiero comer hamburguesa")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer hamburguesa")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10

                                                                                    #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
           
        cambio(ComidaRapida,853,0,"Quiero comer pollo frito")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pollo frito")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10
            

        cambio(ComidaRapida,0,290,"Quiero comer Hot-Dog")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer Hot-Dog")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10

          
        cambio(ComidaRapida,428,290,"Quiero comer papas fritas")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer papas fritas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10
                                                                                 #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
                                        
        cambio(ComidaRapida,853,290,"Quiero comer sándwich")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer sándwich")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaComidaRapida)
            time.sleep(0.01)
            x=x+10
                                                                      #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
           
        regreso(ComidaRapida,550)
        TiempoEspera(plantillaComida2)                             #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
                                        #Se realiza un VelocidadCursor de 2 S 
           
        plantillaComidaRapida()

    def plantillaLacteos1():
        cambio(Lacteos1,0,0,"Quiero comer yogur")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer yogur")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10

        cambio(Lacteos1,428,0,"Quiero beber batidos")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber batidos")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10
                                                                                       #Se realiza un sentencia condicional If donde se evalua el GPIO21 "pin 36" ----se activa con un estado alto y realiza las siguientes acciones--- 
           
        cambio(Lacteos1,853,0,"Quiero comer queso")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer queso")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10
                          
        cambio(Lacteos1,0,290,"Quiero comer natillas")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer natillas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10
        
   
        cambio(Lacteos1,428,290,"Quiero comer helado")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer helado")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10

        cambio(Lacteos1,853,290,"Quiero mantequilla")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero mantequilla")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos1)
            time.sleep(0.01)
            x=x+10

        regreso(Lacteos1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaVarios)

        siguiente(Lacteos1)
        TiempoEspera(plantillaLacteos2)

           
        plantillaLacteos1()

    def plantillaLacteos2():
        cambio(Lacteos2,0,0,"Quiero comer nata")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer nata")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos2)
            time.sleep(0.01)
            x=x+10

        cambio(Lacteos2,428,0,"Quiero comer flan")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer flan")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLacteos2)
            time.sleep(0.01)
            x=x+10
        
    
        regreso(Lacteos2,550)
        TiempoEspera(plantillaLacteos1)                             #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
                                         #Se realiza un VelocidadCursor de 2 S 
           
        plantillaLacteos2()
        
    def plantillaFruta1():
        global OrigenFruta
        
        cambio(Fruta1,0,0,"Quiero comer plátano")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer plátano")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1) 
            time.sleep(0.01)
            x=x+10
            

        cambio(Fruta1,428,0,"Quiero comer manzana")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer manzana")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1)
            time.sleep(0.01)
            x=x+10
            
   
        cambio(Fruta1,853,0,"Quiero comer naranja")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer naranja")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1) 
            time.sleep(0.01)
            x=x+10


        cambio(Fruta1,0,290,"Quiero comer fresas")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer fresas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1) 
            time.sleep(0.01)
            x=x+10
            
 
        cambio(Fruta1,428,290,"Quiero comer durazno")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer durazno")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1)
            time.sleep(0.01)
            x=x+10
        

        cambio(Fruta1,853,290,"Quiero comer uvas")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer uvas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta1)
            time.sleep(0.01)
            x=x+10


        regreso(Fruta1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               
               if origenfruta == "Varios":
                  plantillaVarios()                                          #Se realiza un VelocidadCursor de 2 S
                  
               elif origenfruta == "Desayuno":
                    plantillaDesayuno1() 
            time.sleep(0.01)
            x=x+10
 
        siguiente(Fruta1)
        TiempoEspera(plantillaFruta2)
 
           
        plantillaFruta1()

    def plantillaFruta2():
        cambio(Fruta2,0,0,"Quiero comer piña")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer piña")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Fruta2,428,0,"Quiero comer sandía")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer sandía")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta2)
            time.sleep(0.01)
            x=x+10
        
        
        cambio(Fruta2,853,0,"Quiero comer melón")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer melón")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaFruta2)
            time.sleep(0.01)
            x=x+10
        
        
        regreso(Fruta2,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaFruta1)
                                         #Se realiza un VelocidadCursor de 2 S 
       
        plantillaFruta2()

    def plantillaVerdura1():
        global origenverdura
        
        cambio(Verdura1,0,0,"Quiero comer papas")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer papas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10
        

        cambio(Verdura1,428,0,"Quiero comer tomates")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer tomates")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10
            

        cambio(Verdura1,853,0,"Quiero cebolla")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero cebolla")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10
            

        cambio(Verdura1,0,290,"Quiero comer zanahorias")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer zanahorias")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10
            

        cambio(Verdura1,428,290,"Quiero comer lechugas")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer lechugas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10


        cambio(Verdura1,853,290,"Quiero comer brócolis")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer brócolis")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura1)
            time.sleep(0.01)
            x=x+10
        
        
        regreso(Verdura1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               if origenverdura == "Varios":
                  plantillaVarios()                                          #Se realiza un VelocidadCursor de 2 S
                  
               elif origenverdura == "Cena":
                    plantillaCena2()
            time.sleep(0.01)
            x=x+10

                
        siguiente(Verdura1)
        TiempoEspera(plantillaVerdura2)
        
        
        plantillaVerdura1()


    def plantillaVerdura2():
        cambio(Verdura2,0,0,"Quiero comer pimientos")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pimientos")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura2)
            time.sleep(0.01)
            x=x+10
            

        cambio(Verdura2,428,0,"Quiero comer pepinos")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer pepinos")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura2)
            time.sleep(0.01)
            x=x+10
            
   
        cambio(Verdura2,853,0,"Quiero comer apios")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer apios")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaVerdura2)
            time.sleep(0.01)
            x=x+10
            
      
        regreso(Verdura2,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaVerdura1)
                                                             #Se realiza un VelocidadCursor de 2 S 

        plantillaVerdura2()

    def plantillaSnack():
        cambio(Snack,0,0,"Quiero comer palomitas")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer palomitas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaSnack)
            time.sleep(0.01)
            x=x+10
        

        cambio(Snack,428,0,"Quiero comer gomitas")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer gomitas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaSnack)
            time.sleep(0.01)
            x=x+10
            

        cambio(Snack,853,0,"Quiero comer caramelos")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer caramelos")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaSnack)
            time.sleep(0.01)
            x=x+10
        

        cambio(Snack,0,290,"Quiero comer nueces")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer nueces")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaSnack)
            time.sleep(0.01)
            x=x+10
        
  
        cambio(Snack,428,290,"Quiero comer papas fritas")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero comer papas fritas")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaSnack)
            time.sleep(0.01)
            x=x+10

        regreso(Snack,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaVarios)
                                        #Se realiza un VelocidadCursor de 2 S 
           
        plantillaSnack()

    def plantillaLugares():
        cambio(Lugares,0,0,"Lugares de la casa")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaLugaresCasa)


        cambio(Lugares,428,0,"Lugares de entretenimiento")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaLugaresEntretenimiento1)

           
        cambio(Lugares,853,0,"Quiero ir al supermercado")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al supermercado")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugares)
            time.sleep(0.01)
            x=x+10
        
        cambio(Lugares,0,290,"Quiero ir al hospital")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al hospital")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugares)
            time.sleep(0.01)
            x=x+10

          
        cambio(Lugares,428,290,"Quiero ir a la tienda")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        

        cambio(Lugares,853,290,"Quiero ir al centro comercial")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al centro comercial")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugares)
            time.sleep(0.01)
            x=x+10

        regreso(Lugares,550)
        TiempoEspera(interfazGraficaCasa)                          #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
                                                                 #Se realiza un VelocidadCursor de 2 S 
           
        plantillaLugares()

    def plantillaLugaresCasa():
        cambio(LugaresCasa,0,0,"Quiero ir a la recámara")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir a la recámara")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10
 

        cambio(LugaresCasa,428,0,"Quiero ir al baño")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al baño")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10
        

        cambio(LugaresCasa,853,0,"Quiero ir a la cocina")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir a la cocina")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10
            
        cambio(LugaresCasa,0,290,"Quiero ir al patio")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al patio")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10
        

        cambio(LugaresCasa,428,290,"Quiero ir al comedor")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al comedor")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10

        cambio(LugaresCasa,853,290,"Quiero ir a la sala")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir a la sala")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresCasa)
            time.sleep(0.01)
            x=x+10

        regreso(LugaresCasa,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaLugares) 
                                                          #Se realiza un VelocidadCursor de 2 S 
           
        plantillaLugaresCasa()

    def plantillaLugaresEntretenimiento1():
        cambio(LugaresEntretenimiento1,-10,0,"Quiero ir al cine")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al cine")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10

        cambio(LugaresEntretenimiento1,428,0,"Quiero ir a la cafetería")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir a la cafetería")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10   
       

        cambio(LugaresEntretenimiento1,853,0,"Quiero ir al circo")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al circo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10
            

        cambio(LugaresEntretenimiento1,0,290,"Quiero ir al restaurante")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al restaurante")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10
        
 
        cambio(LugaresEntretenimiento1,428,290,"Quiero ir al museo")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al museo")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10
        

        cambio(LugaresEntretenimiento1,853,290,"Quiero ir al teatro")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al teatro")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento1)
            time.sleep(0.01)
            x=x+10
        
    
        regreso(LugaresEntretenimiento1,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaLugares)
                                        #Se realiza un VelocidadCursor de 2 S 

        siguiente(LugaresEntretenimiento1)
        TiempoEspera(plantillaLugaresEntretenimiento2)

                   
        plantillaLugaresEntretenimiento1()

    def plantillaLugaresEntretenimiento2():
        cambio(LugaresEntretenimiento2,0,0,"Quiero ir al parque")                                             #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al parque")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento2)
            time.sleep(0.01)
            x=x+10
        

        cambio(LugaresEntretenimiento2,428,0,"Quiero ir a un concierto")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir a un concierto")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento2)
            time.sleep(0.01)
            x=x+10        
           
        cambio(LugaresEntretenimiento2,853,0,"Quiero ir al zoológico")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al zoológico")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(plantillaLugaresEntretenimiento2)
            time.sleep(0.01)
            x=x+10
        

        regreso(LugaresEntretenimiento2,550)                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(plantillaLugaresEntretenimiento1)
                                                                              #Se realiza un VelocidadCursor de 2 S 

        plantillaLugaresEntretenimiento2()
        
#########################################################################################################################################################################
#########################################################################################################################################################################
####################################################################                                       ##############################################################
####################################################################      INTERFAZ PICTOGRAFICA HOSPITAL   ##############################################################
####################################################################                                       ##############################################################
#########################################################################################################################################################################
#########################################################################################################################################################################    

    def interfazGrafica():                                                  #Se crea el metodo principal llamado interfazGrafica "sin parametros"                                        
        cambio(Sujeto,0,0,"Yo")                                         #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaYo)

        cambio(Sujeto,428,0,"Personal")                                  #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaPersonal)

        cambio(Sujeto,853,0,"Familia")                                    #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaFamilia1)

        cambio(Sujeto,0,290,"Pregunta")                                   #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(0,0) -cuadro de seleccion se coloca en la posicon 1- **** "Yo" -Se despliega un cuadro con la frase YO- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        TiempoEspera(plantillaPreguntas1)
          
        cambio(Sujeto,428,290,"Sí")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(400,0) -cuadro de seleccion se coloca en la posicon 2- **** "Si" -Se despliega un cuadro con la frase Si- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Sí")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(interfazGrafica)
            time.sleep(0.01)
            x=x+10

        cambio(Sujeto,853,290,"No")                                       #Se manda a llamar el metodo "cambio" con los arguentos "fondo3" -despliega la plantilla principal **** en la posicion(820,0) -cuadro de seleccion se coloca en la posicon 3- **** "No" -Se despliega un cuadro con la frase No- **** "605" -se coloca en la posicion 605 para colocar la frase al centro del recuadro-
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("No")                                                      #Se llama al metodo de voz (realiza una sintesis de voz )con los parametros "Si" -Se despliega un cuadro con la frase Si - y -Realiza la sintesis de voz de esta-***** "605" -se coloca en la posicion 605 para colocar la frase al centro-    
               RepetirFrase(interfazGrafica)
            time.sleep(0.01)
            x=x+10
           
        regreso(Sujeto,410,"Tipo de interfaz")                                #Se manda a llamar al metodo regreso con los parametros "fondo3" despliega la plantilla principal **** "410"-se coloca en la posicion 410 para colocar la frase al centro-  ***** "Tipo de interfaz" -Se despliega un cuadro con la frase Tipo de interfaz-
        TiempoEspera(SelecciondeinterfazPictografica)
                                         

        interfazGrafica()
        
    def plantillaYo():
        global accion
        global plantillaOrigen
        global SeleccionPlantillaPictografica
        
        cambio(Yo,0,0,"Yo quiero")                                
        TiempoEspera(plantillaPeticiones1)  

        cambio(Yo,428,0,"Yo necesito")
        TiempoEspera(plantillaHigiene1)
        
        cambio(Yo,853,0,"Yo tengo")
        TiempoEspera(plantillaMalestar1)
           
        cambio(Yo,0,290,"Yo siento")
        TiempoEspera(plantillaSentimientos1)
                     
        cambio(Yo,428,290,"Tengo comezón")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               accion="Tengo comezón en mi"
               plantillaOrigen=plantillaYo
               plantillaPartesdelCuerpo()
            time.sleep(0.01)
            x=x+10

        cambio(Yo,853,290,"Me duele")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               accion="Tengo dolor en mi"
               plantillaOrigen=plantillaYo
               plantillaPartesdelCuerpo()
            time.sleep(0.01)
            x=x+10

           
        regreso(Yo,550)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()

               if SeleccionPlantillaPictografica == "PlantillaCasa":
                   interfazGraficaCasa()
                       
               else:
                   interfazGrafica()
            time.sleep(0.01)
            x=x+10
             
        plantillaYo()

    def plantillaPersonal():
        global frase
        cambio(Personal,0,0,"Llamar a médico")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a médico")
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10
        
        cambio(Personal,428,0,"Llamar a enfermera")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a enfermera") 
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10

        cambio(Personal,853,0,"Llamar a cirujano")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a cirujano") 
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10

        cambio(Personal,0,290,"Llamar a terapeuta")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a terapeuta")
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10
                             
        cambio(Personal,428,290,"Llamar a fisioterapeuta")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a fisioterapeuta")
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10

           
        cambio(Personal,853,290,"Llamar a limpieza")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a limpieza")
               RepetirFrase(plantillaPersonal)
            time.sleep(0.01)
            x=x+10

        regreso(Personal,550)
        TiempoEspera(interfazGrafica)

        plantillaPersonal()

    def plantillaFamilia1():
        global frase
        global SeleccionPlantillaPictografica
        cambio(Familia1,0,0,"Llamar a hijo")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a hijo") 
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10

        cambio(Familia1,428,0,"Llamar a hija")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a hija")
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10

        cambio(Familia1,853,0,"Llamar a mamá")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a mamá")
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Familia1,0,290,"Llamar a papá")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a papá")
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10
           
        cambio(Familia1,428,290,"Llamar a hermano")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a hermano") 
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Familia1,853,290,"Llamar a hermana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a hermana") 
               RepetirFrase(plantillaFamilia1)
            time.sleep(0.01)
            x=x+10

           
        regreso(Familia1,550)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               if SeleccionPlantillaPictografica == "PlantillaCasa":
                   interfazGraficaCasa2()
                       
               else:
                   interfazGrafica()
            time.sleep(0.01)
            x=x+10

        siguiente(Familia1)
        TiempoEspera(plantillaFamilia2)

                
        plantillaFamilia1()

    def plantillaFamilia2():
        global frase
        cambio(Familia2,0,0,"Llamar a pareja")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a pareja") 
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10


        cambio(Familia2,428,0,"Llamar a primo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a primo") 
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Familia2,853,0,"Llamar a prima")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a prima") 
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Familia2,0,290,"Llamar a abuela")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a abuela") 
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10

                     
        cambio(Familia2,428,290,"Llamar a abuelo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a abuelo")
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Familia2,853,290,"Llamar a tío")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a tío") 
               RepetirFrase(plantillaFamilia2)
            time.sleep(0.01)
            x=x+10

           
        regreso(Familia2,550)
        TiempoEspera(plantillaFamilia1)


        siguiente(Familia2)
        TiempoEspera(plantillaFamilia3)
                
        plantillaFamilia2()
        
        
        
    def plantillaFamilia3():
        global frase
        global SeleccionPlantillaPictografica
        
        cambio(Familia3,0,0,"Llamar a tía")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Llamar a tía")    
               RepetirFrase(plantillaFamilia3)
            time.sleep(0.01)
            x=x+10

        cambio(Familia3,428,0,"Mascota")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Mascota") 
               RepetirFrase(plantillaFamilia3)
            time.sleep(0.01)
            x=x+10
           
        regreso(Familia3,550)
        TiempoEspera(plantillaFamilia2)
               
        plantillaFamilia3()
        
        
    def plantillaPreguntas1():
        global frase
        global SeleccionPlantillaPictografica
        
        cambio(Preguntas1,0,0,"¿Cómo?")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cómo?") 
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10
        

        cambio(Preguntas1,428,0,"¿Cuándo?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cuándo?")
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10  

        cambio(Preguntas1,853,0,"¿Cúantos días?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cúantos días?") 
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10
           
        cambio(Preguntas1,0,290,"¿Cómo estoy?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cómo estoy?")
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10

                     
        cambio(Preguntas1,428,290,"¿Quién?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Quién?") 
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Preguntas1,853,290,"¿Por qué?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Por qué?")
               RepetirFrase(plantillaPreguntas1)
            time.sleep(0.01)
            x=x+10
           
        regreso(Preguntas1,550)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()            
               if SeleccionPlantillaPictografica == "PlantillaCasa":
                   interfazGraficaCasa2()
                       
               else:
                   interfazGrafica()

            time.sleep(0.01)
            x=x+10

        siguiente(Preguntas1)
        TiempoEspera(plantillaPreguntas2)
                
        plantillaPreguntas1() 
     
        
    def plantillaPreguntas2():
        global frase
        cambio(Preguntas2,0,0,"¿Qué hora es?")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Qué hora es?")
               RepetirFrase(plantillaPreguntas2)
            time.sleep(0.01)
            x=x+10


        cambio(Preguntas2,428,0,"¿Cuánto es?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cuánto es?") 
               RepetirFrase(plantillaPreguntas2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Preguntas2,853,0,"¿Dónde?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Dónde?")
               RepetirFrase(plantillaPreguntas2)
            time.sleep(0.01)
            x=x+10

           
        cambio(Preguntas2,0,290,"¿Cuántos?")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("¿Cuántos?")
               RepetirFrase(plantillaPreguntas2)
            time.sleep(0.01)
            x=x+10

        regreso(Preguntas2,550)
        TiempoEspera(plantillaPreguntas1)
                
        plantillaPreguntas2()


    def plantillaPeticiones1():
        global frase
        cambio(Peticiones1,0,0,"Quiero ir al baño")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ir al baño")
               RepetirFrase(plantillaPeticiones1)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones1,428,0,"Quiero bañarme")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero bañarme")
               RepetirFrase(plantillaPeticiones1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones1,853,0,"Quiero dormir")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero dormir") 
               RepetirFrase(plantillaPeticiones1)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones1,0,290,"Quiero leer")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero leer") 
               RepetirFrase(plantillaPeticiones1)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones1,428,290,"Quiero comer")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
                   voz("Quiero comer") 
                   RepetirFrase(plantillaPeticiones1)

            time.sleep(0.01)
            x=x+10
        
        
               
        cambio(Peticiones1,853,290,"Quiero beber")
        TiempoEspera(plantillaBebidas)

           
        regreso(Peticiones1,550)
        TiempoEspera(plantillaYo)


        siguiente(Peticiones1)
        TiempoEspera(plantillaPeticiones2)

                
        plantillaPeticiones1()

    def plantillaBebidas():
        global Frio
        global Templado
        global Caliente
        global Bebida
        global SeleccionPlantillaPictografica
        Frio=" frío"
        Templado=" templado"
        Caliente=" caliente"
        Bebida=""
        cambio(Bebidas,0,0,"Quiero beber agua")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Frio=" fría"
               Templado=" templada"
               Bebida="agua"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10
        
    
        cambio(Bebidas,428,0,"Quiero beber refresco")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Bebida="refresco"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10
        

        cambio(Bebidas,853,0,"Quiero beber leche")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Frio=" fría"
               Templado=" templada"
               Bebida="leche"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10
        

        cambio(Bebidas,0,290,"Quiero beber jugo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Bebida="jugo"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10

                     
        cambio(Bebidas,428,290,"Quiero beber café")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Bebida="café"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10

           
        cambio(Bebidas,853,290,"Quiero beber té")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               Bebida="té"
               plantillaTemperatura()
            time.sleep(0.01)
            x=x+10
           
           
        regreso(Bebidas,550)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
                sonidoSeleccion()            
                if SeleccionPlantillaPictografica == "PlantillaCasa":
                   plantillaAlimentos()    
                else:
                     plantillaPeticiones1()
            time.sleep(0.01)
            x=x+10
            
        plantillaBebidas()
    



    def plantillaTemperatura():                                                       
        global frase
        global Frio
        global Templado
        global Caliente
        global Bebida

        cambio(Temperatura,0,0,"Quiero beber " + Bebida + Frio)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber " + Bebida + Frio)
               RepetirFrase(plantillaTemperatura)
            time.sleep(0.01)
            x=x+10


        cambio(Temperatura,428,0,"Quiero beber " + Bebida + Templado)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber " + Bebida + Templado)
               RepetirFrase(plantillaTemperatura)
            time.sleep(0.01)
            x=x+10


        cambio(Temperatura,853,0,"Quiero beber " + Bebida + Caliente)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero beber " + Bebida + Caliente)
               RepetirFrase(plantillaTemperatura)
            time.sleep(0.01)
            x=x+10
           
        regreso(Temperatura,550)
        TiempoEspera(plantillaBebidas)
     
               
        plantillaTemperatura()
        
    def plantillaPeticiones2():
        global frase
        global PlantillaAlfabetica
        cambio(Peticiones2,0,0,"Quiero ver televisión")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero ver televisión")
               RepetirFrase(plantillaPeticiones2)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones2,428,0,"Apagar la televisión")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Apagar la televisión")
               RepetirFrase(plantillaPeticiones2)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones2,853,0,"Silencio")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Silencio")
               RepetirFrase(plantillaPeticiones2)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones2,0,290,"Quiero escuchar música")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Quiero escuchar música")
               RepetirFrase(plantillaPeticiones2)
            time.sleep(0.01)


        cambio(Peticiones2,428,290,"Volumen")
        TiempoEspera(plantillaVolumen)
          
           
        cambio(Peticiones2,853,290,"Cambiar el canal")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               frase="Cambiar al canal "
               interfazNumerica()
            time.sleep(0.01)
            x=x+10
           
        regreso(Peticiones2,550)
        TiempoEspera(plantillaPeticiones1)


        siguiente(Peticiones2)
        TiempoEspera(plantillaPeticiones3)

                
        plantillaPeticiones2()

    def plantillaVolumen():
        global frase
        cambio(Volumen,0,0,"Subir volumen")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Subir volumen")    
               RepetirFrase(plantillaVolumen)
            time.sleep(0.01)
            x=x+10

        cambio(Volumen,853,0,"Bajar volumen")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Bajar volumen")
               RepetirFrase(plantillaVolumen)
            time.sleep(0.01)
            x=x+10
           
        regreso(Volumen,500)
        TiempoEspera(plantillaPeticiones2)
                
        plantillaVolumen()

    def plantillaPeticiones3():
        global frase
        cambio(Peticiones3,0,0,"Encender aire")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Encender aire")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10 

        cambio(Peticiones3,428,0,"Apagar aire")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Apagar aire")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones3,853,0,"Bajar persiana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Bajar persiana")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones3,0,290,"Subir persiana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Subir persiana")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10
                     
        cambio(Peticiones3,428,290,"Apagar luz")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Apagar luz")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10
           
        cambio(Peticiones3,853,290,"Prender luz")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Prender luz")
               RepetirFrase(plantillaPeticiones3)
            time.sleep(0.01)
            x=x+10
           
        regreso(Peticiones3,550)
        TiempoEspera(plantillaPeticiones2)


        siguiente(Peticiones3)
        TiempoEspera(plantillaPeticiones4)
        
                
        plantillaPeticiones3()

    def plantillaPeticiones4():
        global frase
        cambio(Peticiones4,0,0,"Abrir puerta")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Abrir puerta")
               RepetirFrase(plantillaPeticiones4)
            time.sleep(0.01)
            x=x+10

        cambio(Peticiones4,428,0,"Cerrar puerta")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Cerrar puerta")
               RepetirFrase(plantillaPeticiones4)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones4,853,0,"Abrir ventana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Abrir ventana")
               RepetirFrase(plantillaPeticiones4)
            time.sleep(0.01)
            x=x+10

           
        cambio(Peticiones4,0,290,"Cerrar ventana")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Cerrar ventana")
               RepetirFrase(plantillaPeticiones4)
            time.sleep(0.01)
            x=x+10
           
        cambio(Peticiones4,428,290,"Cambiar posición")
        TiempoEspera(plantillaPosicion1)        
           
        regreso(Peticiones4,550)
        TiempoEspera(plantillaPeticiones3)


        plantillaPeticiones4()

    def plantillaPosicion1():
        global frase
        cambio(Posicion1,0,0,"Subir respaldo")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Subir respaldo")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10


        cambio(Posicion1,428,0,"Bajar respaldo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Bajar respaldo")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10
           
        cambio(Posicion1,853,0,"Subir pies")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Subir pies")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Posicion1,0,290,"Bajar pies")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Bajar pies")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10
                  
        cambio(Posicion1,428,290,"Rotar derecha")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Rotar derecha")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10
            
           
        cambio(Posicion1,853,290,"Rotar izquierda")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Rotar izquierda")
               RepetirFrase(plantillaPosicion1)
            time.sleep(0.01)
            x=x+10

           
        regreso(Posicion1,550)
        TiempoEspera(plantillaPeticiones4)

        siguiente(Posicion1)
        TiempoEspera(plantillaPosicion2)

                
        plantillaPosicion1()

    def plantillaPosicion2():
        global frase
        cambio(Posicion2,0,0,"Boca arriba")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Boca arriba")
               RepetirFrase(plantillaPosicion2)
            time.sleep(0.01)
            x=x+10
        

        cambio(Posicion2,428,0,"Boca abajo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Boca abajo")
               RepetirFrase(plantillaPosicion2)
            time.sleep(0.01)
            x=x+10
                       
        regreso(Posicion2,550)
        TiempoEspera(plantillaPosicion1)


        plantillaPosicion2()

    def plantillaHigiene1():
        global frase
        cambio(Higiene1,0,0,"Necesito bañarme")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito bañarme")    
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene1,428,0,"Necesito lavarme el cabello")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito lavarme el cabello")
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Higiene1,853,0,"Necesito lavarme la cara")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito lavarme la cara")
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene1,0,290,"Necesito lavarme las manos")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito lavarme las manos")
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10
     
           
        cambio(Higiene1,428,290,"Necesito crema")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito crema")          
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10
           
        cambio(Higiene1,853,290,"Necesito limpiarme la boca")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito limpiarme la boca")         
               RepetirFrase(plantillaHigiene1)
            time.sleep(0.01)
            x=x+10

           
        regreso(Higiene1,550)
        TiempoEspera(plantillaYo)

         
        siguiente(Higiene1)
        TiempoEspera(plantillaHigiene2)
                
        plantillaHigiene1()

    def plantillaHigiene2():
        global frase
        cambio(Higiene2,0,0,"Necesito peinarme")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito peinarme")    
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10
           
        cambio(Higiene2,428,0,"Necesito desodorante")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito desodorante")
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene2,853,0,"Necesito perfume")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito perfume")
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10
            
           
        cambio(Higiene2,0,290,"Necesito afeitarme")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito afeitarme")
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene2,428,290,"Necesito un cambio de pañal")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito un cambio de pañal")          
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10
            
           
        cambio(Higiene2,853,290,"Necesito un cambio de toalla")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito un cambio de toalla")         
               RepetirFrase(plantillaHigiene2)
            time.sleep(0.01)
            x=x+10
            
           
        regreso(Higiene2,550)
        TiempoEspera(plantillaHigiene1)


        siguiente(Higiene2)
        TiempoEspera(plantillaHigiene3)

                
        plantillaHigiene2()

    def plantillaHigiene3():
        global frase
        global accion
        global plantillaOrigen
        cambio(Higiene3,0,0,"Necesito enjuague bucal")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito enjuague bucal")    
               RepetirFrase(plantillaHigiene3)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene3,428,0,"Necesito lavarme los dientes")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito lavarme los dientes")
               RepetirFrase(plantillaHigiene3)
            time.sleep(0.01)
            x=x+10
            
        cambio(Higiene3,853,0,"Necesito cortarme las uñas")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito cortarme las uñas")
               RepetirFrase(plantillaHigiene3)
            time.sleep(0.01)
            x=x+10

           
        cambio(Higiene3,0,290,"Necesito un cambio de ropa")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito un cambio de ropa")
               RepetirFrase(plantillaHigiene3)
            time.sleep(0.01)
            x=x+10
           
        cambio(Higiene3,428,290,"Necesito limpiar mis lentes")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz("Necesito limpiar mis lentes")          
               RepetirFrase(plantillaHigiene3)
            time.sleep(0.01)
            x=x+10
           
        cambio(Higiene3,853,290,"Necesito limpiar mi cuerpo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               sonidoSeleccion()
               accion="Necesito limpiar mi"
               plantillaOrigen=plantillaHigiene3
               plantillaPartesdelCuerpo()         
            time.sleep(0.01)
            x=x+10
       

        regreso(Higiene3,550)
        TiempoEspera(plantillaHigiene2)
                
        plantillaHigiene3()

    def plantillaPartesdelCuerpo():
        global accion
        global plantillaOrigen
        if   accion=="Necesito limpiar mi":
             plantillaOrigen=plantillaHigiene3
        else:
            plantillaOrigen=plantillaYo            
           
        cambio(PartesdelCuerpo,0,0,accion + " cabeza")                                
        TiempoEspera(plantillaCabeza1)

        cambio(PartesdelCuerpo,428,0,accion + " torso")
        TiempoEspera(plantillaTorso)
         
        cambio(PartesdelCuerpo,853,0,accion +" brazo")
        TiempoEspera(plantillaBrazo) 
           
        cambio(PartesdelCuerpo,0,290,accion +" pierna")
        TiempoEspera(plantillaPierna)

        regreso(PartesdelCuerpo,550)
        TiempoEspera(plantillaOrigen)

                
        plantillaPartesdelCuerpo()

    def plantillaCabeza1():
        global frase
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo
        global accion
        global plantillaSiguiente
        if accion =="Tengo comezón en mi":
           plantillaSiguiente=plantillaCabeza2Com

        elif accion=="Tengo dolor en mi":
             plantillaSiguiente=plantillaCabeza2Dol
           
        elif accion=="Necesito limpiar mi":
             plantillaSiguiente=plantillaCabeza2Lim
                     
        else:
            None     
        
        cambio(Cabeza1,0,0,accion + "s ojos")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaCabeza1
               parte=" ojo"
               plantillaDireccion()          
            time.sleep(0.01)
            x=x+10              

        cambio(Cabeza1,428,0,accion + "s orejas")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecha"
               izquierdo="izquierda"
               plantillaOrigen = plantillaCabeza1
               parte=" oreja"
               plantillaDireccion()          
            time.sleep(0.01)
            x=x+10
        
        
        cambio(Cabeza1,853,0,accion + " cabeza")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz(accion+" cabeza")
               plantillaOrigen = plantillaCabeza1
               RepetirFrase(plantillaOrigen)        
            time.sleep(0.01)
            x=x+10

        cambio(Cabeza1,0,290,accion + " nariz")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz(accion+" nariz")
               plantillaOrigen = plantillaCabeza1
               RepetirFrase(plantillaOrigen)        
            time.sleep(0.01)

           
        cambio(Cabeza1,428,290,accion + " boca")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21)== GPIO.HIGH:
               voz(accion+" boca")
               plantillaOrigen = plantillaCabeza1
               RepetirFrase(plantillaOrigen)     
            time.sleep(0.01)
            x=x+10
           
        cambio(Cabeza1,853,290,accion + " cuello")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" cuello")
               plantillaOrigen = plantillaCabeza1
               RepetirFrase(plantillaOrigen)        
            time.sleep(0.01)
            x=x+10
        
           
        regreso(Cabeza1,550)
        TiempoEspera(plantillaPartesdelCuerpo)
           
        siguiente(Cabeza1)
        TiempoEspera(plantillaSiguiente)             
       
        plantillaCabeza1()

    def plantillaCabeza2Com():
        global frase
        global accion
        cambio(Cabeza2Com,0,0,accion + " garganta")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" garganta")
               RepetirFrase(plantillaCabeza2Com)        
            time.sleep(0.01)
            x=x+10


        regreso(Cabeza2Com,550)
        TiempoEspera(plantillaCabeza1)     
           
        plantillaCabeza2Com()

    def plantillaCabeza2Dol():
        global frase
        global accion
        cambio(Cabeza2Dol,0,0,accion + "s dientes")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+"s dientes")
               RepetirFrase(plantillaCabeza2Dol)       
            time.sleep(0.01)
            x=x+10

        cambio(Cabeza2Dol,428,0,accion + " garganta")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" garganta")
               RepetirFrase(plantillaCabeza2Dol)       
            time.sleep(0.01)
            x=x+10

        regreso(Cabeza2Dol,550)
        TiempoEspera(plantillaCabeza1)

    
        plantillaCabeza2Dol()

    def plantillaCabeza2Lim():
        global frase
        global accion
        cambio(Cabeza2Lim,0,0,accion + "s dientes")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+"s dientes")
               RepetirFrase(plantillaCabeza2Lim)       
            time.sleep(0.01)
            x=x+10
           
        regreso(Cabeza2Lim,550)
        TiempoEspera(plantillaCabeza1)

        plantillaCabeza2Lim()
   
    def plantillaDireccion():
        global frase
        global derecho
        global accion
        global parte
        global izquierdo
        global plantillaOrigen
                     
        cambio(Direccion,0,0,accion + parte + " " + derecho)                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion + parte +" "+ derecho)
               RepetirFrase(plantillaDireccion)     
            time.sleep(0.01)
            x=x+10
           
        cambio(Direccion,853,0,accion + parte + " " + izquierdo)
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion + parte +" "+ izquierdo)  
               RepetirFrase(plantillaDireccion)       
            time.sleep(0.01)
            x=x+10
           
        regreso(Direccion,550)
        TiempoEspera(plantillaOrigen)       
        
        plantillaDireccion()
       
    def plantillaTorso1():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo 
        cambio(Torso1,0,0,accion+" espalda")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion + " espalda")   
               RepetirFrase(plantillaTorso1)      
            time.sleep(0.01)
            x=x+10
           
        cambio(Torso1,428,0,accion+" glúteo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaTorso1
               parte=" glúteo"
               plantillaDireccion()      
            time.sleep(0.01)
            x=x+10
        
        cambio(Torso1,853,0,accion+" testículo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaTorso1
               parte=" testículo"
               plantillaDireccion()  
            time.sleep(0.01)
            x=x+10
           
        cambio(Torso1,0,290,accion+" pecho")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaTorso1
               parte=" pecho"
               plantillaDireccion()      
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Torso1,428,290,accion+" barriga")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion + " barriga")   
               RepetirFrase(plantillaTorso1)     
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Torso1,853,290,accion+" cadera")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" cadera")
               RepetirFrase(plantillaTorso1)      
            time.sleep(0.01)
            x=x+10
           
        regreso(Torso1,550)
        TiempoEspera(plantillaPartesdelCuerpo)

        siguiente(Torso1)
        TiempoEspera(plantillaTorso2)
                
        plantillaTorso1()

    def plantillaTorso2():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo
        cambio(Torso2,0,0,accion+" pene")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" pene")  
               RepetirFrase(plantillaTorso2)     
            time.sleep(0.01)
            x=x+10
           
        cambio(Torso2,428,0,accion+" vagina")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz(accion+" vagina")
               RepetirFrase(plantillaTorso2)    
            time.sleep(0.01)
            x=x+10
           
        regreso(Torso2,550)
        TiempoEspera(plantillaTorso1)
               
        plantillaTorso2()
        
    def plantillaBrazo():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo
        cambio(Brazo,0,0,accion+" hombro")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaBrazo
               parte=" hombro"
               plantillaDireccion()     
            time.sleep(0.01)
            x=x+10


        cambio(Brazo,428,0,accion+" brazo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaBrazo
               parte=" brazo"
               plantillaDireccion()      
            time.sleep(0.01)
            x=x+10
        
        
        cambio(Brazo,853,0,accion+" muñeca")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecha"
               izquierdo="izquierda"
               plantillaOrigen = plantillaBrazo
               parte=" muñeca"
               plantillaDireccion()      
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Brazo,0,290,accion+" axila")
        x=0
        while x <= VelocidadCursor:         
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecha"
               izquierdo="izquierda"
               plantillaOrigen = plantillaBrazo
               parte=" axila"
               plantillaDireccion()     
            time.sleep(0.01)
            x=x+10
           
        cambio(Brazo,428,290,accion + " mano")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecha"
               izquierdo="izquierda"
               plantillaOrigen = plantillaBrazo
               parte=" mano"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Brazo,853,290,accion + " dedo")
        TiempoEspera(plantillaDedosManos)

           
        regreso(Brazo,550)
        TiempoEspera(plantillaPartesdelCuerpo)

                
        plantillaBrazo()

    def plantillaDedosManos():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo        
        cambio(DedosManos,0,0,accion + " pulgar")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               plantillaOrigen = plantillaDedosManos
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" pulgar"
               plantillaDireccion()               
            time.sleep(0.01)
            x=x+10

        cambio(DedosManos,428,0,accion +" dedo índice")
        x=0
        while x <= VelocidadCursor:        
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosManos
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo índice"
               plantillaDireccion()
            time.sleep(0.01)
            x=x+10
           
        cambio(DedosManos,853,0,accion + " dedo medio")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosManos
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo medio"
               plantillaDireccion()            
            time.sleep(0.01)
            x=x+10
           
        cambio(DedosManos,0,290,accion +" dedo anular")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosManos
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo anular"
               plantillaDireccion()             
            time.sleep(0.01)
            x=x+10
           
        cambio(DedosManos,428,290,accion +" meñique")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosManos
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" meñique"
               plantillaDireccion()             
            time.sleep(0.01)
            x=x+10
           
        regreso(DedosManos,550)
        TiempoEspera(plantillaBrazo)
               
        plantillaDedosManos()

    def plantillaPierna():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo        
        cambio(Piernas,0,0,accion + " muslo")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaPierna
               parte=" muslo"
               plantillaDireccion()               
            time.sleep(0.01)
            x=x+10


        cambio(Piernas,428,0,accion + " chamorro")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaPierna
               parte=" chamorro"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10             
        
        cambio(Piernas,853,0,accion + " talón")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaPierna
               parte=" talón"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10
                   
        cambio(Piernas,0,290,accion + " tobillo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecho"
               izquierdo="izquierdo"
               plantillaOrigen = plantillaPierna
               parte=" tobillo"
               plantillaDireccion()            
            time.sleep(0.01)
            x=x+10     
           
        cambio(Piernas,428,290,accion + " rodilla")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()
               derecho="derecha"
               izquierdo="izquierda"
               plantillaOrigen = plantillaPierna
               parte=" rodilla"
               plantillaDireccion()               
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Piernas,853,290,accion + " dedo")
        TiempoEspera(plantillaDedosPierna)      

        regreso(Piernas,550)
        TiempoEspera(plantillaPartesdelCuerpo)

        plantillaPierna()

    def plantillaDedosPierna():
        global frase
        global accion
        global plantillaOrigen
        global parte
        global derecho
        global izquierdo        
        cambio(DedosPies,0,0,accion + " pulgar")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosPierna
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" pulgar"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10
                     
           
        cambio(DedosPies,428,0,accion +" dedo índice")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosPierna
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo índice"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10
      
        cambio(DedosPies,853,0,accion + " dedo medio")
        x=0
        while x <= VelocidadCursor:            
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosPierna
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo medio"
               plantillaDireccion()
            time.sleep(0.01)
            x=x+10
           
        cambio(DedosPies,0,290,accion +" dedo anular")
        x=0
        while x <= VelocidadCursor:         
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion() 
               plantillaOrigen = plantillaDedosPierna
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" dedo anular"
               plantillaDireccion()
            time.sleep(0.01)
            x=x+10
        
           
        cambio(DedosPies,428,290,accion +" meñique")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               sonidoSeleccion()         
               plantillaOrigen = plantillaDedosPierna
               derecho="derecho"
               izquierdo="izquierdo"
               parte=" meñique"
               plantillaDireccion()              
            time.sleep(0.01)
            x=x+10

        regreso(DedosPies,550)
        TiempoEspera(plantillaPierna)

        plantillaDedosPierna()
        
    def plantillaSentimientos1():
        global frase
        cambio(Sentimientos1,0,0,"Estoy preocupado")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy preocupado")   
               RepetirFrase(plantillaSentimientos1)          
            time.sleep(0.01)
            x=x+10
                     
                     
           
        cambio(Sentimientos1,428,0,"Tengo miedo")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo miedo")   
               RepetirFrase(plantillaSentimientos1)              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Sentimientos1,853,0,"Estoy enfadado")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy enfadado")  
               RepetirFrase(plantillaSentimientos1)              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Sentimientos1,0,290,"Estoy confundido")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy confundido")
               RepetirFrase(plantillaSentimientos1) 
            time.sleep(0.01)
            x=x+10

           
        cambio(Sentimientos1,428,290,"Estoy triste")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy triste")  
               RepetirFrase(plantillaSentimientos1)             
            time.sleep(0.01)
            x=x+10
           
        cambio(Sentimientos1,853,290,"Estoy feliz")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy feliz")
               RepetirFrase(plantillaSentimientos1)              
            time.sleep(0.01)
            x=x+10
           
        regreso(Sentimientos1,550)
        TiempoEspera(plantillaYo)

        siguiente(Sentimientos1)
        TiempoEspera(plantillaSentimientos2)

                
        plantillaSentimientos1()

    def plantillaSentimientos2():
        global frase        
        cambio(Sentimientos2,0,0,"Me siento fuerte")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Me siento fuerte")   
               RepetirFrase(plantillaSentimientos2)              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Sentimientos2,428,0,"Me siento débil")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Me siento débil")   
               RepetirFrase(plantillaSentimientos2)              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Sentimientos2,853,0,"Estoy cansado")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy cansado")  
               RepetirFrase(plantillaSentimientos2)             
            time.sleep(0.01)
            x=x+10
           
           
        cambio(Sentimientos2,0,290,"Estoy aburrido")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy aburrido")
               RepetirFrase(plantillaSentimientos2)              
            time.sleep(0.01)
            x=x+10

           
        cambio(Sentimientos2,428,290,"Me siento sano")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Me siento sano")  
               RepetirFrase(plantillaSentimientos2)             
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Sentimientos2,853,290,"Siento dolor")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Siento dolor")
               RepetirFrase(plantillaSentimientos2)            
            time.sleep(0.01)
            x=x+10
        
           
        regreso(Sentimientos2,550)
        TiempoEspera(plantillaSentimientos1)

               
        plantillaSentimientos2()
  
    def plantillaMalestar1():
        global frase      
        cambio(Malestar1,0,0,"Estoy cansado")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy cansado")
               RepetirFrase(plantillaMalestar1)           
            time.sleep(0.01)
            x=x+10                   

        cambio(Malestar1,428,0,"Tengo frío")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo frío")
               RepetirFrase(plantillaMalestar1)            
            time.sleep(0.01)
            x=x+10        
        
        cambio(Malestar1,853,0,"Tengo calor")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo calor")
               RepetirFrase(plantillaMalestar1)           
            time.sleep(0.01)
            x=x+10        
           
        cambio(Malestar1,0,290,"Tengo taquicardia")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo taquicardia")
               RepetirFrase(plantillaMalestar1)            
            time.sleep(0.01)
            x=x+10        
           
        cambio(Malestar1,428,290,"Tengo comezón")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo comezón")
               RepetirFrase(plantillaMalestar1)          
            time.sleep(0.01)
            x=x+10
                   
        cambio(Malestar1,853,290,"No puedo respirar")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("No puedo respirar")
               RepetirFrase(plantillaMalestar1)            
            time.sleep(0.01)
            x=x+10       
           
        regreso(Malestar1,550)
        TiempoEspera(plantillaYo)

        siguiente(Malestar1)
        TiempoEspera(plantillaMalestar2)

        plantillaMalestar1()

    def plantillaMalestar2():
        global frase        
        cambio(Malestar2,0,0,"Tengo fiebre")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo fiebre")
               RepetirFrase(plantillaMalestar2)           
            time.sleep(0.01)
            x=x+10

        cambio(Malestar2,428,0,"Tengo insomnio")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo insomnio")   
               RepetirFrase(plantillaMalestar2)             
            time.sleep(0.01)
            x=x+10
        

        cambio(Malestar2,853,0,"Tengo alergia")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo alergia")
               frase="Tengo alergia"
               RepetirFrase(plantillaMalestar2)             
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Malestar2,0,290,"Tengo faringitis")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo faringitis")
               RepetirFrase(plantillaMalestar2)              
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Malestar2,428,290,"Tengo mocos")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo mocos")
               RepetirFrase(plantillaMalestar2) 
            time.sleep(0.01)
            x=x+10
           
        cambio(Malestar2,853,290,"Tengo mareos")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo mareos")
               RepetirFrase(plantillaMalestar2)             
            time.sleep(0.01)
            x=x+10
           
        regreso(Malestar2,550)
        TiempoEspera(plantillaMalestar1)

        siguiente(Malestar2)
        TiempoEspera(plantillaMalestar3)

                
        plantillaMalestar2()

    def plantillaMalestar3():
        global frase        
        cambio(Malestar3,0,0,"Estoy sudando")                                
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy sudando")
               RepetirFrase(plantillaMalestar3)            
            time.sleep(0.01)
            x=x+10

        cambio(Malestar3,428,0,"Tengo gases")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo gases")
               RepetirFrase(plantillaMalestar3)            
            time.sleep(0.01)
            x=x+10
        
        cambio(Malestar3,853,0,"Tengo eructos")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo eructos")
               RepetirFrase(plantillaMalestar3)            
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Malestar3,0,290,"Tengo vómito")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo vómito")
               RepetirFrase(plantillaMalestar3)            
            time.sleep(0.01)
            x=x+10
        
           
        cambio(Malestar3,428,290,"Tengo diarrea")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Tengo diarrea")
               RepetirFrase(plantillaMalestar3)             
            time.sleep(0.01)
            x=x+10

        cambio(Malestar3,853,290,"Estoy estriñido")
        x=0
        while x <= VelocidadCursor:
            if GPIO.input(21) == GPIO.HIGH:
               voz("Estoy estriñido")
               RepetirFrase(plantillaMalestar3)             
            time.sleep(0.01)
            x=x+10
           
        regreso(Malestar3,550)
        TiempoEspera(plantillaMalestar2)

        plantillaMalestar3()

    def RepetirFrase(plantillaAnterior):
        global frase
        global Tono
        global Idioma
        global PlantillaAlfabetica
        global PlantillaNumerica
        global PlantillaPictografica
        global Prediccion1
        global Prediccion2
        global Prediccion3
        
        if frase!="":
            Repetir(CuaRepetirFrase,0,0)
            x=0
            while x <= VelocidadCursor:            
                if GPIO.input(21) == GPIO.HIGH:
                   sonidoSeleccion()
                   union = ("espeak "+ Idioma + Tono + " '" + frase  + "' --stdout|aplay")
                   os.system(union)
                   pygame.time.delay(VelocidadCursor)
                   RepetirFrase(plantillaAnterior)
                time.sleep(0.01)
                x=x+10

            Repetir(CuaRepetirFraseInicio,796,0)
            x=0
            while x <= VelocidadCursor:            
                if GPIO.input(21) == GPIO.HIGH:
                   sonidoSeleccion()
                   frase=""
                   Prediccion1=""
                   Prediccion2=""
                   Prediccion3=""
                                  
                   if PlantillaPictografica == "Activada":
                      if SeleccionPlantillaPictografica == "PlantillaHospital":
                          interfazGrafica()
                      else:
                          interfazGraficaCasa()
                        
                   elif PlantillaNumerica == "Activada":
                        interfazNumerica()
                       
                   else:
                       interfazAlfabetica()

                time.sleep(0.01)
                x=x+10

            Repetir(CuaRegresar,3,6)
            TiempoEspera(plantillaAnterior)

            RepetirFrase(plantillaAnterior)

        else:
            None
            
            
            

######################################################################## Ejecucion del programa ########################################################################################################

    os.system("xset -dpms s off")                            ############ Esto desabilita el protector de pantalla por lo que no se apagara la pantalla 
    database = DataBase()
    Selecciondeinterfaz()
                                                                            #AL iniciar se inicializa esta instuccion que manda a llamar aL metodo InterfazGraf     
    for event in pygame.event.get():                                        ###no estoy seguro   //lineas de codigo para mantener la ventana abierta
     if event.type == pygame.QUIT:                                          ###no estoy seguro
             sys.exit()                                                     ###no estoy seguro
             

if __name__ == "__main__":                                                  ###no estoy seguro
    main()
