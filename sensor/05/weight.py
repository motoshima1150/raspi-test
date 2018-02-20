import wiringpi as pi
import time
from hx711 import HX711


pi.wiringPiSetupGpio()
hx = HX711(23, 24)

hx.set_reading_format("LSB", "MSB")

hx.set_reference_unit(92)

hx.reset()
hx.tare()

while True:
    val = hx.get_weight(5)
    print( "Weight:", int(val), "g")

    hx.power_down()
    hx.power_up()
    time.sleep(0.5)
