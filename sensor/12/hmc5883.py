import wiringpi as pi
import time, math

class hmc5883:
    def __init__( self, i2c, addr, scale, scale_data, x_cab, y_cab ):
        self.i2c = i2c
        self.addr = addr
        self.scale = scale
        self.scale_data = scale_data
        self.x_cab = x_cab
        self.y_cab = y_cab

        self.hmc5883 = self.i2c.setup( self.addr )

        self.i2c.writeReg8( self.hmc5883, 0x00, 0x70 )
        self.i2c.writeReg8( self.hmc5883, 0x01, self.scale_data << 5 )
        self.i2c.writeReg8( self.hmc5883, 0x02, 0x00 )
        time.sleep(0.006)

    def get_data( self ):
        while ( self.i2c.readReg8( self.hmc5883, 0x09) != 0x11 ):
            print ("Waiting")
            time.sleep(0.1)

        x_msb = self.i2c.readReg8( self.hmc5883, 0x03 )
        x_lsb = self.i2c.readReg8( self.hmc5883, 0x04 )
        x_data = ( x_msb << 8 ) + x_lsb
        if ( x_data >= 0x8000 ):
            x_data = x_data - 0x10000

        z_msb = self.i2c.readReg8( self.hmc5883, 0x05 )
        z_lsb = self.i2c.readReg8( self.hmc5883, 0x06 )
        z_data = ( z_msb << 8 ) + z_lsb
        if ( z_data >= 0x8000 ):
            z_data = z_data - 0x10000

        y_msb = self.i2c.readReg8( self.hmc5883, 0x07 )
        y_lsb = self.i2c.readReg8( self.hmc5883, 0x08 )
        y_data = ( y_msb << 8 ) + y_lsb
        if ( y_data >= 0x8000 ):
            y_data = y_data - 0x10000
        
        return ( x_data, y_data, z_data )

    def calib( self, x, y ):
        x = x - self.x_cab
        y = y - self.y_cab
        return( x, y )

    def angle( self, x, y ):
        angle_rad = math.atan2( y, x ) 
        angle_deg = math.degrees( angle_rad )
        
        return ( angle_deg )
        
