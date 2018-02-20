import wiringpi as pi
import time

class lsm9ds1:
    def __init__( self, i2c, gyro_addr, mag_addr ):
        self.gyro_addr = gyro_addr
        self.mag_addr = mag_addr
        self.i2c = i2c
        
        self.g_x = 0
        self.g_y = 0
        self.g_z = 0
        
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0
        
        self.m_x = 0
        self.m_y = 0
        self.m_z = 0
        
        self.lsm9ds1_gyro = self.i2c.setup( self.gyro_addr )
        self.lsm9ds1_mag = self.i2c.setup( self.mag_addr )

        val = self.i2c.readReg8( self.lsm9ds1_gyro, 0x0f )
        if ( val != 0x68 ):
            print("Fail")
            return(-1)

        self.i2c.writeReg8( self.lsm9ds1_gyro, 0x1e, 0x38 )
        self.i2c.writeReg8( self.lsm9ds1_gyro, 0x10, 0x81 )
        self.i2c.writeReg8( self.lsm9ds1_gyro, 0x1f, 0x38 )
        self.i2c.writeReg8( self.lsm9ds1_gyro, 0x38, 0x87 )
        self.i2c.writeReg8( self.lsm9ds1_gyro, 0x22, 0x44 )
        time.sleep(0.1)

        self.i2c.writeReg8( self.lsm9ds1_mag, 0x20, 0xd0 )
        self.i2c.writeReg8( self.lsm9ds1_mag, 0x21, 0x00 )
        self.i2c.writeReg8( self.lsm9ds1_mag, 0x22, 0x00 )
        self.i2c.writeReg8( self.lsm9ds1_mag, 0x23, 0x08 )
        self.i2c.writeReg8( self.lsm9ds1_mag, 0x24, 0x40 )
        time.sleep(0.1)
        
    def read_sensor( self ):
        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x18 )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x19 )
        data = msb << 8 | lsb
        self.g_x = data * 8.71 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x1a )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x1b )
        data = msb << 8 | lsb
        self.g_y = data * 8.71 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x1c )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x1d )
        data = msb << 8 | lsb
        self.g_z = data * 8.71 /1000
    
        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x28 )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x29 )
        data = msb << 8 | lsb
        self.a_x = data * 0.061 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x2a )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x2b )
        data = msb << 8 | lsb
        self.a_y = data * 0.061 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x2c )
        msb = self.i2c.readReg8( self.lsm9ds1_gyro, 0x2d )
        data = msb << 8 | lsb
        self.a_z = data * 0.061 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_mag, 0x28 )
        msb = self.i2c.readReg8( self.lsm9ds1_mag, 0x29 )
        data = msb << 8 | lsb
        self.m_x = data * 0.14 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_mag, 0x2a )
        msb = self.i2c.readReg8( self.lsm9ds1_mag, 0x2b )
        data = msb << 8 | lsb
        self.m_y = data * 0.14 /1000

        lsb = self.i2c.readReg8( self.lsm9ds1_mag, 0x2c )
        msb = self.i2c.readReg8( self.lsm9ds1_mag, 0x2d )
        data = msb << 8 | lsb
        self.m_z = data * 0.14 /1000   

    def get_accel( self ):
        return( self.a_x, self.a_y, self.a_z )

    def get_gyro( self ):
        return( self.g_x, self.g_y, self.g_z )

    def get_magnet( self ):
        return( self.m_x, self.m_y, self.m_z )

