from core.context import ContextManager

class AiContextUser:
    """
    A class to manage AI-related context
    """
    
    _context = ContextManager()
    """
    The context manager
    """

    def get_context(self, name: str, type: str = "pickle"):
        """
        Retrieves a context value

        Args:
            name (str): The name of the context value
            type (str): The type of the context value (default: "pickle")

        Returns:
            The context value
        """
        return self._context.load(name, type)

    def set_context(self, name: str, value, type: str = "pickle"):
        """
        Sets a context value

        Args:
            name (str): The name of the context value
            value: The value to be set
            type (str): The type of the context value (default: "pickle")
        """
        self._context.save(value, name, type)
