# System Commands
EXIT = "Exit"
ABORT = "Abort"
RESUME = "Resume"
CUTDOWN = "Cutdown"
CUTDOWN_RESPONSE = "CutdownResponse"
RELAY = "Relay"
CONFIRM_CONNECTION = "ConfirmConnection"
CHECK_CONNECTION = "CheckConnection"
CONFIRMED_CONNECTION = "ConfirmedConnection"
UNKNOWN_COMMAND = "UnknownCommand"
ERROR = "Error"
CONFIRM = "Confirm"

# Sensor Commands
HUMIDITY = "Humidity"
GPS = "GPS"
PRESSURE = "Pressure"
TEMPERATURE = "Temperature"

def cmd(input, expect):
    if input.lower() == expect.lower():
        return True
    return False
