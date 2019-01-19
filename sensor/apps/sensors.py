import time

class Sensors:
    def __init__(self):
        pass
    def helper_DS18B20(self, phys_addr):
        f = open(phys_addr, 'r')
        lines = f.readlines()
        f.close()
        return lines
    def DS18B20(self, phys_addr):
        temp = 0.0
        alert = [18.0, 30.0]
        alert_logic = False

        lines = self.helper_DS18B20(phys_addr)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.helper_DS18B20()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
        if temp <= alert[0] or temp >= alert[1]:
            alert_logic = True
        return [temp, alert_logic]
