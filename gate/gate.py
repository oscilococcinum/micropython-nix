import machine
from machine import Pin, Timer
import time

# Define the pins for the sensors and motor control
SENSOR_OPEN = 16  # Replace with your actual open sensor pin
SENSOR_CLOSED = 17 # Replace with your actual closed sensor pin
MOTOR_FORWARD = 2 # Forward direction (opening)
MOTOR_BACKWARD = 3 # Backward direction (closing)

# Initialize the pins
open_sensor = Pin(SENSOR_OPEN, Pin.IN, Pin.PULL_UP)
closed_sensor = Pin(SENSOR_CLOSED, Pin.IN, Pin.PULL_UP)
motor_forward = Pin(MOTOR_FORWARD, Pin.OUT)
motor_backward = Pin(MOTOR_BACKWARD, Pin.OUT)

# Motor control function
def motor_control(direction):
    if direction == "forward":
        motor_forward.value(1)
        motor_backward.value(0)
    elif direction == "backward":
        motor_forward.value(0)
        motor_backward.value(1)
    else:
        motor_forward.value(0)
        motor_backward.value(0)


# Global state variables
gate_state = None  # Possible states: 'open', 'closed', 'opening', 'closing'
request_to_interrupt = False


# Open sensor interrupt handler
def open_sensor_handler(pin):
    global gate_state, request_to_interrupt
    if gate_state == 'closing':
        motor_control('stop')
        gate_state = 'open'
        print("Gate opened due to open sensor")
    request_to_interrupt = False


# Closed sensor interrupt handler
def closed_sensor_handler(pin):
    global gate_state, request_to_intersect
    if gate_state == 'opening':
        motor_control('stop')
        gate_state = 'closed'
        print("Gate closed due to closed sensor")
    request_to_interrupt = False


# Function to handle button inputs
def control_button_handler():
    global gate_state, request_to_interrupt
    if gate_state in ('open', 'closed'):
        if gate_state == 'open':
            print("Gate is opening...")
            motor_control('forward')
            gate_state = 'opening'
        else:
            print("Gate is closing...")
            motor_control('backward')
            gate_state = 'closing'


# Function to handle interrupt request (optional)
def interrupt_request_handler():
    global request_to_interrupt, gate_state
    if gate_state in ('opening', 'closing'):
        print("Movement interrupted")
        motor_control('stop')
        gate_state = None  # Or set to 'stopped' state


# Set up sensor interrupts
open_sensor.irq(trigger=Pin.IRQ_FALLING, handler=open_sensor_handler)
closed_sensor.irq(trigger=Pin.IRQ_FALLING, handler=closed_sensor_handler)

# Main loop for handling inputs and controlling the gate
while True:
    try:
        # Wait for input to control the gate (you can modify this part based on your input method)
        input("Press Enter to control the gate or Ctrl+C to exit... ")

        if gate_state is None:
            print("Gate is not in a known state. Please reset.")
            continue

        if gate_state == 'open':
            print("Gate is currently open")
        elif gate_state == 'closed':
            print("Gate is currently closed")
        else:
            print(f"Gate is {gate_state}")

        # Control the gate based on current state
        if gate_state in ('open', 'closed'):
            control_button_handler()
        else:
            print("Gate is already moving or in an unknown state")

    except KeyboardInterrupt:
        print("\nExiting program...")
        motor_control('stop')
        break

print("Program exited")
