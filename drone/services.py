import rospy
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from clover.srv import SetLEDEffect

def make_proxy(namespace, service_name, service_type):
    return rospy.ServiceProxy(f'{namespace}/{service_name}', service_type)

# from clover_swarm.async_ros import AsyncService


# class FlightServices:
#     get_telemetry = AsyncService("get_telemetry", srv.GetTelemetry)
#     navigate = AsyncService("navigate", srv.Navigate)
#     navigate_global = AsyncService("navigate_global", srv.NavigateGlobal)
#     set_position = AsyncService("set_position", srv.SetPosition)
#     set_velocity = AsyncService("set_velocity", srv.SetVelocity)
#     set_attitude = AsyncService("set_attitude", srv.SetAttitude)
#     set_rates = AsyncService("set_rates", srv.SetRates)
#     land = AsyncService("land", Trigger)

#     async def connect(self, timeout=None):
#         async with trio.open_nursery() as nursery:
#             nursery.start_soon(self.get_telemetry.connect, timeout)


    # get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
    # navigate = rospy.ServiceProxy('navigate', srv.Navigate)
    # navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
    # set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
    # set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
    # set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
    # set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
    # land = rospy.ServiceProxy('land', Trigger)
    # arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)


class FlightServices:
    def __init__(self, drones = None):
        if not drones:
            drones = ['drone1', 'drone2', 'drone3', 'drone4']

        self.get_telemetry = {}
        self.navigate = {}
        self.land = {}
        self.arming = {}
        self.set_effect = {}
        self.set_position = {}
        self.set_velocity = {}        

        for drone in drones:
            self.get_telemetry[drone] = make_proxy(drone, 'get_telemetry', srv.GetTelemetry)
            self.navigate[drone] = make_proxy(drone, 'navigate', srv.Navigate)
            self.land[drone] = make_proxy(drone, 'land', Trigger)
            self.arming[drone] = make_proxy(drone, 'mavros/cmd/arming', CommandBool)
            self.set_effect[drone] = make_proxy(drone, 'led/set_effect', SetLEDEffect)
            self.set_position[drone] = make_proxy(drone, 'set_position', srv.SetPosition)
            self.set_velocity[drone] = make_proxy(drone, 'set_velocity', srv.SetVelocity)            