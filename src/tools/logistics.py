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


def notify_customer(customer_id, message):
    """
    Simulates notifying a customer with a message.
    """
    print(f"Notifying customer {customer_id}: '{message}'")
    # Simulate API call delay
    time.sleep(0.5)
    print("Notification sent successfully.")
    return {"status": "success", "customer_id": customer_id}


def re_route_driver(driver_id, new_destination, reason):
    """
    Simulates re-routing a driver to a new destination for a given reason.
    """
    print(f"Re-routing driver {driver_id} to {new_destination} because: {reason}")
    # Simulate API call delay
    time.sleep(1)
    print(f"Driver {driver_id} successfully re-routed.")
    return {"status": "success", "driver_id": driver_id, "new_destination": new_destination}


def get_nearby_merchants(latitude, longitude, category, radius_km=2):
    """
    Simulates finding nearby merchants of a specific category.
    """
    print(f"Finding nearby '{category}' merchants near ({latitude}, {longitude})...")
    # Simulate API call delay
    time.sleep(1)
    merchants = [
        {"merchant_id": "merchant-888", "name": "Speedy Pizza", "wait_time_minutes": 15},
        {"merchant_id": "merchant-999", "name": "Quick Burger", "wait_time_minutes": 10},
    ]
    print(f"Found {len(merchants)} nearby merchants.")
    return {"merchants": merchants}


def initiate_mediation_flow(order_id, customer_id, driver_id):
    """
    Simulates initiating a real-time mediation flow for a dispute.
    """
    print(f"Initiating mediation for order {order_id} between customer {customer_id} and driver {driver_id}.")
    time.sleep(1)
    return {"status": "success", "mediation_id": f"med-{order_id}"}


def collect_evidence(mediation_id, parties):
    """
    Simulates collecting evidence from parties in a dispute.
    """
    print(f"Collecting evidence for mediation {mediation_id} from {', '.join(parties)}.")
    time.sleep(2) # Simulate time for parties to respond
    evidence = {
        "customer_photo_url": "https://example.com/spilled_drink.jpg",
        "driver_statement": "The bag was sealed by the merchant.",
        "customer_statement": "The seal was intact upon handover, but the drink was spilled inside the sealed bag."
    }
    print("Evidence collected.")
    return {"status": "success", "evidence": evidence}


def analyze_evidence(evidence):
    """
    Simulates analyzing the collected evidence to determine fault.
    """
    print("Analyzing evidence...")
    time.sleep(1.5)
    if "sealed" in evidence.get("driver_statement", "") and "intact" in evidence.get("customer_statement", ""):
        fault = "merchant"
        reason = "The damage occurred inside a sealed bag, indicating poor packaging by the merchant."
    else:
        fault = "unclear"
        reason = "The evidence is not sufficient to determine clear fault."

    print(f"Analysis complete. Determined fault: {fault}.")
    return {"fault": fault, "reason": reason}


def issue_instant_refund(customer_id, order_id, amount):
    """
    Simulates issuing an instant refund to a customer.
    """
    print(f"Issuing refund of ${amount} to customer {customer_id} for order {order_id}.")
    time.sleep(0.5)
    return {"status": "success", "refund_id": f"ref-{order_id}"}


def exonerate_driver(driver_id, order_id):
    """
    Simulates clearing a driver of fault for a delivery issue.
    """
    print(f"Exonerating driver {driver_id} from fault for order {order_id}.")
    time.sleep(0.5)
    return {"status": "success", "driver_id": driver_id}


def log_merchant_packaging_feedback(merchant_id, order_id, feedback_details):
    """
    Simulates logging feedback about a merchant's packaging.
    """
    print(f"Logging packaging feedback for merchant {merchant_id} regarding order {order_id}.")
    print(f"Feedback: {feedback_details}")
    time.sleep(0.5)
    return {"status": "success", "log_id": f"log-{order_id}"}


def notify_resolution(parties, order_id, resolution_summary):
    """
    Simulates notifying all parties of the final resolution.
    """
    print(f"Notifying parties ({', '.join(parties)}) for order {order_id} of the resolution.")
    print(f"Resolution: {resolution_summary}")
    time.sleep(0.5)
    return {"status": "success"}


def contact_recipient_via_chat(recipient_id, initial_message):
    """
    Simulates contacting a recipient via chat and getting a response.
    """
    print(f"Contacting recipient {recipient_id} with message: '{initial_message}'")
    time.sleep(1.5) # Simulate sending message and waiting for reply
    responses = [
        "I'm not home right now, can you leave it with my neighbour at Unit 102?",
        "Just leave it at the door, please.",
        "I'm stuck in traffic, I'll be there in 15 minutes!",
        "Sorry, I'm out of town. Can you deliver it tomorrow?",
    ]
    simulated_response = random.choice(responses)
    print(f"Received response from {recipient_id}: '{simulated_response}'")
    return {"status": "success", "response": simulated_response}


def suggest_safe_drop_off(recipient_id, suggestion):
    """
    Simulates suggesting a safe drop-off location and getting confirmation.
    """
    print(f"Suggesting to {recipient_id}: 'Is it okay if I {suggestion}?'")
    time.sleep(1)
    confirmation = random.choice([True, False])
    if confirmation:
        print(f"Recipient {recipient_id} approved the suggestion.")
        return {"status": "approved", "suggestion": suggestion}
    else:
        print(f"Recipient {recipient_id} rejected the suggestion.")
        return {"status": "rejected", "suggestion": suggestion}


def find_nearby_locker(latitude, longitude):
    """
    Simulates finding a nearby secure parcel locker.
    """
    print(f"Searching for secure parcel lockers near ({latitude}, {longitude})...")
    time.sleep(1)
    lockers = [
        {"locker_id": "locker-a1", "address": "123 Main St, Lobby", "availability": "high"},
        {"locker_id": "locker-b2", "address": "456 Oak Ave, Supermarket", "availability": "low"},
    ]
    print(f"Found {len(lockers)} nearby lockers.")
    return {"status": "success", "lockers": lockers}
