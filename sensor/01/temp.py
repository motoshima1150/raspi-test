import wiringpi as pi
import time
from mcp3204 import mcp3204

SPI_CE = 0
SPI_SPEED = 1000000
READ_CH = 0
VREF = 3.3

adc = mcp3204( SPI_CE, SPI_SPEED, VREF )

while True:
    value = adc.get_value( READ_CH )
    volt = adc.get_volt( value )

    temp = ( volt - 0.6 ) * 100

    print ("Temp:", temp, "C" )

    time.sleep( 1 )


