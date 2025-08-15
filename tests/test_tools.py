from src.tools.logistics import check_traffic, get_merchant_status, get_driver_location
import time

def test_check_traffic():
    """Tests the check_traffic tool."""
    result = check_traffic("A", "B")
    assert "travel_time_minutes" in result
    assert 15 <= result["travel_time_minutes"] <= 60

def test_get_merchant_status():
    """Tests the get_merchant_status tool."""
    result = get_merchant_status("merchant-123")
    assert "merchant_id" in result
    assert result["merchant_id"] == "merchant-123"
    assert "status" in result
    assert result["status"] in ["open", "closed", "busy"]

def test_get_driver_location():
    """Tests the get_driver_location tool."""
    result = get_driver_location("driver-456")
    assert "driver_id" in result
    assert result["driver_id"] == "driver-456"
    assert "location" in result
    assert "latitude" in result["location"]
    assert "longitude" in result["location"]
