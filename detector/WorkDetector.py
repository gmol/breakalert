import logging
from threading import Event, Thread

from detector.DistanceThresholdCounter import DistanceThresholdCounter
from detector.Sample import Sample
from states import Config

from states.Config import Activity
from states.Context import Context


class WorkDetector:

    def __init__(self, context: Context):
        self.measurements = []
        self.logger = logging.getLogger("WorkDetector")
        self.context = context

    def add_sample(self, sample: Sample):
        self.measurements.append(sample)
        # self.detect()
        self.clean_up()

    def start(self):
        # TODO Strategy is not configurable
        if Config.IS_DEBUG:
            self.call_repeatedly(5, self.detect, DistanceThresholdCounter())
        else:
            self.call_repeatedly(1, self.detect, DistanceThresholdCounter())

    def detect(self, strategy):
        self.logger.info("* detect")
        if len(self.measurements) > 0:
            work_detected = strategy.detect(self.measurements)
            if work_detected:
                self.context.update_action(Activity.WORKING)
            else:
                self.context.update_action(Activity.IDLE)

    def clean_up(self):
        if len(self.measurements) > 1000:
            # TODO provide a better cleanup
            del self.measurements[0]

    def call_repeatedly(self, interval, func, *args):
        # self.logger.info("* call_repeatedly interval [{}]".format(interval))
        stopped = Event()

        def loop():
            while not stopped.wait(interval):  # the first call is in `interval` secs
                # self.logger.info(f"Thread's loop: ${func}")
                func(*args)

        Thread(target=loop).start()
        return stopped.set
