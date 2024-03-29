import logging

from states.Config import LightEffect, LightColor, Activity, REST_TIME
from states.Context import Context
from states.IdleState import IdleState
from states.State import State
# from states.WorkState import WorkState
import states.WorkState


class RestState(State):

    def __init__(self, context: Context):
        super().__init__(context)
        self.logger = logging.getLogger("RestState")
        self.logger.info("* RestState created")
        self.restTimerStart = self.context.get_current_time()
        self.context.light_on(LightEffect.SOLID_GREEN)

    def evaluate(self, activity: Activity) -> None:
        if activity == Activity.WORKING:
            self.logger.info("working move to WorkState")
            # TODO This might be optional. Do not come back to WorkState after the break started
            # You can avoid false work comebacks if you rest time is near the desk
            # Unless the activity evaluation exclude near desk presence as working time

            # Adjust the working state timer by deducting a 'short' break time
            # self.nextState.adjust_timer(-self.context.get_current_time() + self.restTimerStart)
            self.context.light_off()
            self.context.change_state(states.WorkState.WorkState(self.context))

        current_time = self.context.get_current_time()
        if self.restTimerStart + REST_TIME < current_time:
            self.logger.info("Activity[{}] rest finish move to Idle state".format(activity))
            # Create Idle state and switch
            self.context.light_off()
            self.context.change_state(IdleState(self.context))
        else:

            self.logger.info("Activity[{}] resting. Timer[{}]"
                             .format(activity, round(current_time - self.restTimerStart)))
            self.context.light_on(LightEffect.SOLID_GREEN)
