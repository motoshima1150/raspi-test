import wiringpi as pi
import time
from lsm9ds1 import lsm9ds1

gyro_addr = 0x6b
magnet_addr = 0x1e


pi.wiringPiSetupGpio()
i2c = pi.I2C()
motion = lsm9ds1( i2c, gyro_addr, magnet_addr )

while True:
    motion.read_sensor()
    ( g_x, g_y, g_z ) = motion.get_gyro()
    print( "Gyro X:", g_x, " Y:", g_y, " Z:",g_z )

    ( a_x, a_y, a_z ) = motion.get_accel()
    print( "Accel X:", a_x, " Y:", a_y, " Z:",a_z )

    ( m_x, m_y, m_z ) = motion.get_magnet()
    print( "Magnet X:", m_x, " Y:", m_y, " Z:",m_z )

    time.sleep(1)
