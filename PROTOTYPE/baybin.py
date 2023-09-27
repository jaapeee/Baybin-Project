import RPi.GPIO as GPIO
from gpiozero import AngularServo
#from hx711 import HX711
from time import sleep


#stepper motor function putangina
def stepper_motor(step_pin, dir_pin, steps, direction, delay):
	GPIO.output(dir_pin, direction)
	for x in range(steps):
		GPIO.output(step_pin, GPIO.HIGH)
		sleep(delay)
		GPIO.output(step_pin, GPIO.LOW)
		sleep(delay)

#water pump function
def m_pump(pin):
	#turns on pump to do shit
	GPIO.output(pin, GPIO.LOW)
	sleep(5)#runs for 30 seconds
	GPIO.output(pin, GPIO.HIGH)
	sleep(2)

#servo motor function
def servo_motor(pin):
	#servo pulse/hz and pin setup
	servo = AngularServo(pin, min_pulse_width=0.0006, max_pulse_width=0.0023)

	#initiate servo
	servo.angle = 90
	sleep(3)
	servo.angle = -90
	sleep(2)

#submersible pump function
def submersible_pump(pin):
	GPIO.output(pin, GPIO.LOW)
	sleep(5)
	GPIO.output(pin, GPIO.HIGH)
	sleep(2)
	

def water_level(trig_pin, echo_pin):
    while True:
        print ("Distance measurement in progress")
        GPIO.setup(trig_pin,GPIO.OUT)
        GPIO.setup(echo_pin,GPIO.IN)
        GPIO.output(trig_pin,False)
        print ("Waiting for sensor to settle")
        time.sleep(0.2)
        GPIO.output(trig_pin,True)
        time.sleep(0.00001)
        GPIO.output(trig_pin,False)
        while GPIO.input(echo_pin)==0:
            pulse_start=time.time()
        while GPIO.input(echo_pin)==1:
            pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        percentage=distance/30.5*100
        invert_percentage=100-percentage+20
        print ("Content:",int(invert_percentage),"%")
        time.sleep(2)

#load cell function
def load_cell(data_pin, serial_pin, container_cont):
	hx = HX711(dout_pin = data_pin, pd_sck_pin = serial_pin)

	hx.zero()

	while True:
		reading = hx.get_raw_data_mean()

		if reading <= 5:
			print("Low ", container_cont, "/nRefill Now!")

		else:
			print(reading)

