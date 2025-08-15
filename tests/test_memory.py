from src.memory.context import ContextMemory

def test_context_memory_creation():
    """Tests that the ContextMemory can be created."""
    memory = ContextMemory()
    assert memory is not None
    assert memory.get_all_context() == {}

def test_context_memory_add_and_get():
    """Tests adding and retrieving context."""
    memory = ContextMemory()
    memory.add_context("case_123", {"status": "resolved"})
    context = memory.get_context("case_123")
    assert context is not None
    assert context["status"] == "resolved"

def test_context_memory_get_nonexistent():
    """Tests retrieving non-existent context."""
    memory = ContextMemory()
    context = memory.get_context("nonexistent_key")
    assert context is None
