import wiringpi as pi
import time

class isl29125:
    def __init__( self, i2c, addr ):
        self.addr = addr
        self.i2c = i2c
        
        self.isl29125 = self.i2c.setup( self.addr )
        
        val = self.i2c.readReg8( self.isl29125, 0x00 )
        if ( val != 0x7d ):
            print ("Fail")
            return ( -1 )
        
        self.i2c.writeReg8( self.isl29125, 0x00, 0x46 )
        time.sleep(0.1)
        self.i2c.writeReg8( self.isl29125, 0x01, 0x0d )
        self.i2c.writeReg8( self.isl29125, 0x02, 0x3f )
        self.i2c.writeReg8( self.isl29125, 0x03, 0x00 )

    def read_red( self ):
        msb = self.i2c.readReg8( self.isl29125, 0x0c )
        lsb = self.i2c.readReg8( self.isl29125, 0x0b )
        
        data = (msb << 8) | lsb
    
        return( data )
    
    def read_green( self ):
        msb = self.i2c.readReg8( self.isl29125, 0x0a )
        lsb = self.i2c.readReg8( self.isl29125, 0x09 )
        
        data = (msb << 8) | lsb
    
        return( data )

    def read_blue( self ):
        msb = self.i2c.readReg8( self.isl29125, 0x0e )
        lsb = self.i2c.readReg8( self.isl29125, 0x0d )
        
        data = (msb << 8) | lsb
    
        return( data )
    
