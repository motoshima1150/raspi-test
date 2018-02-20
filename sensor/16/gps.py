import wiringpi as pi

serial_tty = "/dev/ttyS0"
serial_speed = 9600

serial = pi.serialOpen( serial_tty, serial_speed )

def dm_to_deg( data ):
    deg = int ( float(data) / 100 )
    min = float( data ) - deg * 100
    return( round( deg + min / 60.0 , 6 ) )

while(True):
    gps_line = ''
    while ( True ):
        buf = chr( pi.serialGetchar(serial) )
        if ( buf == '\r' ):
            break
        elif ( buf != '\n' ):
            gps_line = gps_line + buf
    gps_data = gps_line.split(",")
    if ( gps_data[0] == '$GPRMC' ):
        lat = gps_data[3]
        long = gps_data[5]
        
        if ( lat != "" and long != "" ):
            lat_deg = dm_to_deg( lat )
            long_deg = dm_to_deg( long )
            print ("Latitude:", lat_deg , "  Longitude:", long_deg )
        else:
            print( "Cannot catch satellite." )
            print (gps_line)


