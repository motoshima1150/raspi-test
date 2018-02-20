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

    current = volt / 10000
    u_current = current * 1000000
    illumi = 0.6 * u_current ** 0.9655

    print ("Illuminance:", illumi, "lux" )

    time.sleep( 1 )


