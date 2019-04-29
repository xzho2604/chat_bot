import RPi.GPIO as GPIO
from time import sleep
import time
from flask import Flask
from flask import jsonify
from flask import request

#set pin 3 as output pin to control the servo
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
pwm=GPIO.PWM(3,50)


# will rote for the angle specified
def SetAngle(angle):
    duty = angle/ 18 + 2
    GPIO.output(3,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)




#GPIO.cleanup()
#pwm.stop()
#start a server and listent to the incomming reqest


app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    print("get request")

    pwm.start(0)

    SetAngle(180)
    SetAngle(180)


    return jsonify({'message' : 'Dog Feeded'})


if __name__ == '__main__':
    app.run(debug=True,port = 6000 )
