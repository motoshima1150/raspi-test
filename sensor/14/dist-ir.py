import time, wiringpi as pi

GP2Y0E03_ADDR = 0x40

pi.wiringPiSetupGpio()
i2c = pi.I2C()

gp2y0e03 = i2c.setup( GP2Y0E03_ADDR )

time.sleep(1)

while True:
    shift = i2c.readReg8( gp2y0e03, 0x35 )
    d_h = i2c.readReg8( gp2y0e03, 0x5e )
    d_l = i2c.readReg8( gp2y0e03, 0x5f )

    d = ( d_h << 4 ) + d_l
    distance = d / ( 16 * pow( 2, shift ) )

    print ("Distance:", distance , "cm" )

    time.sleep(1)
