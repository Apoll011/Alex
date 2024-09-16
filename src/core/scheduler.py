from core.config import EventPriority
from core.event_scheduler import *

class Scheduler:
    event_scheduler: EventScheduler

    def start_scheduler(self):
        """
        Enable the event scheduler to start taking events
        """
        self.event_scheduler = EventScheduler("AlexEventScheduler")
        return self.event_scheduler.start()

    def stop_scheduler(self, hard_stop=False):
        """
        Stop the event scheduler and its internal thread.
        Set hard_stop to True to stop the scheduler right away and discard all pending events.
        Set hard_stop too False to wait for all events to finish executing at their scheduled times.
        """
        return self.event_scheduler.stop(hard_stop)

    def schedule(self, delay, priority: EventPriority, action, *args, **kwargs):
        """
        Schedule an event with a callable action to be executed after the delay.
        Events will be executed according to their delay and priority (lower number = higher priority).
        Arguments hold positional arguments and kwargs hold keyword arguments for the action.
        Returns an event object which can be used to cancel the event.

        Args:
            :param delay: The relative time the event will be scheduled to execute.
                E.g.,
                If you pass in 1 as the delay, the event will be scheduled
                to execute in 1 + now() seconds from now.
            :param priority: The priority the event will execute with.
            If two
                events are scheduled for the same time, the event with the
                lower priority will execute first.
            :param action: The function which will be invoked when the event
                executes.
            :param args: Variable length argument list for the action.
            :param kwargs: Keyword arguments for the action.

        """
        return self.event_scheduler.enter(delay, priority.value, action, arguments=args, kwargs=kwargs)

    def schedule_recurrent(self, interval, priority: EventPriority, action, *args, **kwargs):
        """
        Enter a new recurring event in the queue to occur at a specified
        interval.

        Args:
            interval: The interval time the event will be scheduled to execute.
                E.g., If you pass in 5 as the delay, the event will be scheduled to
                execute every 5 seconds starting five seconds from when it's
                entered.
            priority (int): The priority the event will execute with. If two
                events are scheduled for the same time, the event with the
                lower priority will execute first.
            action (callable): The function which will be invoked when the event
                executes.
            args (optional): Variable length argument list for the action.
            kwargs (:obj:`dict`, optional): Keyword arguments for the action.

        Returns:
            int: An event id of the recurring event if the scheduler is
            running, None otherwise. This id can be used to cancel the event
            later, if necessary.

        Raises:
            ValueError: If the 0 > priority >= sys.maxsize

        Warning:
            Long running actions will stall the internal thread and may impact
            the scheduling of other events.
        """
        return self.event_scheduler.enter_recurring(interval, priority.value, action, arguments=args, kwargs=kwargs)
    

    def cancel(self, event: Event):
        """
        Cancel the event if it has not yet been executed.
        """
        return self.event_scheduler.cancel(event)
    
    def cancel_recurring(self, event_id):
        """
        Cancel the recurring event and all future occurrences.
        """
        return self.event_scheduler.cancel_recurring(event_id)
