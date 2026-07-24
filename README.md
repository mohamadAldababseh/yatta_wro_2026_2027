Engineering materials
This repository contains engineering materials of yatta team 2027 self-driven vehicle's model participating in the WRO Future Engineers 
competition in the season 2026-2027.

Content
photos contains photos of the teamand the vehicle

video contains the video.md file with the link to a video where driving demonstration exists

schemes contains diagrams about the design and cricut

codes contains the source code that is used

chasis contains photos of the used chasis and its parts

3d contains the models we print for our project

As of this commit it only contains the source.

Software
We are using the Raspberry Pi as the main controller. We also use the Arduino ATmega328p to read the ultrasonic sensors, 
filter the readings, and send them through the serial connection to the Raspberry Pi.

Code basic idea
We took advantage of the Raspberry Pi ability to run multiple processes at the same time, so we divided the main program
into separate threads.

Main-thread
The main thread runs all other threads while waiting for the gyroscope to calibrate. After calibration, the main thread
waits for a button click. When the button is clicked, the main thread starts the car movement by calling the moving and 
turning functions when needed.

Gyro-thread
In the gyro thread we calibrate the BNO085 sensor and set the current angle to zero. Then the thread keeps running and
updating the yaw angle continuously. This thread blocks the main thread until calibration is finished.

Distance-thread
In the distance thread we read the ultrasonic sensors continuously. The Arduino collects the readings and sends them to
the Raspberry Pi, which updates the distances. This thread ensures the robot avoids collisions with walls by checking 
front, back, left, and right distances.

Color-thread
In the color thread we process frames from the fisheye camera using OpenCV. We detect orange and blue lines on the track.
Orange indicates one type of turn, blue indicates the opposite. If neither is found, the robot decides based on left and right distances from ultrasonic sensors.

Turning
The robot uses ultrasonic sensors to check distances and the gyroscope to measure the current angle. When a line is detected,
the robot stops, then turns 90 degrees in the correct direction. The PID controller ensures the turn is accurate.

Avoiding walls
The robot calculates distance errors from left and right ultrasonic sensors. These errors are combined with the yaw error
from the gyroscope. The PID algorithm adjusts the servo angle to keep the robot centered between the walls while moving straight.

3 laps detection
The robot completes three full laps around the square track. Each edge of the track is handled with a dedicated function.
The end of an edge is detected by the orange or blue line on the floor. After three laps, the robot stops at the starting square.
