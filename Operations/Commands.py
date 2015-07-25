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
ARDUINO_RELAY = "ArduinoRelay"
ARDUINO_RESPONSE = "ArduinoResponse"

# Sensor Commands
HUMIDITY = "Humidity"
GPS = "GPS"
BAROMETER = "Barometer"
TIMESTAMP = "Timestamp"

# Arduino Commands
ARDUINO_GPS = "G"
ARDUINO_TIMESTAMP = "T"
ARDUINO_BAROMETER = "B"
ARDUINO_HUMIDITY = "H"

def cmd(input, expect):
    if input.lower() == expect.lower():
        return True
    return False
