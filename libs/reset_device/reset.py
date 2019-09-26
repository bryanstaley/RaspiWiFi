import RPi.GPIO as GPIO
import os
import time
import subprocess
import reset_lib


SEEED_BUTTON_GPIO=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SEEED_BUTTON_GPIO, GPIO.IN)

counter = 0
serial_last_four = subprocess.check_output(['cat', '/proc/cpuinfo'])[-5:-1].decode('utf-8')
config_hash = reset_lib.config_file_hash()
ssid_prefix = config_hash['ssid_prefix'] + " "
reboot_required = False


reboot_required = reset_lib.wpa_check_activate(config_hash['wpa_enabled'], config_hash['wpa_key'])

reboot_required = reset_lib.update_ssid(ssid_prefix, serial_last_four)

if reboot_required == True:
    os.system('reboot')

while True:
    if GPIO.input(SEEED_BUTTON_GPIO):
        counter=0
    else:
        counter+=1
    if counter >= 9:
        reset_lib.reset_to_host_mode()
    time.sleep(1)
