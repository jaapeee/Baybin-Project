import RPi.GPIO as GPIO
import time
from gpiozero import AngularServo
import baybin as bay
import threading
#from hx711 import HX711
import pyrebase

config = {
    "apiKey": "AIzaSyAlnnZo7Lm2lMDVzFjOUsovZL9cfpeFEVY",
    "authDomain": "baybin-project.firebaseapp.com",
    "databaseURL": "https://baybin-project-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "baybin-project",
    "storageBucket": "baybin-project.appspot.com",
    "messagingSenderId": "25254133300",
    "appId": "1:25254133300:web:411a031c53deb9dec59461",
    "measurementId": "G-WXEEG63GZ9"
};

firebase = pyrebase.initialize_app(config)
database = firebase.database()

#setup pins
#stepper motors
step_pin1 = 12
dir_pin1 = 6
step_pin2 = 13
dir_pin2 = 16
step_pin3 = 18
dir_pin3 = 17
#main pump
main_pump = 27
#electromagnetic rod
magnet = 7
#submersible pumps
sub_pump1 = 22
sub_pump2 = 23
sub_pump3 = 21
#servo motors
servo1 = 20
#load cells
#load_cell_dpin1 = 24
#load_cell_spin1 = 25
#load_cell_dpin2 = 5
#load_cell_spin2 = 26
#ultrasonic sensors
echo_pin1 = 24
trig_pin1 = 25
echo_pin2 = 5
trig_pin2 = 26
#buzzer
buzz_pin = 4


#Setup GPIO
GPIO.setmode(GPIO.BCM)
#for stepper motors
GPIO.setup(step_pin1, GPIO.OUT)
GPIO.setup(dir_pin1, GPIO.OUT)
GPIO.setup(step_pin2, GPIO.OUT)
GPIO.setup(dir_pin2, GPIO.OUT)
GPIO.setup(step_pin3, GPIO.OUT)
GPIO.setup(dir_pin3, GPIO.OUT)
#for main pump
GPIO.setup(main_pump, GPIO.OUT)
#for electromagnetic rod
GPIO.setup(magnet, GPIO.OUT)
#for submersible pumps
GPIO.setup(sub_pump1, GPIO.OUT)
GPIO.setup(sub_pump2, GPIO.OUT)
GPIO.setup(sub_pump3, GPIO.OUT)
#for servo motors
GPIO.setup(servo1, GPIO.OUT)
#for load cells
#GPIO.setup(load_cell_dpin1, GPIO.OUT)
#GPIO.setup(load_cell_spin1, GPIO.OUT)
#GPIO.setup(load_cell_dpin2, GPIO.OUT)
#GPIO.setup(load_cell_spin2, GPIO.OUT)
#for ultrasonic sensors
GPIO.setup(trig_pin1,GPIO.OUT)
GPIO.setup(echo_pin1,GPIO.IN)
GPIO.setup(trig_pin2,GPIO.OUT)
GPIO.setup(echo_pin2,GPIO.IN)
#buzzer
GPIO.setup(buzz_pin, GPIO.OUT)

#def iron_oxide():
#    hx = HX711(dout_pin = load_cell_dpin1, pd_sck_pin = load_cell_spin1)
#    hx.zero()
#    reading = hx.get_raw_data_mean()
#    read_percentage = reading / 75000 * 70 + 30
    
#    return read_percentage
    
#    database.child("oxide_level").set(read_percentage)
            
#def vegetable_oil():
#    hx = HX711(dout_pin = load_cell_dpin2, pd_sck_pin = load_cell_spin2)
#    hx.zero()
#    reading = hx.get_raw_data_mean()
#    read_percentage = reading / 75000 * 70 + 30

#    return read_percentage
            
