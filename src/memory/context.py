class ContextMemory:
    """
    A simple in-memory store for the agent's context.
    This can be replaced with a more sophisticated database or vector store in the future.
    """
    def __init__(self):
        self._memory = {}
        print("Context memory initialized.")

    def add_context(self, key, value):
        """
        Adds a piece of context to the memory.
        """
        print(f"Adding context for key '{key}': {value}")
        self._memory[key] = value

    def get_context(self, key):
        """
        Retrieves a piece of context from the memory.
        """
        print(f"Retrieving context for key '{key}'...")
        return self._memory.get(key)

    def get_all_context(self):
        """
        Retrieves all context from the memory.
        """
        return self._memory
