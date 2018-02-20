import time
import threading
from mcp3204 import mcp3204

class pulse_sensor:
    def __init__( self, channel, ce, spi_speed, adc_vref ):
        self.channel = channel
        self.ce = ce
        self.spi_speed = spi_speed
        self.adc_vref = adc_vref
        self.BPM = 0
        
        self.adc = mcp3204( self.ce, self.spi_speed, self.adc_vref )

    def getBPMLoop( self ):
        rate = [0] * 10
        sampleCounter = 0
        lastBeatTime = 0
        P = 512
        T = 512
        thresh = 525
        amp = 100
        firstBeat = True
        secondBeat = False

        IBI = 600
        Pulse = False
        lastTime = int( time.time() * 1000 )
        
        while not self.thread.stopped:
            Signal = int( self.adc.get_value( self.channel) / 4 )
            currentTime = int( time.time() * 1000 )
            
            sampleCounter = sampleCounter + currentTime - lastTime
            lastTime = currentTime
            
            N = sampleCounter - lastBeatTime

            if( Signal < thresh and N > ( IBI / 5.0 ) * 3 ):
                if( Signal < T ):
                    T = Signal

            if( Signal > thresh and Signal > P ):
                P = Signal

            if( N > 250 ):
                if( Signal > thresh and Pulse == False and N > ( IBI / 5.0 ) * 3 ):       
                    Pulse = True
                    IBI = sampleCounter - lastBeatTime
                    lastBeatTime = sampleCounter

                    if( secondBeat ):
                        secondBeat = False;
                        for i in range( len( rate ) ):
                          rate[i] = IBI

                    if( firstBeat ):
                        firstBeat = False
                        secondBeat = True
                        continue

                    rate[:-1] = rate[1:]
                    rate[-1] = IBI
                    runningTotal = sum( rate )

                    runningTotal = runningTotal / len( rate )
                    self.BPM = 60000 / runningTotal

            if( Signal < thresh and Pulse == True ):
                Pulse = False
                amp = P - T
                thresh = amp / 2 + T
                P = thresh
                T = thresh

            if( N > 2500 ):
                thresh = 512
                P = 512
                T = 512
                lastBeatTime = sampleCounter
                firstBeat = True
                secondBeat = False
                self.BPM = 0

            time.sleep( 0.005 )
            
        
    def startAsyncBPM( self ):
        self.thread = threading.Thread( target = self.getBPMLoop )
        self.thread.stopped = False
        self.thread.start()
        return
        
    def stopAsyncBPM( self ):
        self.thread.stopped = True
        self.BPM = 0
        return
