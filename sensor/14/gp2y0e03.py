import wiringpi as pi

class gp2y0e03:
    def __init__( self, i2c, addr ):
        self.i2c = i2c
        self.addr = addr
        
        self.ir_mod = self.i2c.setup( addr )
        
    def read_distance( self ):
        shift = self.i2c.readReg8( self.ir_mod, 0x35 )
        d_h = self.i2c.readReg8( self.ir_mod, 0x5e )
        d_l = self.i2c.readReg8( self.ir_mod, 0x5f )

        d = ( d_h << 4 ) + d_l
        dist = d / ( 16 * pow( 2, shift ) )    
        
        return (dist)
 
