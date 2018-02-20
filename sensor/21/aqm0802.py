import time, wiringpi as pi
import RPi.GPIO as GPIO

class aqm0802:
    def __init__(self, i2c, ad ):
        self.ad = ad
        self.cursol = 1
        self.blink = 1
        self.display = 1
        self.x = 0
        self.y = 0
        self.ledpin = 4
        self.i2c = i2c
        
        self.so = self.i2c.setup( self.ad )
        
        time.sleep(0.1)
        self.i2c.writeReg8( self.so, 0x00, 0x38 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x39 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x14 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x70 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x56 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x6c )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x38 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x06 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x0c )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x01 )
        time.sleep(0.03)
        self.i2c.writeReg8( self.so, 0x00, 0x02 )
        time.sleep(0.03)
        
        pi.pinMode( self.ledpin, pi.OUTPUT )
        
    def clear(self):
        self.i2c.writeReg8( self.so, 0x00, 0x01)
        time.sleep(0.1)       

    def set_display(self):
        buf = 0x08 + 0x04 * self.display + 0x02 * self.cursol + self.blink
        self.i2c.writeReg8( self.so, 0x00, buf)
        time.sleep(0.1)
        
    def set_cursol(self, buf):
        if buf != 0:
            buf = 1
        self.cursol = buf
        self.set_display( )

    def set_blink(self, buf):
        if buf != 0:
            buf = 1
        self.blink = buf
        self.set_display()

    def move_home(self):
        self.x = 0
        self.y = 0
        self.i2c.writeReg8( self.so, 0x00, 0x02 )
        time.sleep(0.1)

    def move(self, mx, my):    
        self.x = mx
        self.y = my
        if self.x < 0:
            self.x=0
        if self.x > 0x07:
            self.x=0x07
        if self.y < 0:
            self.y=0
        if self.y > 1:
            self.y=1
        oy = self.y * 0x40
        out = self.x + oy + 0x80
        self.i2c.writeReg8( self.so, 0x00, out )
        time.sleep( 0.1 )

    def write(self, buf):
        length = len(buf)
        i = 0
        while i < length:
            if self.x > 0x0f:
                if self.y == 0:
                    self.move( 0x00, 0x01 )
                else:
                    break
            out = ord( buf[i] )
            self.i2c.writeReg8( self.so, 0x40, out)

            self.x = self.x + 1
            i = i + 1

    def backlight(self, onoff):
        if ( onoff == 0 ):
            pi.digitalWrite( self.ledpin, pi.LOW )
        else:
            pi.digitalWrite( self.ledpin, pi.HIGH )


