from time import sleep
import sys


def is_temperature_ok(temperature):
    """Checks if temperature is within the normal range."""
    return 95 <= temperature <= 102

def is_pulse_rate_ok(pulse_rate):
    """Checks if pulse rate is within the normal range."""
    return 60 <= pulse_rate <= 100

def is_spo2_ok(spo2):
    """Checks if oxygen saturation is within the normal range."""
    return spo2 >= 90

def vitals_ok(temperature, pulseRate, spo2):
  return is_temperature_ok(temperature) and is_pulse_rate_ok(pulseRate) and is_spo2_ok(spo2)

def get_vital_alerts(temperature, pulse_rate, spo2):
    """
    Checks all vitals and returns a list of alert messages for abnormal vitals.
    This function is data-driven to reduce complexity.
    """
    vital_checks = [
        (is_temperature_ok, temperature, 'Temperature critical!'),
        (is_pulse_rate_ok, pulse_rate, 'Pulse Rate is out of range!'),
        (is_spo2_ok, spo2, 'Oxygen Saturation out of range!')
    ]
    return [message for check, value, message in vital_checks if not check(value)]

def print_alerts(alerts):
    """Prints alerts to the console with an animation."""
    for alert in alerts:
        print(alert)
        for _ in range(6):
            print('\r* ', end='')
            sys.stdout.flush()
            sleep(0.1)
            print('\r *', end='')
            sys.stdout.flush()
            sleep(0.1)
        print()