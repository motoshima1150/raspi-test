import wiringpi as pi
import time, math

class lis3dh:
    def __init__( self, cs ):
        self.cs = cs
        
        buffer = 0x20 << 8 | 0x77
        buffer = buffer.to_bytes( 2, byteorder='big' )
        pi.wiringPiSPIDataRW( self.cs, buffer )

    def spi_read( self, read_addr ):
        command = read_addr | 0x80
        buffer = command << 8
        buffer = buffer.to_bytes( 2, byteorder='big' )
        pi.wiringPiSPIDataRW( self.cs, buffer)
        return( buffer[1] )

    def conv_two_byte( self, high, low ):
        dat = high << 8 | low
        if ( high >= 0x80 ):
            dat = dat - 65536
        dat = dat >> 4
        return ( dat )

    def conv_angle( self, x, y, z ):
        x_angle = math.degrees( math.atan2( x, math.sqrt( y ** 2 + z ** 2 ) ) )
        y_angle = math.degrees( math.atan2( y, math.sqrt( x ** 2 + z ** 2 ) ) )
        return ( x_angle, y_angle )

    def read_accel( self ):
        lb = self.spi_read( 0x28 )
        hb = self.spi_read( 0x29 )
        x = self.conv_two_byte( hb, lb )

        lb = self.spi_read( 0x2a )
        hb = self.spi_read( 0x2b )
        y = self.conv_two_byte( hb, lb )

        lb = self.spi_read( 0x2c )
        hb = self.spi_read( 0x2d )
        z = self.conv_two_byte( hb, lb )
    
        return ( x, y, z )
    


