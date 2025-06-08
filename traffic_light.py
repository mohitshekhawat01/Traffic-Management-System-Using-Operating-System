import random

class TrafficLight:
    def __init__(self, env, name, traffic, priority):
        self.env = env
        self.name = name
        self.traffic = traffic
        self.priority = priority
        self.green_time = 10
        self.red_time = 5
        self.light_color = 'red'
        self.emergency_detected = False
        self.vehicles = self.generate_vehicles()

        self.env.process(self.control_light())

    def control_light(self):
        while True:
            self.light_color = 'red'
            print(f"{self.env.now}: {self.name} light is RED.")
            for _ in range(self.red_time):
                yield self.env.timeout(1)
                self.check_camera_feed()
                if self.emergency_detected:
                    print(f"{self.env.now}: Emergency detected at {self.name}, switching to GREEN!")
                    break

            self.light_color = 'green'
            print(f"{self.env.now}: {self.name} light is GREEN.")
            green_duration = self.green_time
            if self.emergency_detected:
                green_duration += 5
                self.emergency_detected = False

            for _ in range(green_duration):
                yield self.env.timeout(1)
                self.reduce_traffic()

            self.light_color = 'yellow'
            print(f"{self.env.now}: {self.name} light is YELLOW.")
            yield self.env.timeout(3)

    def reduce_traffic(self):
        self.traffic = max(0, self.traffic - 1)
        if self.vehicles:
            vehicle = self.vehicles.pop(0)
            print(f"{self.env.now}: {vehicle['type']} passed from {self.name}.")

    def check_camera_feed(self):
        self.emergency_detected = random.random() < 0.1  

    def generate_vehicles(self):
        return [{"id": f"{self.name}-{i}", "type": random.choice(["car", "bus", "bike", "truck", "ambulance"])}
                for i in range(self.traffic)]

    def get_vehicle_queue(self):
        return self.vehicles
