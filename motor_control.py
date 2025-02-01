import serial
import time

# Replace with your Arduino's COM port (Windows: "COMX", Linux/macOS: "/dev/ttyUSB0" or "/dev/ttyACM0")
ser = serial.Serial("COM5", 9600, timeout=1)  
time.sleep(2)  # Wait for connection

def move_servo(angle):
    ser.write(f"{angle}\n".encode())  # Send angle as string
    time.sleep(0.1)  # Give time for execution
    response = ser.readline().decode().strip()  # Read response
    print("Arduino:", response)

# Test by moving the servo
for angle in range(0, 181, 30):  # Move from 0 to 180 in steps of 30
    move_servo(angle)
    time.sleep(1)

ser.close()  # Close serial connection
