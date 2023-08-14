import threading
import time

class IntervalRunner:
    def __init__(self, interval_secs, target_func, func_args=(), result_callback=None):
        """
        Constructor for IntervalRunner.

        :param interval: The interval in seconds at which the target function should be called.
        :param target_func: The function to be called at the specified interval.
        :param func_args: Tuple of arguments to pass to the target function (default: empty tuple).
        :param result_callback: Callback function to receive results from the target function (default: None).
        """
        self.interval = interval_secs
        self.target_func = target_func
        self.func_args = func_args
        self.result_callback = result_callback
        self.running = False
        self.thread = None

    def _run(self):
        while self.running:
            result = self.target_func(*self.func_args)
            if self.result_callback:
                self.result_callback(result)
            time.sleep(self.interval)

    def start(self):
        """
        Start the IntervalRunner.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        """
        Stop the IntervalRunner.
        """
        if self.running:
            self.running = False
            self.thread.join()

    #property
    @property
    def interval(self):
        """
        Getter for the interval attribute.
        """
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        """
        Setter for the interval attribute.
        """
        if new_interval <= 0:
            raise ValueError("Interval must be a positive value")
        self._interval = new_interval

# Example usage:
def example_target_function(arg1, arg2):
    # Simulate some work
    result = arg1 + arg2
    print("Target function called with args:", arg1, arg2)
    return result

def example_result_callback(result):
    print("Result from target function:", result)

if __name__ == "__main__":
    interval_runner = IntervalRunner(interval_secs=2, target_func=example_target_function,
                                     func_args=(5, 10), result_callback=example_result_callback)

    interval_runner.start()

    try:
        # Keep the program running for some time to observe the interval runner in action
        time.sleep(10)
    finally:
        interval_runner.stop()
