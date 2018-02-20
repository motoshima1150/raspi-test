import wiringpi as pi
import time
from mcp3204 import mcp3204

MIN = 100
MAX = 3100

SPI_CE = 0
SPI_SPEED = 1000000
READ_CH = 0
VREF = 3.3

adc = mcp3204( SPI_CE, SPI_SPEED, VREF )

while True:
    value = adc.get_value( READ_CH )

    if ( value > MIN and value < MAX ):
        pos = int( ( value - MIN ) / ( MAX - MIN ) * 100.0 )
        print ("Position:", pos )

    time.sleep( 0.1 )


