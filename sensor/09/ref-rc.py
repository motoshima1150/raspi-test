import wiringpi as pi
from qtr_rc import qtr_rc
import time

ref_pin = 4
sensor_th = 0.00007

pi.wiringPiSetupGpio()

sensor = qtr_rc( ref_pin, sensor_th )

while True:
	if ( sensor.read() == 0 ):
		print( "Black" )
	else:
		print( "White" )

	time.sleep( 1 )

