import smbus, time, wiringpi as pi
from aqm0802 import aqm0802

aqm0802_addr = 0x3e
i2c_ch = 1

pi.wiringPiSetupGpio()
i2c = pi.I2C()

aqm0802 = aqm0802( i2c, aqm0802_addr )

aqm0802.move_home( )
aqm0802.set_cursol( 0 )
aqm0802.set_blink( 0 )

aqm0802.write( 'Value' )

value = 37.5139013

output = format( value, '.2f' )
aqm0802.move( 3, 1 )
aqm0802.write( output )


