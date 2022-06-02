#Librerias
import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM)
from mpu6050 import mpu6050
import time
import pygame
import firebase_admin
from GetPulse import GetPulse
import requests
mpu = mpu6050(0x68)


#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore


firebase_sdk= credentials.Certificate('activebro-886ff-firebase-adminsdk-ocz4r-314803e1f9.json')
firebase_admin.initialize_app(firebase_sdk,{'databaseURL':'https://activebro-886ff-default-rtdb.firebaseio.com/'})

bp=firestore.client()
peso=bp.collection("users").stream()
for pe in peso:
    ko=pe.to_dict()
    print(ko.get('weight'))


#Reproduccion de audio
pygame.mixer.init()
pygame.display.init()
music_ready=0
music_ready2=0
music_ready3=0
Timer_Descanso=0
descanso_ready=0
descanso_ready2=0
descanso_ready3=0
estoy_descansando=0
Timer_animo=0
animo_ready=0
animo_ready2=0
fin_ready=0
audiofinal1_ready=0
audiofinal1_ready=0

#Sensor de pulso
pulso=GetPulse()
pulso.startAsyncBPM()

#Pulsador
Pulsador=18
GPIO.setup(Pulsador, GPIO.IN)
conteo_pul=0

#Variables de calibracion
dato_cal1x=0
dato_cal1y=0
dato_cal1z=0
dato_cal1x_mas10=0
dato_cal1x_menos10=0
dato_cal1y_mas10=0
dato_cal1y_menos10=0
dato_cal1z_mas10=0
dato_cal1z_menos10=0

dato_cal2x=0
dato_cal2y=0
dato_cal2z=0
dato_cal2x_mas10=0
dato_cal2x_menos10=0
dato_cal2y_mas10=0
dato_cal2y_menos10=0
dato_cal2z_mas10=0
dato_cal2z_menos10=0

#Variables que deben llegar de la aplicacion
Peso_corporal=120 #Libras

#Otras variables
repeticiones=-1
paso1=0
paso2=0
correcto=0
incorrecto=0
inicio_rutina=0
inicio_rutina2=0
Tiempo_inicio=0
Tiempo_actual=0
Tiempo_actual_seg=0
Tiempo_actual_min=0
rutina_completada=0
division1=0
division2=0
multiplicacion1=0
calorias_quemadas=0
reps_incorrectas=0
verif_incorrecto=0
audio_incorrecto=0
control_animo=0

pygame.mixer.music.load("Presentacion.mp3")
pygame.mixer.music.play()
time.sleep(11)

pygame.mixer.music.load("Nombreejercicio.mp3")
pygame.mixer.music.play()
time.sleep(7)

pygame.mixer.music.load("Calibracion1.mp3")
pygame.mixer.music.play()
time.sleep(8)


