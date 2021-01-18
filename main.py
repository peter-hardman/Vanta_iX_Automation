import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM) #Set Board to BCM mode
GPIO.setwarnings(False)

# Inputs/Outputs(Sensors)
out1 = 26
ready_in =19
fault_in= 13

GPIO.setup(out1, GPIO.OUT) #Output 1

GPIO.setup(ready_in, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Ready input. 
GPIO.setup(fault_in, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Fault input.

def send_start_signal():
    print ("sending start ", end="")
    GPIO.output(out1, 1)
    time.sleep(1.0)
    #print ("Turning off")
    GPIO.output(out1, 0)

def test_code():
    while(1):
        time.sleep(1)
        now =datetime.datetime.now()
        timestr=now.strftime("%b %d %Y %H:%M:%S")
        
        if GPIO.input(ready_in):
            print(timestr+" ready")
        else:
            print(timestr+" not_ready")
        if GPIO.input(fault_in):
            print("fault")
            
        

def main():
    test_count = 0
    loop_count = 0
    test_time  = 0
    starting_count =0
    
#    test_code()
    
    while (1):
        time.sleep(0.1)
        
        if (GPIO.input(ready_in) or GPIO.input(fault_in)):
            loop_count = 0
            
            if (GPIO.input(fault_in)):
                print ("Fault detected!")
            if (GPIO.input(ready_in)):
                print ("System Ready")
                
            send_start_signal()
            
            print("waiting for test to start")
            while (GPIO.input(ready_in)):
            #    print(".",end="")
                time.sleep(0.1)
                starting_count = starting_count+1
                if (starting_count>10):
                    break
                   
            if (GPIO.input(ready_in) == 0):
                print("test started")
                test_count +=1
                time.sleep(1.0)  #wait for test to have time to start.
            
            print("waiting for test to finish")
            while (GPIO.input(ready_in) == 0):
                if (test_time>0):
                    if loop_count >( test_time+10):
                        print ("Test time exceeded!")
                        break;
                if (GPIO.input(fault_in)):
                    print ("Fault detected!")
                    break;
                # print(".",end="") 
                time.sleep(0.1)
                loop_count = loop_count +1
            print(".")        
            print ("test %i completed in %i cycles" % (test_count,loop_count))
            if (test_time == 0):
                test_time = loop_count
                print ("First test took %i loops to run" % test_time)
                
            time.sleep(1)

if __name__ == "__main__":
    main()