from collections import deque

class EmergencyManager:
    def __init__(self):
        self.emergency_queue = deque()

    def add_emergency(self, road_name, vehicle_type):
        if road_name not in [e['road'] for e in self.emergency_queue]:
            self.emergency_queue.append({"road": road_name, "vehicle_type": vehicle_type})

    def get_active_emergencies(self):
        return [e['road'] for e in self.emergency_queue]

    def get_vehicle_type(self, road_name):
        for e in self.emergency_queue:
            if e['road'] == road_name:
                return e['vehicle_type']
        return None

    def clear_emergency(self, road_name):
        self.emergency_queue = deque(e for e in self.emergency_queue if e['road'] != road_name)