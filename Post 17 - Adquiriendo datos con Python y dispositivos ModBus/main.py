from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from stepTHconf import step_th
import numpy as np
import struct
from mysqlConnect import insertQuery

method = step_th()['default_config']['method']
stopbits = step_th()['default_config']['stopbits']
bytesize = step_th()['default_config']['bytesize']
parity = step_th()['default_config']['parity']
baudrate = step_th()['default_config']['baudrate']
timeout = step_th()['default_config']['timeout']
nper = step_th()['default_config']['nper']
port = '/dev/ttyUSB0'

client = ModbusClient(method=method,
                      stopbits=stopbits,
                      bytesize=bytesize,
                      parity=parity,
                      baudrate=baudrate,
                      timeout=timeout,
                      port=port)

connection = client.connect()

if connection:
    #Leemos los valores de los registros tipo integer
    #correspondientes a la configuración de la sonda
    print("memo_Integers values")
    for key, value in step_th()['memo_Integers'].items():
        rr = client.read_holding_registers(value, 1, unit=0x01)
        if not rr.isError():
            val = rr.registers[0]
            print('{}: {}'.format(key, val))
        else:
            print('{}: error'.format(key))
    
    #Leemos los valores de los registros tipo float
    #correspondientes a las medidas de la sonda
    print("memo_floats values")
    measure_names=[]
    values=[]
    for key, value in sorted(step_th()['memo_Floats'].items()):
        rr1 = client.read_holding_registers(value, 1, unit=0x01)
        rr2 = client.read_holding_registers(value, 2, unit=0x01)
        if not rr1.isError() and not rr2.isError():
            print('{}: {};{}'.format(key, rr1.registers[0], rr2.registers[0]))
            bin_number = '0' + str(np.base_repr(rr2.registers[0], base=2)) \
                         + '0' + str(np.base_repr(rr1.registers[0], base=2))
            f = int(bin_number, 2)
            value = round(struct.unpack('f', struct.pack('I', f))[0], 1)
            print("#"*20)
            print('{}:{}'.format(key, struct.unpack('f', struct.pack('I', f))[0]))
            print('#'*20)
            values.append(value)
            measure_names.append(key)
        else:
            print('{}: error'.format(key))

    client.close()

#Guardamos los valores en la base de datos
insertQuery(values)