#    database.child("oil_level").set(read_percentage)
            
    
def water_level():
    while True:
        print ("distance measurement in progress")
        GPIO.setup(trig_pin1,GPIO.OUT)
        GPIO.setup(echo_pin1,GPIO.IN)
        GPIO.output(trig_pin1,False)
        print ("waiting for sensor to settle")
        time.sleep(0.2)
        GPIO.output(trig_pin1,True)
        time.sleep(0.00001)
        GPIO.output(trig_pin1,False)
        while GPIO.input(echo_pin1)==0:
            pulse_start=time.time()
        while GPIO.input(echo_pin1)==1:
            pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        percentage=distance/30.5*100
        invert_percentage=100-percentage+20
        mod_percentage = int(invert_percentage)
        if invert_percentage >= 80:
            print("Water is overflowing")
            print("")
            GPIO.output(buzz_pin, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(buzz_pin, GPIO.LOW)
            time.sleep(2)
        else:
            print ("water content:",int(invert_percentage),"%")
            print("")
            time.sleep(2)
        database.child("water_content").set(mod_percentage)
            
def seabin_level():
    waste_daily = 24 * 60 * 60
    total_daily = 0
    while True:
        print ("distance measurement in progress")
        GPIO.setup(trig_pin2,GPIO.OUT)
        GPIO.setup(echo_pin2,GPIO.IN)
        GPIO.output(trig_pin2,False)
        print ("waiting for sensor to settle")
        time.sleep(0.2)
        GPIO.output(trig_pin2,True)
        time.sleep(0.00001)
        GPIO.output(trig_pin2,False)
        while GPIO.input(echo_pin2)==0:
            pulse_start=time.time()
        while GPIO.input(echo_pin2)==1:
            pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        percentage=distance/30.5*100
        invert_percentage=100-percentage-1
        mod_distance = int(distance)
        mod_percentage = int(invert_percentage)
        #for baybin content
        if invert_percentage >= 60:
            print("Full of garbage")
            print("")
            GPIO.output(buzz_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzz_pin, GPIO.LOW)
            time.sleep(1)
        else:
            print("baybin content:",int(invert_percentage),"%")
            print("")
            time.sleep(1)
        database.child("baybin_content").set(mod_percentage)
        database.child("distance_content").set(mod_distance)
        #data gathering for waste collection
        
def waste_per_hour():
    get_data = database.child("distance_content").get()
    count = 0
    total_per_hour = 0
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= count:
            print(f"Waste Collected: {total_per_hour}")
            count += 1
            total_per_hour += get_data.val()
        time.sleep(3600)
        database.child("waste_collected_per_hour").set(total_per_hour)

def waste_daily():
    get_data = database.child("distance_content").get()
    count = 0
    total_daily = 0
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= count:
            print(f"Waste Collected: {total_daily}")
            count += 1
            total_daily += get_data.val()
        time.sleep(86400)
        database.child("daily_waste_collected").set(total_daily)
    
def main1():
    count = 0
    while True:
        #turn off relay for initial output
        GPIO.output(main_pump, GPIO.HIGH)
        GPIO.output(magnet, GPIO.HIGH)
        GPIO.output(sub_pump1, GPIO.HIGH)
        GPIO.output(sub_pump2, GPIO.HIGH)
        GPIO.output(sub_pump3, GPIO.HIGH)
        time.sleep(1)
        #run pump function
        bay.m_pump(main_pump)
        #pours iron oxide and vegetable oil
        bay.servo_motor(servo1)
        bay.submersible_pump(sub_pump3)
        #stirs the unfiltered water
        bay.submersible_pump(sub_pump1)
        #turn on electromagnet
        GPIO.output(magnet, GPIO.LOW)
        #control electromagnet position | step pin, dir pin, steps, direction, delay
        bay.stepper_motor(step_pin1, dir_pin1, 700, 0, 0.001)
        time.sleep(2)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        time.sleep(2)
        bay.stepper_motor(step_pin1, dir_pin1, 700, 1, 0.001)
        time.sleep(.5)
        bay.stepper_motor(step_pin2, dir_pin2, 20, 0, 0.095)
        time.sleep(.5)
        bay.stepper_motor(step_pin1, dir_pin1, 700, 0, 0.001)
        GPIO.output(magnet, GPIO.HIGH)#turn off electromagnet
        time.sleep(1)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 1, 0.001)
        bay.stepper_motor(step_pin1, dir_pin1, 150, 0, 0.001)
        time.sleep(2)
        bay.stepper_motor(step_pin1, dir_pin1, 700, 1, 0.001)
        time.sleep(.5)
        bay.stepper_motor(step_pin2, dir_pin2, 20, 1, 0.095)
        time.sleep(2)
        #drains the filtered water
        bay.submersible_pump(sub_pump2)
        #chill muna 15 seconds
        time.sleep(15)
        count += 1
        print("Cycles done: ",count)
        database.child("no_of_cycles").set(count)


#Create threads
thread_main = threading.Thread(target = main1)
thread_water = threading.Thread(target = water_level)
thread_seabin = threading.Thread(target = seabin_level)
thread_waste_hourly = threading.Thread(target = waste_per_hour)
thread_waste_daily = threading.Thread(target = waste_daily)
#thread_iron = threading.Thread(target = iron_oxide)
#thread_vegetable = threading.Thread(target = vegetable_oil)


try:
    thread_main.start()
    #thread_iron.start()
    #thread_vegetable.start()
    thread_water.start()
    thread_seabin.start()
    thread_waste_hourly.start()
    thread_waste_daily.start()

except KeyboardInterrupt:
     GPIO.cleanup()