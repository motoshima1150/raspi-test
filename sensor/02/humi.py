import wiringpi as pi
from dht11 import dht11
import time

HUMI_PIN = 4

pi.wiringPiSetupGpio()

sensor = dht11( HUMI_PIN )

while True:
    ( state, temp, humi ) = sensor.read_sensor()
    
    if ( state == 0 ):
        print( "Temperature:", temp, "C  Humidity:", humi , "%" )
    
    time.sleep(1)
