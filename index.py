from time import sleep
from pytesseract import initCamera, detect
from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="192.168.0.10", port=502,
                 unit_id=1, auto_open=True, auto_close=True)

while(True):
    try:
        webcam = initCamera()
        print('Inicializacao OK')
        while(True):

            ler = c.read_holding_registers(200, 1)

            if(ler == [1]):
                detect(webcam)    

    except Exception as e:
        print(e)
        sleep(1)