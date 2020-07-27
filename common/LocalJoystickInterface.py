import numpy as np
import time
from common.State import BehaviorState, State
from common.Command import Command
from common.Utilities import deadband, clipped_first_order_filter

from xbox_controller import XboxController

class LocalJoystickInterface:
    def __init__(self, config):
        self.config = config
        self.previous_gait_toggle = 0
        self.previous_state = BehaviorState.REST
        self.previous_hop_toggle = 0
        self.previous_activate_toggle = 0

        self.message_rate = 50

        self.gamepad = XboxController()

    def get_command(self, state, do_print=False):
        command = Command()

        ####### Handle discrete commands ########
        # Check if requesting a state transition to trotting, or from trotting to resting
        gait_toggle = self.gamepad.RightBumper
        command.trot_event = (gait_toggle == 1 and self.previous_gait_toggle == 0)

        # Check if requesting a state transition to hopping, from trotting or resting
        hop_toggle = self.gamepad.X
        command.hop_event = (hop_toggle == 1 and self.previous_hop_toggle == 0)

        activate_toggle = self.gamepad.LeftBumper
        command.activate_event = (activate_toggle == 1 and self.previous_activate_toggle == 0)

        # Update previous values for toggles and state
        self.previous_gait_toggle = gait_toggle
        self.previous_hop_toggle = hop_toggle
        self.previous_activate_toggle = activate_toggle

        ####### Handle continuous commands ########
        x_vel = self.gamepad.LeftJoystickY * self.config.max_x_velocity
        y_vel = self.gamepad.LeftJoystickX * -self.config.max_y_velocity
        command.horizontal_velocity = np.array([x_vel, y_vel])
        command.yaw_rate = self.gamepad.RightJoystickX * -self.config.max_yaw_rate

        message_rate = self.message_rate
        message_dt = 1.0 / message_rate

        pitch = self.gamepad.RightJoystickY * self.config.max_pitch
        deadbanded_pitch = deadband(
            pitch, self.config.pitch_deadband
        )
        pitch_rate = clipped_first_order_filter(
            state.pitch,
            deadbanded_pitch,
            self.config.max_pitch_rate,
            self.config.pitch_time_constant,
        )
        command.pitch = state.pitch + message_dt * pitch_rate

        height_movement = self.gamepad.UpDPad - self.gamepad.DownDPad
        command.height = state.height - message_dt * self.config.z_speed * height_movement

        roll_movement = self.gamepad.RightDPad - self.gamepad.LeftDPad
        command.roll = state.roll + message_dt * self.config.roll_speed * roll_movement

        return command
