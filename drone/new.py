import rospy
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool

import math

from clover.srv import SetLEDEffect

rospy.init_node('flight')

def make_proxy(namespace, service_name, service_type):
    return rospy.ServiceProxy(f'{namespace}/{service_name}', service_type)

drones = ['drone1', 'drone2', 'drone3', 'drone4']

get_telemetry = {}
navigate = {}
land = {}
arming = {}
set_effect = {}
set_position = {}
set_velocity = {}

for drone in drones:
    get_telemetry[drone] = make_proxy(drone, 'get_telemetry', srv.GetTelemetry)
    navigate[drone] = make_proxy(drone, 'navigate', srv.Navigate)
    land[drone] = make_proxy(drone, 'land', Trigger)
    arming[drone] = make_proxy(drone, 'mavros/cmd/arming', CommandBool)
    set_effect[drone] = make_proxy(drone, 'led/set_effect', SetLEDEffect)
    set_position[drone] = make_proxy(drone, 'set_position', srv.SetPosition)
    set_velocity[drone] = make_proxy(drone, 'set_velocity', srv.SetVelocity)

# get_telemetry[drone] = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
# navigate = rospy.ServiceProxy('navigate', srv.Navigate)
# navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
# set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
# set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
# set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
# set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
# set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
# land = rospy.ServiceProxy('land', Trigger)
# arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

def takeoff_wait(drone="drone1", z=1):
   # navigate[drone](z=z, frame_id='body', auto_arm=True)
    while True:
        telemetry = get_telemetry[drone]()
        if telemetry.z > (z-0.1):
            break
        rospy.sleep(0.2)

def land_wait(drone="drone1"):
   # land[drone]()
    while get_telemetry[drone]().armed:
        rospy.sleep(0.2)

def navigate_wait(drone="drone1", x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
   # navigate[drone](x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry[drone](frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def gorizontal_circle():
    RADIUS = 0.6  # m
    SPEED = 0.3  # rad / s
    
    start = get_telemetry[drone]()
    start_stamp = rospy.get_rostime()
    
    r = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        angle = (rospy.get_rostime() - start_stamp).to_sec() * SPEED
        x = start.x + math.sin(angle) * RADIUS
        y = start.y + math.cos(angle) * RADIUS
        set_position(x=x, y=y, z=start.z)
        
        r.sleep()


def main():
    # arming[drone](True)
   
    for drone in drones:
        print(f'{drone} Arming and taking off...')
        arming[drone](True)
        # set_effect[drone](r=0, g=0, b=255)
        navigate[drone](x=0, y=0, z=1, frame_id='body', auto_arm=True)
        takeoff_wait(drone)
        
    # for drone in drones:
    #     takeoff_wait(drone)
    
    # Wait for 5 seconds
    # rospy.sleep(5)
    
    # print('Fly forward 1 m')
    # set_effect(effect='rainbow')
    # # navigate[drone](x=1, y=0, z=0, frame_id='body')
    # navigate_wait(frame_id='aruco_5', x=0, y=0, z=0)

    for drone in drones:
        print(f'{drone} Landing...')
        # set_effect[drone](r=255, g=0, b=0)
        land[drone]()
    
    for drone in drones:
        land_wait(drone)
    
    # arming[drone](False)

if __name__ == "__main__":
    main()