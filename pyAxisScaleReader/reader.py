import serial
from datetime import datetime
from time import sleep, time
import sys

port = sys.argv[1]#'/dev/ttyUSB0'
bound=9600
file=sys.argv[2] #"/tmp/mass.csv"

with open(file, 'a') as fp:

    ser=serial.Serial(
        port=port,
        baudrate=bound,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    #ser.open()
    dt = 1.
    ts = time()
    while(True):
        #print(time() - ts)
        try:
            if (time() - ts > dt):
                ts = time()
                ser.write(str.encode(str('Sx1\r\n')))

                data = ser.read(16)
                data_decoded = data.decode("utf-8") 
                data_float = float(data[:10].decode("utf-8"))
                tm = datetime.fromtimestamp(ts).isoformat()
                print(f'{tm};{data_float}', file=fp)
                print(f'{tm};{data_float}')
                fp.flush()
            else:
                st = (dt - (time() - ts))*0.9
                if st > 0:
                    sleep()
        except:
            pass
    ser.close()