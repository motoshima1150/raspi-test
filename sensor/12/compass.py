import time, wiringpi as pi
from hmc5883 import hmc5883

HMC5883L_ADDR = 0x1e
scale = 0.92
scale_data = 0x01

x_cab = 62
y_cab = -261.5

pi.wiringPiSetupGpio()
i2c = pi.I2C()

compass = hmc5883( i2c, HMC5883L_ADDR, scale, scale_data, x_cab, y_cab )



while True:
    ( x, y, z ) = compass.get_data()

    print ( "X:", x, " Y:", y, " Z:", z )

    ( x_c, y_c ) = compass.calib( x, y )
    angle = compass.angle( x_c, y_c )
    
    print ( "Degree: ", angle )

    time.sleep(1)
