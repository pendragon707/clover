from threading import Thread
import rospy

from clover import srv
from std_srvs.srv import Trigger

import numpy as np

import logging


class SingleClover: 
#Create and call all servicers, subscribers and clover topics
    def __init__(self, name, clover_id):
        self.name = name
        self.id = clover_id
        self.init_coord = []

        # Configure clover services and topics
        self.configure()

    def configure(self):

        logging.debug("Waiting clover services...")
        rospy.loginfo("Waiting clover services...")

        rospy.wait_for_service(f"{self.name}/get_telemetry", timeout=1)
        self.get_telemetry = rospy.ServiceProxy(f"{self.name}/get_telemetry", srv.GetTelemetry)
        
        rospy.wait_for_service(f"{self.name}/navigate", timeout=1)
        self.navigate = rospy.ServiceProxy(f"{self.name}/navigate", srv.Navigate)
        
        rospy.wait_for_service(f"{self.name}/navigate_global", timeout=1)
        self.navigate_global = rospy.ServiceProxy(f"{self.name}/navigate_global", srv.NavigateGlobal)
        
        rospy.wait_for_service(f"{self.name}/set_position", timeout=1)
        self.set_position = rospy.ServiceProxy(f"{self.name}/set_position", srv.SetPosition)
        
        rospy.wait_for_service(f"{self.name}/set_velocity", timeout=1)
        self.set_velocity = rospy.ServiceProxy(f"{self.name}/set_velocity", srv.SetVelocity)
        
        rospy.wait_for_service(f"{self.name}/set_attitude", timeout=1)
        self.set_attitude = rospy.ServiceProxy(f"{self.name}/set_attitude", srv.SetAttitude)
        
        rospy.wait_for_service(f"{self.name}/set_rates", timeout=1)
        self.set_rates = rospy.ServiceProxy(f"{self.name}/set_rates", srv.SetRates)
        
        rospy.wait_for_service(f"{self.name}/land", timeout=1)
        self.land = rospy.ServiceProxy(f"{self.name}/land", Trigger)

        rospy.wait_for_service(f"{self.name}/led/set_effect", timeout=1)
        self.set_effect = rospy.ServiceProxy(f"{self.name}/led/set_effect", srv.SetLEDEffect)
   
    def navigateWait(self, x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
      
        self.navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

        while not rospy.is_shutdown():
            telem = self.get_telemetry(frame_id='navigate_target' + str(self.id))
            if np.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
                break
            rospy.sleep(0.2)
         
    def landWait(self):
        self.land()
        while self.get_telemetry().armed:
            rospy.sleep(0.2)

class Swarm:

    def __init__(self, num_of_clovers=None, swarm_name=None):
        logging.basicConfig(level=logging.INFO)

        self.swarm = []
        # self.swarm_state = SwarmState()     

        self.num_of_clovers = None
        if num_of_clovers != None:
            if num_of_clovers == 0:
                logging.error('Input num_of_clover need to be greater than zero.')
            else:
                self.num_of_clovers = num_of_clovers         
     
        self.all_of_clovers = 0
        self.connected_clovers = 0
        self.armed_clovers = 0
        self.offboard_mode_clovers = 0

        self.all_clovers_ids = []
        self.connected_ids = []

    def __createCloversObjects(self):
        for idx, clover_id in enumerate(self.connected_ids):
            clover_object = SingleClover(f"clover{clover_id}", clover_id)
            clover_object.init_coord = self.init_formation_coords[idx]
            self.swarm.append(clover_object)

    def takeOffAll(self, z=1, speed=0.5):
        logging.debug(f"{self.num_of_clovers} drones taking off")
        rospy.loginfo(f"{self.num_of_clovers} drones taking off")

        threads = []
        for idx, clover in enumerate(self.swarm):
            # x = self.des_formation_coords[idx][0] - clover.init_coord[0]
            # y = self.des_formation_coords[idx][1] - clover.init_coord[1]
            # z = self.des_formation_coords[idx][2]  

            x = 0
            y = 0
            z = 1

            thrd = Thread(target=clover.navigateWait, kwargs=dict(x=x, y=y, z=z, tolerance=0.2, speed=speed, auto_arm=True))
            threads.append(thrd)

        for thrd in threads:
            thrd.start()
        
        for thrd in threads:
            thrd.join()




# def make_proxy(namespace, service_name, service_type):
#     return rospy.ServiceProxy(f'{namespace}/{service_name}', service_type)

# class FlightServices:
#     def __init__(self, drones = None):
#         if not drones:
#             drones = ['drone1', 'drone2', 'drone3', 'drone4']

#         self.get_telemetry = {}
#         self.navigate = {}
#         self.land = {}
#         self.arming = {}
#         self.set_effect = {}
#         self.set_position = {}
#         self.set_velocity = {}        

#         for drone in drones:
#             self.get_telemetry[drone] = make_proxy(drone, 'get_telemetry', srv.GetTelemetry)
#             self.navigate[drone] = make_proxy(drone, 'navigate', srv.Navigate)
#             self.land[drone] = make_proxy(drone, 'land', Trigger)
#             self.arming[drone] = make_proxy(drone, 'mavros/cmd/arming', CommandBool)
#             self.set_effect[drone] = make_proxy(drone, 'led/set_effect', SetLEDEffect)
#             self.set_position[drone] = make_proxy(drone, 'set_position', srv.SetPosition)
#             self.set_velocity[drone] = make_proxy(drone, 'set_velocity', srv.SetVelocity)            