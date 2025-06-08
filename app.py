
from flask import Flask, render_template, jsonify, request # type: ignore
import simpy # type: ignore
import threading
import logging
import time
import random

from traffic_light import TrafficLight
from emergency_handler import EmergencyManager
from scheduling import round_robin_scheduling


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)


traffic_data = {}
stop_simulation = False
simulation_running = False
emergency_manager = EmergencyManager()
roads = []

def init_traffic():
    return {
        "Road A": {"status": "RED", "traffic": random.randint(20, 50), "emergency": False, "vehicle": None},
        "Road B": {"status": "RED", "traffic": random.randint(15, 40), "emergency": False, "vehicle": None},
        "Road C": {"status": "RED", "traffic": random.randint(25, 45), "emergency": False, "vehicle": None},
        "Road D": {"status": "RED", "traffic": random.randint(18, 38), "emergency": False, "vehicle": None},
    }

def update_status(name, status, traffic, emergency=False, vehicle=None):
    global traffic_data
    if name in traffic_data:
        traffic_data[name].update({
            "status": status,
            "traffic": max(0, traffic),
            "emergency": emergency,
            "vehicle": vehicle
        })
        logger.debug(f"Updated {name}: {traffic_data[name]}")

def simulation():
    global env, traffic_data, stop_simulation, simulation_running, roads

    env = simpy.Environment()
    traffic_data = init_traffic()
    roads = []

    road_names = ["Road A", "Road B", "Road C", "Road D"]
    for name in road_names:
        traffic = random.randint(5, 20)
        priority = random.randint(1, 5)
        light = TrafficLight(env, name, traffic, priority)
        roads.append(light)

    def update_callback(name, status, traffic):
        update_status(name, status, traffic)

    env.process(round_robin_scheduling(env, roads, update_callback))

    def run():
        global simulation_running
        simulation_running = True
        logger.debug("Simulation running...")
        while not stop_simulation:
            try:
                env.step()
                for light in roads:
                    update_status(light.name, light.status, light.traffic,
                                  emergency=light.emergency_detected,
                                  vehicle=light.vehicles[0]["type"] if light.vehicles else None)

                    # If emergency vehicle detected, override traffic light status
                    if light.emergency_detected:
                        update_status(light.name, "GREEN", light.traffic, emergency=True, vehicle=light.vehicles[0]["type"])

                time.sleep(1)
            except Exception as e:
                logger.error(f"Simulation error: {e}")
                break
        simulation_running = False
        logger.debug("Simulation stopped.")

    threading.Thread(target=run, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global stop_simulation, simulation_running
    if simulation_running:
        return jsonify({"status": "already running"})
    stop_simulation = False
    threading.Thread(target=simulation, daemon=True).start()
    return jsonify({"status": "started"})

@app.route('/stop')
def stop():
    global stop_simulation, simulation_running
    if not simulation_running:
        return jsonify({"status": "already stopped"})
    stop_simulation = True
    return jsonify({"status": "stopped"})

@app.route('/data')
def data():
    return jsonify(traffic_data)

@app.route('/emergency/<road>', methods=['POST'])
def trigger_emergency(road):
    global emergency_manager, traffic_data
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/json' not in content_type:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        data = request.get_json(force=True)
        if not data or 'vehicle' not in data:
            return jsonify({"error": "Missing 'vehicle' in data"}), 400

        vehicle_type = data['vehicle']
        emergency_manager.add_emergency(road, vehicle_type)
        traffic_data[road]["emergency"] = True
        traffic_data[road]["vehicle"] = vehicle_type

        
        traffic_data[road]["status"] = "GREEN"

        return jsonify({"status": "emergency triggered", "road": road, "vehicle": vehicle_type})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    logger.debug("Starting Flask app...")
    app.run(debug=True)