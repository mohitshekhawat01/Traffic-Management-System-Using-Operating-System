def round_robin_scheduling(env, traffic_lights, update_callback, manual_override):
    """Round-robin scheduling for traffic lights with manual override."""
    while True:
        
        override_road = manual_override()
        if override_road:
            for tl in traffic_lights:
                if tl.name == override_road:
                    update_callback(tl.name, "GREEN", tl.traffic)
                else:
                    update_callback(tl.name, "RED", tl.traffic)
            yield env.timeout(10)
            continue

        
        traffic_lights.sort(key=lambda x: -x.traffic)

        for tl in traffic_lights:
            
            if hasattr(tl, 'emergency_detected') and tl.emergency_detected:
                continue

            # Green phase
            tl.traffic = max(0, tl.traffic - 10)
            update_callback(tl.name, "GREEN", tl.traffic)
            yield env.timeout(10)

            # Yellow phase
            update_callback(tl.name, "YELLOW", tl.traffic)
            yield env.timeout(3)

            # Red phase
            update_callback(tl.name, "RED", tl.traffic)
            yield env.timeout(5)

        yield env.timeout(1)
