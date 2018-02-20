import wiringpi as pi
import time
import bme280

bme280_addr = 0x76

pi.wiringPiSetupGpio()
i2c = pi.I2C()
weather = bme280.bme280( i2c, bme280_addr )
weather.setup()

while True:
    ( temp, humi, press ) = weather.get_value()
    
    print( "Temperature:", temp ,"C  Humidity:", humi ,"%  Pressure:", press , "hPa" )
    time.sleep(1)
