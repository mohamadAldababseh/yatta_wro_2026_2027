import time
import cv2
import numpy as np
from WebcamVideoStream import WebcamVideoStream as ws
from MyGyro import BNO085 as BN
from MyUltrasonic import UltrasonicSensor
from gpiozero import RotaryEncoder
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BCM)

btn = 6
GPIO.setup(btn, GPIO.IN)

ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.flush()
time.sleep(2)

rotor = RotaryEncoder(19, 13, wrap=True, max_steps=18000)
rotor.steps = 0

min_angle = 30
mid_angle = 90
max_angle = 130

front_sensor = UltrasonicSensor(trig=23, echo=24)
back_sensor  = UltrasonicSensor(trig=25, echo=8)
left_sensor  = UltrasonicSensor(trig=7,  echo=1)
right_sensor = UltrasonicSensor(trig=12, echo=16)

imu = BN()
imu.start()

cam = ws()
cam.start()

Kp, Ki, Kd = 0.5, 0.0, 0.1
integral = 0
last_error = 0

def send_command(code):
    ser.write((code + "$").encode("utf-8"))

def stop():
    send_command("s:")

def set_servo_angle(angle):
    send_command(f"a:{angle}")

def forward(speed, target_angle):
    dist_front = front_sensor.distance()
    dist_left  = left_sensor.distance()
    dist_right = right_sensor.distance()
    if dist_front < 20 or dist_left < 10 or dist_right < 10:
        stop()
        print("blocked forward")
        return
    yaw = imu.Read_Yaw()
    if yaw != "err":
        error = ((target_angle - yaw + 180) % 360) - 180
        global integral, last_error
        integral += error
        derivative = error - last_error
        last_error = error
        output = Kp*error + Ki*integral + Kd*derivative
        servo_angle = mid_angle + output
        servo_angle = max(min_angle, min(max_angle, servo_angle))
        set_servo_angle(int(servo_angle))
    send_command(f"f:{speed}")

def backward(speed):
    dist = back_sensor.distance()
    if dist < 20:
        stop()
        print("blocked back")
        return
    set_servo_angle(mid_angle)
    send_command(f"b:{speed}")

def go_left(speed):
    dist = left_sensor.distance()
    if dist < 20:
        stop()
        print("blocked left")
        return
    set_servo_angle(min_angle)
    send_command(f"f:{speed}")

def go_right(speed):
    dist = right_sensor.distance()
    if dist < 20:
        stop()
        print("blocked right")
        return
    set_servo_angle(max_angle)
    send_command(f"f:{speed}")

def detect_lines(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    orange_lower = np.array([5, 100, 100], np.uint8)
    orange_upper = np.array([20, 255, 255], np.uint8)
    blue_lower = np.array([100, 150, 0], np.uint8)
    blue_upper = np.array([140, 255, 255], np.uint8)
    mask_orange = cv2.inRange(hsv, orange_lower, orange_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    if cv2.countNonZero(mask_orange) > 200:
        return "orange"
    if cv2.countNonZero(mask_blue) > 200:
        return "blue"
    return None

laps = 0
side = 0
while True:
    if not GPIO.input(btn):
        time.sleep(1)
        heading = imu.Read_Yaw()
        while heading == 'err':
            heading = imu.Read_Yaw()
        print("start heading", heading)

        while laps < 3:
            frame = cam.read()
            line = detect_lines(frame)
            forward(150, heading)
            if line == "orange" or line == "blue":
                print("line detected", line, "side", side)
                stop()
                time.sleep(1)
                go_left(150)
                time.sleep(1)
                stop()
                heading = (heading + 90) % 360
                side += 1
                if side == 4:
                    side = 0
                    laps += 1
                    print("lap finished", laps)
        stop()
        print("finished 3 laps")
        break
