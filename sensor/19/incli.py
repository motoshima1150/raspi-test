import wiringpi as pi
import time

SENSOR_PIN = 18

pi.wiringPiSetupGpio()
pi.pinMode( SENSOR_PIN, pi.INPUT )

while True:
    if ( pi.digitalRead( SENSOR_PIN ) == pi.HIGH ):
        print ("Standing.")
    else:
        print ("Fall down.")

    time.sleep(1)
