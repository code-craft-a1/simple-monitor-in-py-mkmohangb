from time import sleep
import sys


def is_temperature_ok(temperature):
    """Check if temperature is within normal range (95-102°F)"""
    return 95 <= temperature <= 102


def is_pulse_rate_ok(pulse_rate):
    """Check if pulse rate is within normal range (60-100 bpm)"""
    return 60 <= pulse_rate <= 100


def is_spo2_ok(spo2):
    """Check if SpO2 is within normal range (>=90%)"""
    return spo2 >= 90


def get_vital_alerts(temperature, pulse_rate, spo2):
    """Get list of alert messages for out-of-range vitals"""
    alerts = []
    
    if not is_temperature_ok(temperature):
        alerts.append('Temperature critical!')
    
    if not is_pulse_rate_ok(pulse_rate):
        alerts.append('Pulse Rate is out of range!')
    
    if not is_spo2_ok(spo2):
        alerts.append('Oxygen Saturation out of range!')
    
    return alerts


def display_alert_animation():
    """Display the alert animation"""
    for i in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)


def display_alerts(alerts):
    """Display alerts with animation"""
    for alert in alerts:
        print(alert)
        display_alert_animation()


def vitals_ok(temperature, pulse_rate, spo2):
    """Check if all vitals are within normal range and display alerts if not"""
    alerts = get_vital_alerts(temperature, pulse_rate, spo2)
    
    if alerts:
        display_alerts(alerts)
        return False
    
    return True
