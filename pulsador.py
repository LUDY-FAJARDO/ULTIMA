import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Pulsador
Pulsador=18
GPIO.setup(Pulsador, GPIO.IN)

while True:
    
    pul = GPIO.input(Pulsador)
    if pul==0:
        print ("PULSADOR PRESIONADO")
        
    else:
        print ("PULSADOR NO PRESIONADO")