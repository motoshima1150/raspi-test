import wiringpi as pi
import time
from mcp3204 import mcp3204

HEATER_PIN = 24
SENSOR_PIN = 23

SPI_CE = 0
SPI_SPEED = 1000000
READ_CH = 0
VREF = 3.3

pi.wiringPiSetupGpio()
pi.pinMode( HEATER_PIN, pi.OUTPUT )
pi.pinMode( SENSOR_PIN, pi.OUTPUT )
pi.digitalWrite( HEATER_PIN, pi.LOW )
pi.digitalWrite( SENSOR_PIN, pi.LOW )

adc = mcp3204( SPI_CE, SPI_SPEED, VREF )

while True:
    i = 0
    while ( i < 5 ):
        time.sleep( 0.242 )
        pi.digitalWrite( HEATER_PIN, pi.HIGH )
        time.sleep( 0.008 )
        pi.digitalWrite( HEATER_PIN, pi.LOW )
        i = i + 1
    time.sleep( 0.237 )
    pi.digitalWrite( SENSOR_PIN, pi.HIGH )
    time.sleep( 0.0025 )

    value = adc.get_value( READ_CH )
    print ("Smell:", value )

    time.sleep( 0.0025 )
    pi.digitalWrite( SENSOR_PIN, pi.LOW )

    time.sleep( 1 )


