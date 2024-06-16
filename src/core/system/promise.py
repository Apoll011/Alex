import threading

class Promise:
    def __init__(self):
        """
        Initializes a new Promise object.
        """
        self.resolved = False
        self.rejected = False
        self.value = None
        self.error = None
        self.then_callback = None
        self.catch_callback = None
        self.lock = threading.Lock()

    def then(self, callback):
        """
        Registers a callback to be called when the promise is resolved.

        Args:
            callback: The callback function to be called when the promise is resolved.

        Returns:
            The promise object.
        """
        with self.lock:
            if self.resolved:
                callback(self.value)
            else:
                self.then_callback = callback
        return self

    def catch(self, callback):
        """
        Registers a callback to be called when the promise is rejected.

        Args:
            callback: The callback function to be called when the promise is rejected.

        Returns:
            The promise object.
        """
        with self.lock:
            if self.rejected:
                callback(self.error)
            else:
                self.catch_callback = callback
        return self

    def resolve(self, value):
        """
        Resolves the promise with a given value.

        Args:
            value: The value to resolve the promise with.
        """
        threading.Thread(target=self.do_resolve, args=(value,)).start()

    def do_resolve(self, value):
        """
        Resolves the promise with a given value in a separate thread.

        Args:
            value: The value to resolve the promise with.
        """
        try:
            v = value()
            self._set_result(v)
        except Exception as e:
            self._set_error(e)

    def reject(self, error):
        """
        Rejects the promise with a given error.

        Args:
            error: The error to reject the promise with.
        """
        self._set_error(error)

    def _set_result(self, value):
        """
        Sets the result of the promise to a given value.

        Args:
            value: The value to set the result to.
        """
        with self.lock:
            if not self.resolved and not self.rejected:
                self.value = value
                self.resolved = True
                if self.then_callback:
                    self.then_callback(value)

    def _set_error(self, error):
        """
        Sets the error of the promise to a given error.

        Args:
            error: The error to set the error to.
        """
        with self.lock:
            if not self.rejected and not self.resolved:
                self.rejected = True
                self.error = error
                if self.catch_callback:
                    self.catch_callback(error)
