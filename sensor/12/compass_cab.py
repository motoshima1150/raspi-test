import time, wiringpi as pi
import os, struct, math

HMC5883L_ADDR = 0x1e
scale = 0.92
scale_data = 0x01

x_max = 0
x_min = 0
y_max = 0
y_min = 0

x_cab = 0
y_cab = 0

pi.wiringPiSetupGpio()
i2c = pi.I2C()

hmc5883 = i2c.setup( HMC5883L_ADDR )

i2c.writeReg8( hmc5883, 0x00, 0x70 )
i2c.writeReg8( hmc5883, 0x01, scale_data << 5 )
i2c.writeReg8( hmc5883, 0x02, 0x00 )
time.sleep(0.006)

while True:
    while ( i2c.readReg8(hmc5883, 0x09) != 0x11 ):
        print ("Waiting")
        time.sleep(0.1)

    x_msb = i2c.readReg8( hmc5883, 0x03 )
    x_lsb = i2c.readReg8( hmc5883, 0x04 )
    x_data = ( x_msb << 8 ) + x_lsb
    if ( x_data >= 0x8000 ):
        x_data = x_data - 0x10000

    z_msb = i2c.readReg8( hmc5883, 0x05 )
    z_lsb = i2c.readReg8( hmc5883, 0x06 )
    z_data = ( z_msb << 8 ) + z_lsb
    if ( z_data >= 0x8000 ):
        z_data = z_data - 0x10000

    y_msb = i2c.readReg8( hmc5883, 0x07 )
    y_lsb = i2c.readReg8( hmc5883, 0x08 )
    y_data = ( y_msb << 8 ) + y_lsb
    if ( y_data >= 0x8000 ):
        y_data = y_data - 0x10000

        if ( x_data > x_max ):
            x_max = x_data
        if ( x_data < x_min ):
            x_min = x_data

        if ( y_data > y_max ):
            y_max = y_data
        if ( y_data < y_min ):
            y_min = y_data

        x_cab = x_max - ( x_max - x_min ) / 2
        y_cab = y_max - ( y_max - y_min ) / 2

        print ( "X Cab:" + str(x_cab) + " Y Cab:" + str(y_cab) )

    time.sleep(0.3)
    
