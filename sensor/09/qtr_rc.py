import wiringpi as pi
import time

class qtr_rc:
	def __init__( self, pin, th ):
		self.pin = pin
		self.th = th

	def read( self ):
		pi.pinMode( self.pin , pi.OUTPUT )
		pi.digitalWrite( self.pin, pi.HIGH )
		time.sleep( 0.01 )
		timer_start = time.time()

		pi.pinMode( self.pin, pi.INPUT )
		pi.pullUpDnControl( self.pin, pi.PUD_DOWN )

		while( pi.digitalRead( self.pin ) == pi.HIGH ):
			pass

		timer_stop = time.time()

		duration = timer_stop - timer_start

		if ( duration > self.th ):
			return( 0 )
		else:
			return( 1 )




