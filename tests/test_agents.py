from src.agent.coordinator import Coordinator
from src.agent.specialist import Specialist

def test_coordinator_creation():
    """Tests that the Coordinator agent can be created."""
    coordinator = Coordinator()
    assert coordinator is not None

def test_coordinator_handle_disruption():
    """Tests the placeholder handle_disruption method."""
    coordinator = Coordinator()
    result = coordinator.handle_disruption("Test Disruption")
    assert result == "Disruption handled."

def test_specialist_creation():
    """Tests that the Specialist agent can be created."""
    specialist = Specialist("Traffic")
    assert specialist is not None
    assert specialist.name == "Traffic"

def test_specialist_provide_analysis():
    """Tests the placeholder provide_analysis method."""
    specialist = Specialist("Traffic")
    result = specialist.provide_analysis("Road closure")
    assert result == "Analysis for Road closure."
