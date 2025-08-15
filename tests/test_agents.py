from src.agent.coordinator import Coordinator
from src.agent.specialist import Specialist

def test_coordinator_creation_mock_mode():
    """Tests that the Coordinator agent can be created in mock mode."""
    coordinator = Coordinator(use_mock_llm=True)
    assert coordinator is not None
    assert coordinator.use_mock_llm is True

def test_coordinator_handle_disruption_mock_mode():
    """Tests the handle_disruption method in mock mode."""
    coordinator = Coordinator(use_mock_llm=True)
    result = coordinator.handle_disruption("Test Disruption")
    assert result is not None
    assert "input" in result
    assert "output" in result
    assert "The original merchant is busy" in result["output"]

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
