import random
import time

def check_traffic(start_point, end_point):
    """
    Simulates checking the traffic between two points.
    Returns a simulated travel time in minutes.
    """
    print(f"Checking traffic from {start_point} to {end_point}...")
    # Simulate API call delay
    time.sleep(1)
    travel_time = random.randint(15, 60)
    print(f"Simulated travel time: {travel_time} minutes.")
    return {"travel_time_minutes": travel_time}

def get_merchant_status(merchant_id):
    """
    Simulates getting the status of a merchant.
    Returns a simulated status.
    """
    print(f"Getting status for merchant {merchant_id}...")
    # Simulate API call delay
    time.sleep(0.5)
    statuses = ["open", "closed", "busy"]
    status = random.choice(statuses)
    print(f"Simulated merchant status: {status}.")
    return {"merchant_id": merchant_id, "status": status}

def get_driver_location(driver_id):
    """
    Simulates getting the location of a driver.
    Returns a simulated GPS coordinate.
    """
    print(f"Getting location for driver {driver_id}...")
    # Simulate API call delay
    time.sleep(0.5)
    location = {
        "latitude": round(random.uniform(3.0, 4.0), 6),
        "longitude": round(random.uniform(101.0, 102.0), 6)
    }
    print(f"Simulated driver location: {location}.")
    return {"driver_id": driver_id, "location": location}
