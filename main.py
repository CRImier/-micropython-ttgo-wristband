from hw import *
import esp
from time import sleep, time
import machine

start_time = time()

machine.freq(80*1000*1000)
esp.osdebug(None)

import wifi
wifi.default_setup()
wifi.connect()

def scan_i2c():
    print([hex(i) for i in i2c.scan()])

run_time = 60
print(reset_cause_hr())

#scan_i2c()

def get_ip():
    import urequests as requests
    r = requests.get("http://icanhazip.com")
    return r.text.strip()

def read_touch():
    while True:
        print(touch.value())
        sleep(0.1)

def deepsleep(*args):
    import esp32
    esp32.wake_on_ext0(pin=touch, level=esp32.WAKEUP_ANY_HIGH)
    # for deepsleep testing with the breakout
    # esp32.wake_on_ext1(pins=(Pin(14, Pin.IN, Pin.PULL_DOWN), touch), level=esp32.WAKEUP_ANY_HIGH)
    deinit_hw_for_deepsleep()
    print("Sleeping")
    machine.deepsleep(*args)

print(time())
init_all_hw() # touch is initialized here
# however, touchpad will not be recognized as "held" from when the touchpad IC is powered on
led.value(is_charging())

red = color565(255, 0, 0)
blue = color565(0, 0, 255)
green = color565(0, 255, 0)
black = color565(0, 0, 0)
cyan = color565(0x60, 0xd0, 0xf0)
pink = color565(0xf0, 0xb0, 0xc0)
white = color565(0xff, 0xff, 0xff)

lcd.fill(black)
lcd_bl.on()

if gp0.value() == 0:
    print("Ampy")
    lcd.fill(green)
    lcd.text("Ampy", 80-16, 40-4, color=red, background=green)
    raise Exception # stopping main.py execution here in case something is wrong with deepsleep or smth

"""
lcd.fill(red)

colors = (0, green, blue, green|blue, red|blue, red|green|blue)

for i in range(80/5):
    lcd.pixel(i*10, i*5, colors[(i+0)%len(colors)])

lcd.fill_rectangle(10, 15, 20, 30, green|red)
lcd.fill_rectangle(30, 45, 20, 30, blue|red)
"""


lcd.text("Hello world!", 0, 0, color=cyan)
lcd.text(" ".join([hex(i) for i in i2c.scan()]), 0, 10, color=pink)
lcd.text("Going to sleep in", 0, 30, color=pink)
lcd.text("3 seconds!", 0, 40, color=cyan)

for i in range(4):
    voltage_texts = battery_voltage(str=True) + "Vb " + charging_voltage(str=True) + "Vc"
    lcd.text(voltage_texts, 0, 20, color=white)
    lcd.text(str(2-i//2)+" seconds!", 0, 40, color=cyan)
    if i == 0: vibro.on()
    sleep(0.5)
    if i == 0: vibro.off()

time_before_sleep = time()
time_spent = time_before_sleep-start_time
time_to_sleep = run_time-time_spent
print("Going to sleep for {} seconds".format(time_to_sleep), time_before_sleep, time_spent)
sleep(1)
deepsleep(time_to_sleep*1000)