#Giroscopio
while True:

    #Adquirimos los datos del sensor de pulso

    if(inicio_rutina2==1 and rutina_completada==0):
    
        bpm = pulso.BPM

        if bpm > 0:
            print("BPM: %d" % bpm)
        else:
            print("No se detecta el pulso")

    #Adquirimos los datos del acelerometro

    accel_data = mpu.get_accel_data()
    #print("Acc X : "+str(accel_data['x']))
    #print("Acc Y : "+str(accel_data['y']))
    #print("Acc Z : "+str(accel_data['z']))
    print()
    print("-------------------------------")
    
    #Si se presiona el boton, guardamos el dato 1 de calibracion
    
    pul = GPIO.input(Pulsador)
    if pul==0 and conteo_pul==0:

        dato_cal1x=accel_data['x']
        dato_cal1y=accel_data['y']
        dato_cal1z=accel_data['z']

        print("Calibracion 1 en X: ",dato_cal1x)
        print("Calibracion 1 en Y: ",dato_cal1y)
        print("Calibracion 1 en Z: ",dato_cal1z)

        pygame.mixer.music.load("Calibracion2.mp3")
        pygame.mixer.music.play()
        time.sleep(6)


        if(dato_cal1x > 0):
            dato_cal1x_mas10 = dato_cal1x + dato_cal1x*0.6
            dato_cal1x_menos10= dato_cal1x - dato_cal1x*0.6
            #print(dato_cal1x_mas10,dato_cal1x_menos10)

        elif(dato_cal1x < 0):
            dato_cal1x_menos10 = dato_cal1x + dato_cal1x*0.6
            dato_cal1x_mas10= dato_cal1x - dato_cal1x*0.6
            #print(dato_cal1x_mas10,dato_cal1x_menos10)

        #if(dato_cal1y > 0):
            #dato_cal1y_mas10 = dato_cal1y + dato_cal1y*0.6
            #dato_cal1y_menos10= dato_cal1y - dato_cal1y*0.6
            #print(dato_cal1y_mas10,dato_cal1y_menos10)

        #elif(dato_cal1y < 0):
            #dato_cal1y_menos10 = dato_cal1y + dato_cal1y*0.6
            #dato_cal1y_mas10= dato_cal1y - dato_cal1y*0.6
            #print(dato_cal1y_mas10,dato_cal1y_menos10)
            
        if(dato_cal1z > 0):
            dato_cal1z_mas10 = dato_cal1z + dato_cal1z*0.75
            dato_cal1z_menos10= dato_cal1z - dato_cal1z*0.75
            #print(dato_cal1z_mas10,dato_cal1z_menos10)

        elif(dato_cal1z < 0):
            dato_cal1z_menos10 = dato_cal1z + dato_cal1z*0.75
            dato_cal1z_mas10= dato_cal1z - dato_cal1z*0.75
            #print(dato_cal1z_mas10,dato_cal1z_menos10)

        conteo_pul=1

    #Esperamos a que se despresione el boton
        
    if pul==1 and conteo_pul==1:

        conteo_pul=2
        
    #Si se presiona el boton, guardamos el dato 2 de calibracion
        
    if pul==0 and conteo_pul==2:

        dato_cal2x=accel_data['x']
        dato_cal2y=accel_data['y']
        dato_cal2z=accel_data['z']

        print("Calibracion 2 en X: ",dato_cal2x)
        print("Calibracion 2 en Y: ",dato_cal2y)
        print("Calibracion 2 en Z: ",dato_cal2z)

            
        if(dato_cal2z > 0):
            dato_cal2z_mas10 = dato_cal2z + dato_cal2z*0.75
            dato_cal2z_menos10= dato_cal2z - dato_cal2z*0.75
            print(dato_cal2z_mas10,dato_cal2z_menos10)

        elif(dato_cal2z < 0):
            dato_cal2z_menos10 = dato_cal2z + dato_cal2z*0.75
            dato_cal2z_mas10= dato_cal2z - dato_cal2z*0.75
            print(dato_cal2z_mas10,dato_cal2z_menos10)

        conteo_pul=0
        inicio_rutina=1

    #Empieza la rutina

    if (inicio_rutina==1):
        pygame.mixer.music.load("Comenzarrutina.mp3")
        pygame.mixer.music.play()
        time.sleep(3)
        Tiempo_inicio = time.time()
        inicio_rutina=0
        inicio_rutina2=1
 



        

    #Si el valor actual del acelerometro se encuentra en el rango del dado calibrado 1, paso1=1, ya se tiene la mitad del movimiento
        
    if (accel_data['z']>dato_cal1z_menos10 and accel_data['z']<dato_cal1z_mas10 and paso1==0):
        paso1=1

    #Si el valor actual esta en el rango del dato 2, es por que ya se completo el movimiento
        
    elif (accel_data['z']>dato_cal2z_menos10 and accel_data['z']<dato_cal2z_mas10 and paso1==1):
        paso2=1

    #Analizar si el movimiento se esta haciendo mal

    if(inicio_rutina2==1 and rutina_completada==0):
        
        if (accel_data['x']>dato_cal1x_menos10 and accel_data['x']<dato_cal1x_mas10):
            correcto=1
            print("Movimiento correcto")
            
        else:
            correcto=0

        if(correcto==0 and verif_incorrecto==0):
            Tiempo_incorrecto=time.time()
            verif_incorrecto=1

        while(correcto==0 and estoy_descansando==0):

            #Cronometro    
            Tiempo_actual=time.time()
            Tiempo_actual_seg=round((Tiempo_actual-Tiempo_inicio), 2)
        
            if(Tiempo_actual_seg >= 60):
                Tiempo_actual_min=Tiempo_actual_min+1
                Tiempo_inicio = time.time()

            print("Movimiento INCORRECTO")
            print("Repeticiones: ",repeticiones)
            print("Tiempo transcurrido: ", Tiempo_actual_min, ":", Tiempo_actual_seg)
            print()
            print("-------------------------------")

            if(Tiempo_actual-Tiempo_incorrecto>=10 and audio_incorrecto==0):
                pygame.mixer.music.load("Nomovimiento.mp3")
                pygame.mixer.music.play()
                time.sleep(5)
                audio_incorrecto=1

            accel_data = mpu.get_accel_data()
            if (accel_data['x']>dato_cal1x_menos10 and accel_data['x']<dato_cal1x_mas10):
                correcto=1
                verif_incorrecto=0
                audio_incorrecto=0
                Timer_animo=time.time()
                
            time.sleep(0.3)


    #Si ya se completaron los pasos 1 y 2 y el movimiento es correcto, aumentar las repeticiones
        
    if paso1==1 and paso2==1 and correcto==1 and estoy_descansando==0:
        repeticiones=repeticiones+1
        
        pop = db.reference('/Repeticiones')
        pop.child("numero").set({'valor':repeticiones})
        
        Timer_animo=time.time()
        paso1=0
        paso2=0


    #Esperando a que comience la rutina
    if(inicio_rutina2==0):
        print("Esperando inicio de rutina")

    elif(inicio_rutina2==1 and rutina_completada==0):
        
        #Cronometro    
        Tiempo_actual=time.time()
        Tiempo_actual_seg=round((Tiempo_actual-Tiempo_inicio), 2)
        
        if(Tiempo_actual_seg >= 60):
            Tiempo_actual_min=Tiempo_actual_min+1
            Tiempo_inicio = time.time()
        

        print("Repeticiones: ",repeticiones)
        print("Tiempo transcurrido: ", Tiempo_actual_min, ":", Tiempo_actual_seg)




      #ASI SE ENVIAN LOS DATOS A FIREBASE, PONER AL FINAL DE LA MAQUINA DE ESTADOS, CUANDO FINALICE 
        #data = db.reference ('/prueba')
        #data.push({'datoprub':repeticiones}) #ESTA GUARDANDO EN CARPETA PRUEBA Y ENVIA TODAS LAS REPETICIONES


    if(repeticiones==12 and music_ready==0):
        pygame.mixer.music.load("Descanso1.mp3")
        pygame.mixer.music.play()
        time.sleep(3)
        music_ready=1
        Timer_Descanso=time.time()
        estoy_descansando=1

    if (Tiempo_actual-Timer_Descanso>=15 and descanso_ready==0 and music_ready==1):
        pygame.mixer.music.load("Continua1.mp3")
        pygame.mixer.music.play()
        time.sleep(3)
        descanso_ready=1
        estoy_descansando=0
        Timer_animo=time.time()
        
    if(repeticiones==24 and music_ready2==0):
        pygame.mixer.music.load("Descanso2.mp3")
        pygame.mixer.music.play()
        time.sleep(4)
        music_ready2=1
        Timer_Descanso=time.time()
        estoy_descansando=1

    if (Tiempo_actual-Timer_Descanso>=15 and descanso_ready2==0 and music_ready2==1):
        pygame.mixer.music.load("Continua2.mp3")
        pygame.mixer.music.play()
        time.sleep(4)
        descanso_ready2=1
        estoy_descansando=0
        Timer_animo=time.time()

    if(repeticiones==36 and music_ready3==0):
        pygame.mixer.music.load("Descanso3.mp3")
        pygame.mixer.music.play()
        time.sleep(5)
        music_ready3=1
        Timer_Descanso=time.time()
        estoy_descansando=1 

    if (Tiempo_actual-Timer_Descanso>=15 and descanso_ready3==0 and music_ready3==1):
        pygame.mixer.music.load("Ultimaserie.mp3")
        pygame.mixer.music.play()
        time.sleep(4)
        descanso_ready3=1
        estoy_descansando=0
        Timer_animo=time.time()

    if(Tiempo_actual-Timer_animo>=10 and animo_ready==0 and estoy_descansando==0):
        pygame.mixer.music.load("Animo1.mp3") 
        pygame.mixer.music.play()
        time.sleep(4)
        control_animo=1
        animo_ready=1

    if(control_animo==1 and animo_ready==1):
        Timer_animo=time.time()
        animo_ready=0
        control_animo=0

    if(repeticiones==44 and animo_ready2==0):
        pygame.mixer.music.load("Animo2.mp3")
        pygame.mixer.music.play()
        time.sleep(4)
        animo_ready2=1
    
        
    if(repeticiones>=48):

        if(fin_ready==0):
            pygame.mixer.music.load("Fin.mp3")
            pygame.mixer.music.play()
            time.sleep(8)
            fin_ready=1

        print("RUTINA COMPLETADA")
        print("Tiempo transcurrido: ", Tiempo_actual_min, ":", Tiempo_actual_seg)

        #Se analiza si el usuario se demoro mucho o poco tiempo en completar la rutina
        if(Tiempo_actual_min <= 2 and audiofinal1_ready==0):
            print("Terminaste el ejercicio muy rapido, deberias aumentar el peso")
            pygame.mixer.music.load("AUMENTARPESO.mp3")
            pygame.mixer.music.play()
            time.sleep(5)
            audiofinal1_ready=1
            
            

        if(Tiempo_actual_min >= 5 and audiofinal2_ready==0):
            print("Te demoraste mucho, deberias disminuir el peso")
            pygame.mixer.music.load("DISMINUIRPESO.mp3")
            pygame.mixer.music.play()
            time.sleep(5)
            audiofinal2_ready=1
            
            
        
        print("Presiona  para volver a iniciar")
        inicio_rutina2==0
        rutina_completada=1

        #Calculo de calorias para Curl de Bicep con mancuerna
        #Segun FitClick.com, una persona que pese 150 libras y haga el ejercicio por 5 minutos quema 27 calorias. Hacemos entonces la regla de 3 compuesta.

        division1=150/Peso_corporal
        division2=5/Tiempo_actual_min
        multiplicacion1=division1*division2
        calorias_quemadas=round((27/multiplicacion1),2)

        print("Calorias quemadas: ", calorias_quemadas)
        
        
        time.sleep(1.7)

        #Para volver a empezar se debe presionar el pulsador
        
        pul = GPIO.input(Pulsador)
        if pul==0:
            rutina_completada=0
            repeticiones=0
       
    time.sleep(0.3)


    


        
        
        
