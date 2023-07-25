HighFlowRate = 3 # ml / hr
LowFlowRate = 1 # ml / hr


HighFlowRateTime = 5 # sec
LowFlowRateTime = 5 # sec

PumpPort = '/dev/ttyUSB0'
OutFile = 'PumpingLog.csv'

###############################
### DO NOT EDIT BELOW THIS LINE
###############################


import serial
from datetime import datetime
from time import sleep, time

with serial.Serial(PumpPort, 19200) as ser:


    def spc(ser, cmd):
        
        ser.write(('0'+cmd+'\x0D').encode())
        
        sleep(0.5)

        out = ser.read_all()
        
        return out.decode()
    # check connection

    spc(ser, 'ADR')
    if spc(ser, 'STP')[3] != 'S':
        print('Unable to control pump [0]')


    def RunFlowRate(ser, fp, fl,tim):
        ts = datetime.fromtimestamp(time()).isoformat()
        
        if spc(ser, 'STP')[3] not in  ['S', 'P']:
            print('Unable to control pump [1]')

        out = spc(ser,'DIS')
        vols = float(out[5:10])


        spc(ser,'RAT'+str(fl)+'MH*')
        out = spc(ser,'RAT')
        
        if float(out[4:-3]) != fl:
            print('Unable to control pump [2]', out)

        if spc(ser, 'RUN')[3] != 'I':
            print('Unable to control pump [3]')
        
        sleep(tim)

        te = datetime.fromtimestamp(time()).isoformat()
        out = spc(ser,'DIS')
        vole = float(out[5:10])

        print(f'{ts};{te};{fl};{tim};{vols};{vole}', file=fp)
        print(f'{ts};{te};{fl};{tim};{vols};{vole}')
        print(f'Injected already {vole} ml')
    with open(OutFile, 'a') as fp:
        for i in range(1):
            print(f'Setting rate to {HighFlowRate} for {HighFlowRateTime} seconds')
            RunFlowRate(ser,fp, HighFlowRate, HighFlowRateTime)

            print(f'Setting rate to {LowFlowRate} for {LowFlowRateTime} seconds')
            RunFlowRate(ser,fp, LowFlowRate, LowFlowRateTime)

        if spc(ser, 'STP')[3] not in  ['S', 'P']:
            print('Unable to sop pump!!')







