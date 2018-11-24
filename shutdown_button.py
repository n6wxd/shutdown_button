#!/usr/bin/python3
# -*- coding: utf-8 -*-
# example gpiozero code that could be used to have a reboot
#  and a shutdown function on one GPIO button
# scruss - 2017-10

use_button=19                       # Switch pi pin
use_led=20                          # LED pi pin

from gpiozero import Button
from gpiozero import PWMLED
from signal import pause
from subprocess import check_call
import signal

led = PWMLED(use_led)
held_for=0.0

def rls():
    global held_for
    if (held_for > 5.0):
        check_call(['/sbin/poweroff'])
    elif (held_for > 2.0):
        check_call(['/sbin/reboot'])
    else:
        held_for = 0.0

def hld():
    global held_for
    # callback for when button is held
    # set  switch led
    if (held_for > 5.0):
        led.value = 0.2
    else:
        led.pulse
    #  is called every hold_time seconds
    # need to use max() as held_time resets to zero on last callback
    held_for = max(held_for, button.held_time + button.hold_time)

def quit():
    #led.value = 0
    logging.warning('exit')
    sys.exit(0)

def handler(signum=None, frame=None):
    quit()

# set switch led to full brightness
led.value = 1

button=Button(use_button, hold_time=1.0, hold_repeat=True)
button.when_held = hld
button.when_released = rls

signal.signal(signal.SIGTERM, handler)

pause() # wait forever
