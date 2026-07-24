from gpiozero import RotaryEncoder
from time import sleep
rotor = RotaryEncoder(23, 24, wrap=True, max_steps=18000)  # Encoder pins
while True:
     print(rotor.steps)
     sleep(0.2)
