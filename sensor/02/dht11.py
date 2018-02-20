import wiringpi as pi
import time

class dht11:
    def __init__( self, pin ):
        self.pin = pin
    
    def read_sensor( self ):
        temp = 0.0
        humi = 0.0
        
        pi.pinMode( self.pin, pi.OUTPUT )
        pi.digitalWrite( self.pin, pi.HIGH )
        time.sleep( 0.05 )
        pi.digitalWrite( self.pin, pi.LOW )
        time.sleep( 0.02 )
        
        pi.pinMode( self.pin, pi.INPUT )
        pi.pullUpDnControl( self.pin, pi.PUD_UP )
        
        data = self.collect_input()
        
        lengths = self.parse_data( data )
        
        if( len( lengths ) != 40 ):
            return( -1, 0.0, 0.0 )
        
        bit = self.calc_bit( lengths )
        byte = self.bit_to_byte( bit )
        
        check = byte[0] + byte[1] + byte[2] + byte[3] & 255
        if( byte[4] != check ):
            return( -2, 0, 0 )
        
        return( 0, byte[2], byte[0] )
        
        return( temp, humi )


    def collect_input( self ):
        count = 0
        max_count = 100

        last = -1
        data = []
        while True:
            current = pi.digitalRead( self.pin )
            data.append( current )
            if( last != current ):
                count = 0
                last = current
            else:
                count = count + 1
                if( count > max_count ):
                    break
        return( data )

    def parse_data( self, data ):
        state = 1

        lengths = []
        current_length = 0

        for i in range( len( data ) ) :

            current = data[i]
            current_length = current_length + 1

            if( state == 1 ):
                if( current == pi.LOW ):
                    state = 2
                    continue
                else:
                    continue
            if( state == 2 ):
                if( current == pi.HIGH ):
                    state = 3
                    continue
                else:
                    continue
            if( state == 3 ):
                if( current == pi.LOW ):
                    state = 4
                    continue
                else:
                    continue
            if( state == 4 ):
                if( current == pi.HIGH ):
                    current_length = 0
                    state = 5
                    continue
                else:
                    continue
            if( state == 5 ) :
                if( current == pi.LOW ):
                    lengths.append( current_length )
                    state = 4
                    continue
                else:
                    continue

        return( lengths )

    def calc_bit( self, data ):
        short = 1000
        long = 0

        for i in range( 0, len( data ) ):
            length = data[i]
            if( length < short ):
                short = length
            if( length > long ):
                long = length

        half = short + (long - short) / 2
        bits = []

        for i in range( 0, len( data ) ):
            bit = False
            if( data[i] > half ):
                bit = True
            bits.append( bit )

        return( bits )

    def bit_to_byte( self, bit ):
        return_byte = []
        byte = 0

        for i in range( 0, len( bit ) ):
            byte = byte << 1
            if( bit[i] ):
                byte = byte | 1
            else:
                byte = byte | 0
            if( (i + 1) % 8 == 0 ):
                return_byte.append( byte )
                byte = 0

        return( return_byte )



