import wiringpi as pi
import time
import numpy  # sudo apt-get python-numpy

class HX711:
    def __init__(self, dout, sck, gain=128):
        self.SCK = sck
        self.DOUT = dout

        pi.pinMode( self.SCK, pi.OUTPUT )
        pi.pinMode( self.DOUT, pi.INPUT )

        self.GAIN = 0
        self.REFERENCE_UNIT = 1
        
        self.OFFSET = 1
        self.lastVal = int(0)

        self.LSByte = [2, -1, -1]
        self.MSByte = [0, 3, 1]
        
        self.MSBit = [0, 8, 1]
        self.LSBit = [7, -1, -1]

        self.byte_range_values = self.LSByte
        self.bit_range_values = self.MSBit

        self.set_gain(gain)

        time.sleep(1)


    def is_ready(self):
        return( pi.digitalRead( self.DOUT ) == 0 )


    def set_gain(self, gain):
        if( gain is 128 ):
            self.GAIN = 1
        elif( gain is 64 ):
            self.GAIN = 3
        elif( gain is 32 ):
            self.GAIN = 2

        pi.digitalWrite( self.SCK, pi.LOW )
        self.read()


    def createBoolList(self, size=8):
        ret = []
        for i in range(size):
            ret.append(False)
        return( ret )


    def read(self):
        while not self.is_ready():
            pass

        dataBits = [self.createBoolList(), self.createBoolList(), self.createBoolList()]
        dataBytes = [0x0] * 4

        for j in range(self.byte_range_values[0], self.byte_range_values[1], self.byte_range_values[2]):
            for i in range(self.bit_range_values[0], self.bit_range_values[1], self.bit_range_values[2]):
                pi.digitalWrite( self.SCK, pi.HIGH )
                dataBits[j][i] = pi.digitalRead(self.DOUT)
                pi.digitalWrite( self.SCK, pi.LOW )
            dataBytes[j] = numpy.packbits(numpy.uint8(dataBits[j]))

        for i in range(self.GAIN):
            pi.digitalWrite( self.SCK, pi.HIGH )
            pi.digitalWrite( self.SCK, pi.LOW )

        dataBytes[2] ^= 0x80

        return( dataBytes )


    def get_binary_string(self):
        binary_format = "{0:b}"
        np_arr8 = self.read_np_arr8()
        binary_string = ""
        for i in range(4):
            binary_segment = format(np_arr8[i], '#010b')
            binary_string += binary_segment + " "
        return( binary_string )


    def get_np_arr8_string(self):
        np_arr8 = self.read_np_arr8()
        np_arr8_string = "[";
        comma = ", "
        for i in range(4):
            if( i is 3 ):
                comma = ""
            np_arr8_string += str(np_arr8[i]) + comma
        np_arr8_string += "]";
        
        return( np_arr8_string )


    def read_np_arr8(self):
        dataBytes = self.read()
        np_arr8 = numpy.uint8(dataBytes)

        return( np_arr8 )


    def read_int(self):
        np_arr8 = self.read_np_arr8()
        np_arr32 = np_arr8.view('uint32')
        self.lastVal = np_arr32

        return( int(self.lastVal) )


    def read_average(self, times=3):
        values = int(0)
        for i in range(times):
            values += self.read_int()

        return( values / times )


    def get_value(self, times=3):
        return( self.read_average(times) - self.OFFSET )


    def get_weight(self, times=3):
        value = self.get_value(times)
        value = value / self.REFERENCE_UNIT
        return( value )


    def tare(self, times=15):
        reference_unit = self.REFERENCE_UNIT
        self.set_reference_unit(1)

        value = self.read_average(times)
        self.set_offset(value)

        self.set_reference_unit(reference_unit)


    def set_reading_format(self, byte_format="LSB", bit_format="MSB"):
        if( byte_format == "LSB"):
            self.byte_range_values = self.LSByte
        elif( byte_format == "MSB"):
            self.byte_range_values = self.MSByte

        if( bit_format == "LSB"):
            self.bit_range_values = self.LSBit
        elif( bit_format == "MSB"):
            self.bit_range_values = self.MSBit


    def set_offset(self, offset):
        self.OFFSET = offset


    def set_reference_unit(self, reference_unit):
        self.REFERENCE_UNIT = reference_unit


    def power_down(self):
        pi.digitalWrite( self.SCK, pi.LOW )
        pi.digitalWrite( self.SCK, pi.HIGH )
        time.sleep(0.0001)


    def power_up(self):
        pi.digitalWrite( self.SCK, pi.LOW )
        time.sleep(0.0001)


    def reset(self):
        self.power_down()
        self.power_up()
        
        