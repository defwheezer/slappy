# slappy
Animatronic Ventriloquist Dummy ala "Slappy" from Goosebumps

[Autogenerated]
Summary
This circuit integrates a variety of components including microcontrollers (ESP32 and Raspberry Pi 3B), sensors (PIR sensor), displays (TFT LCD Display ST7735S), audio components (Stereo Jack, Audio Level Meter), actuators (Servo), and various switches and LEDs. The circuit is designed to interface between the ESP32 and Raspberry Pi 3B, with the ESP32 handling peripheral interactions such as display control and sensor readings, while the Raspberry Pi 3B serves as the central processing unit. The circuit includes power management through USB and USB-C connectors and uses XY MOS modules for power distribution to LEDs. The circuit's functionality is extended with the Arduino Pro Mini, which controls an Audio Level Meter and a Servo motor.

Component List:
ESP32 (30 pin): A microcontroller with Wi-Fi and Bluetooth capabilities, featuring a variety of digital I/O pins.

Raspberry Pi 3B: A single-board computer with GPIO pins, used as the main processing unit.

PIR sensor: A motion sensor that detects changes in infrared radiation levels.

TFT LCD Displays ST7735S: A small graphical display for user interface.

Audio Level Meter: A device that indicates the audio signal level through LED indicators.

Servo: An actuator capable of precise position control.

Stereo Jack: An audio connector for input signals.

Toggle Switches: A single-pole single-throw switch used for controlling circuit connections.

USB: Connectors for power supply and data transfer.

Arduino Pro Mini: A compact microcontroller board used for controlling the Audio Level Meter and Servo.

XY MOS: A module used for switching power lines with an external trigger.

LEDs (red, blue, white, green): Light-emitting diodes used as indicators.

Resistors (220 Ohms): Used to limit current to the LEDs.

2Pin Push Switch: A momentary switch that closes the circuit when pressed.


Wiring Details:

ESP32 (30 pin)-
D12 connected to Raspberry Pi 3B GPIO24.
GND connected to TFT LCD Display ST7735S GND and Raspberry Pi 3B GND.
D23 connected to TFT LCD Display ST7735S SDA.
D19 connected to TFT LCD Display ST7735S A0.
D18 connected to TFT LCD Display ST7735S SCK.
D5 connected to TFT LCD Display ST7735S CS.
D4 connected to TFT LCD Display ST7735S LED.
D2 connected to TFT LCD Display ST7735S CS.
3V3 connected to TFT LCD Display ST7735S Vcc.

Raspberry Pi 3B-
GPIO24 connected to ESP32 D12.
GND connected to ESP32 GND, PIR sensor GND, and XY MOS GND.
3V3 connected to 2Pin Push Switch Input + and PIR sensor VDD.
GPIO17, GPIO27, GPIO22 connected to XY MOS Trigger (3.3-25v).
GPIO25 connected to 2Pin Push Switch Output +.
GPIO23 connected to PIR sensor SIG.
GPIO18, GPIO15, GPIO14 connected to Toggle Switch spst COM.
5V connected to LED (green) cathode, Audio Level Meter Vcc (5v), and Arduino Pro Mini VCC.

PIR sensor-
GND connected to Raspberry Pi 3B GND.
VDD connected to Raspberry Pi 3B 3V3.
SIG connected to Raspberry Pi 3B GPIO23.

TFT LCD Display ST7735S-
GND connected to ESP32 GND.
SDA connected to ESP32 D23.
A0 connected to ESP32 D19.
SCK connected to ESP32 D18.
CS connected to ESP32 D5 and D2.
LED connected to ESP32 D4.
Vcc connected to ESP32 3V3.

Audio Level Meter-
Vcc (5v) connected to Raspberry Pi 3B 5V and Arduino Pro Mini VCC.
GND (power) connected to Arduino Pro Mini GND.
LED1 to LED5 connected to Arduino Pro Mini D4 to D8.
Audio IN connected to Stereo Jack Right.
Audio GND connected to Stereo Jack GND.

Servo-
pulse connected to Arduino Pro Mini D9.
gnd connected to USB GND.
vcc connected to USB 5v.

Stereo Jack-
Right connected to Audio Level Meter Audio IN.
GND connected to Audio Level Meter Audio GND.

Toggle Switches-
COM connected to Raspberry Pi 3B GPIO18, GPIO15, GPIO14.
L1 connected to Resistor pin2.

USB-
5v and GND used for power distribution to various components.

Arduino Pro Mini-
GND connected to Raspberry Pi 3B GND and Audio Level Meter GND (power).
VCC connected to Audio Level Meter Vcc (5v).
D4 to D9 connected to Audio Level Meter LED1 to LED5 and Servo pulse.

MOSFET Relays-
Trigger (3.3-25v) connected to Raspberry Pi 3B GPIO17, GPIO27, GPIO22.
GND connected to Raspberry Pi 3B GND.
Power In (GND) and Power In (5-35v) connected to USB GND and 5v.
Power Out (GND) and Power Out (V+) connected to LEDs and Resistors.
LEDs (red, blue, white, green)
cathode connected to XY MOS Power Out (GND).
anode connected to Resistor pin1.
Resistors (220 Ohms)
pin1 connected to LED anode.
pin2 connected to Toggle Switch spst L1 and XY MOS Power Out (V+).
2Pin Push Switch
Input + connected to Raspberry Pi 3B 3v3.
Output + connected to Raspberry Pi 3B GPIO25.
