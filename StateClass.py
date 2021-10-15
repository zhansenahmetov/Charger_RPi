"""
This file defines the states available to the Wheelchir
"""
from enum import Enum

# Global state variable
CState = 1
 
class State(Enum):
    """
        This class contains enumerations representing each of the wheelchair states

            ::
                CHARGER_AVAILABLE = 1
                CHARGING_ALLOWED = 3
                AWAITING_CONNECTION= 5
                READY_TO_CHARGE = 6
                CHARGING_IN_PROGRESS = 7
                CHARGER_FAULTY_PLUGGED = 8
                CHARGER_FAULTY_UNPLUGGED = 12
                WC_FULLY_CHARGED = 9
                BATTERY_FAULTY = 10
                TERMINATED_BY_USER = 11
    """
    CHARGER_AVAILABLE = 1
    CHARGING_ALLOWED = 3
    AWAITING_CONNECTION= 5
    READY_TO_CHARGE = 6
    CHARGING_IN_PROGRESS = 7
    CHARGER_FAULTY_PLUGGED = 8
    CHARGER_FAULTY_UNPLUGGED = 12
    WC_FULLY_CHARGED = 9 
    BATTERY_FAULTY = 10
    TERMINATED_BY_USER = 11
    
if __name__ == "__main__":
    CState = State.CHARGER_AVAILABLE
