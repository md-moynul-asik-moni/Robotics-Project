from controller import robot
from controller import Camera


robot = Robot()


timestep = int(robot.getBasicTimeStep())

time_step = 32
max_speed = 6.28


last_error = P = I = D = error = 0
kp = 1.5
ki = 0
kd = 0.3


#camera

cam = Camera('cam')
cam.enable(time_step)



#motor

wheels = []
wheel_names = ['wheel1', 'wheel2', 'wheel3', 'wheel4']


for i in range(4):
    wheels.append(robot.getDevice(wheel_names[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)


#IR sensor


ds = []
ds_names = ['ds_right', 'ds_mid', 'ds_left']

for i in range(3):
    ds.append(robot.getDevice(ds_names[i]))
    ds[i].enable(time_step)


#take reading

while robot.step(time_step) != -1:

    right_ir_value = ds[0].getValue()
    mid_ir_value = ds[1].getValue()
    left_ir_value = ds[2].getValue()

    print("Left {0}, Middle {1}, Right {2}".format(left_ir_value,mid_ir_value,right_ir_value))

    if left_ir_value < 500 and right_ir_value < 500 and mid_ir_value >= 500:
        error = 0
    elif left_ir_value < 500 and right_ir_value >= 500 and mid_ir_value >= 500:
        error =-1
    elif left_ir_value >= 500 and right_ir_value < 500 and mid_ir_value >= 500:
        error = 1
    elif left_ir_value >= 500 and right_ir_value < 500 and mid_ir_value < 500:
        error = 2
    elif left_ir_value < 500 and right_ir_value >= 500 and mid_ir_value < 500:
        error = -2


    #PID implementation

    P = error
    print("P: {}".format(P))

    I = error + I
    print("I: {}".format(I))

    D = error - last_error
    print("D: {}".format(D))

    balance = int ((kp*P) + (ki*I) + (kd*D))
    print("balance: {}".format(balance))

    last_error = error
    print("last_error: {}".format(last_error))


    left_Speed = max_speed - balance
    print("left_speed: {}".format(left_Speed))

    right_Speed = max_speed - balance
    print("left_speed: {}".format(left_Speed))


    #processing of sensor data

    if left_Speed > max_speed :
        wheels[0].setVelocity(left_Speed)
        wheels[1].setVelocity(0)
        wheels[2].setVelocity(left_Speed)
        wheels[3].setVelocity(0)

    if right_Speed > max_speed :
        wheels[0].setVelocity(0)
        wheels[1].setVelocity(right_Speed)
        wheels[2].setVelocity(0)
        wheels[3].setVelocity(right_Speed)

    if left_Speed < 0 :
        wheels[0].setVelocity(0)
        wheels[1].setVelocity(right_Speed)
        wheels[2].setVelocity(0)
        wheels[3].setVelocity(right_Speed)

    if right_Speed < 0 :
        wheels[0].setVelocity(left_Speed)
        wheels[1].setVelocity(0)
        wheels[2].setVelocity(left_Speed)
        wheels[3].setVelocity(0)

    if right_Speed == max_speed :
        wheels[0].setVelocity(left_Speed)
        wheels[1].setVelocity(right_Speed)
        wheels[2].setVelocity(left_Speed)
        wheels[3].setVelocity(right_Speed)
    
    pass