import unittest
from unittest.mock import patch
from monitor import (
    is_temperature_ok, is_pulse_rate_ok, is_spo2_ok, 
    vitals_ok, get_vital_alerts, display_alert_animation, display_alerts
)


class ComprehensiveMonitorTest(unittest.TestCase):

    def test_temperature_boundary_conditions(self):
        """Test temperature at exact boundaries"""
        # Normal range boundaries
        self.assertTrue(is_temperature_ok(95.0))    # Lower boundary
        self.assertTrue(is_temperature_ok(102.0))   # Upper boundary
        self.assertTrue(is_temperature_ok(98.6))    # Normal value
        
        # Out of range
        self.assertFalse(is_temperature_ok(94.9))   # Just below lower
        self.assertFalse(is_temperature_ok(102.1))  # Just above upper
        self.assertFalse(is_temperature_ok(90.0))   # Well below
        self.assertFalse(is_temperature_ok(105.0))  # Well above

    def test_pulse_rate_boundary_conditions(self):
        """Test pulse rate at exact boundaries"""
        # Normal range boundaries
        self.assertTrue(is_pulse_rate_ok(60))       # Lower boundary
        self.assertTrue(is_pulse_rate_ok(100))      # Upper boundary
        self.assertTrue(is_pulse_rate_ok(70))       # Normal value
        
        # Out of range
        self.assertFalse(is_pulse_rate_ok(59))      # Just below lower
        self.assertFalse(is_pulse_rate_ok(101))     # Just above upper
        self.assertFalse(is_pulse_rate_ok(40))      # Well below
        self.assertFalse(is_pulse_rate_ok(120))     # Well above

    def test_spo2_boundary_conditions(self):
        """Test SpO2 at exact boundaries"""
        # Normal range boundary
        self.assertTrue(is_spo2_ok(90))             # Lower boundary
        self.assertTrue(is_spo2_ok(95))             # Normal value
        self.assertTrue(is_spo2_ok(100))            # Maximum value
        
        # Out of range
        self.assertFalse(is_spo2_ok(89))            # Just below boundary
        self.assertFalse(is_spo2_ok(85))            # Well below
        self.assertFalse(is_spo2_ok(70))            # Critical low

    def test_get_vital_alerts_single_issues(self):
        """Test alerts for single vital issues"""
        # Single issues
        self.assertEqual(get_vital_alerts(94, 70, 95), ['Temperature critical!'])
        self.assertEqual(get_vital_alerts(103, 70, 95), ['Temperature critical!'])
        self.assertEqual(get_vital_alerts(98, 59, 95), ['Pulse Rate is out of range!'])
        self.assertEqual(get_vital_alerts(98, 101, 95), ['Pulse Rate is out of range!'])
        self.assertEqual(get_vital_alerts(98, 70, 89), ['Oxygen Saturation out of range!'])

    def test_get_vital_alerts_multiple_issues(self):
        """Test alerts for multiple vital issues"""
        # Multiple issues
        self.assertEqual(get_vital_alerts(94, 59, 89), [
            'Temperature critical!',
            'Pulse Rate is out of range!',
            'Oxygen Saturation out of range!'
        ])
        self.assertEqual(get_vital_alerts(103, 101, 95), [
            'Temperature critical!',
            'Pulse Rate is out of range!'
        ])
        self.assertEqual(get_vital_alerts(98, 59, 89), [
            'Pulse Rate is out of range!',
            'Oxygen Saturation out of range!'
        ])

    def test_get_vital_alerts_all_normal(self):
        """Test no alerts when all vitals are normal"""
        self.assertEqual(get_vital_alerts(98.6, 70, 95), [])
        self.assertEqual(get_vital_alerts(95, 60, 90), [])
        self.assertEqual(get_vital_alerts(102, 100, 100), [])

    @patch('monitor.display_alerts')
    def test_vitals_ok_with_normal_values(self, mock_display):
        """Test vitals_ok returns True for normal values without displaying alerts"""
        result = vitals_ok(98.6, 70, 95)
        self.assertTrue(result)
        mock_display.assert_not_called()

    @patch('monitor.display_alerts')
    def test_vitals_ok_with_abnormal_values(self, mock_display):
        """Test vitals_ok returns False for abnormal values and displays alerts"""
        result = vitals_ok(94, 70, 95)
        self.assertFalse(result)
        mock_display.assert_called_once_with(['Temperature critical!'])

    def test_vitals_ok_integration(self):
        """Integration test for vitals_ok function"""
        # This will actually display alerts and animations
        self.assertTrue(vitals_ok(98.6, 70, 95))    # All normal
        self.assertFalse(vitals_ok(94, 70, 95))     # Temperature critical
        self.assertFalse(vitals_ok(98, 59, 95))     # Pulse rate out of range
        self.assertFalse(vitals_ok(98, 70, 89))     # SpO2 out of range

    def test_edge_cases(self):
        """Test edge cases and extreme values"""
        # Test with float values
        self.assertTrue(is_temperature_ok(98.6))
        self.assertTrue(is_pulse_rate_ok(75.5))
        self.assertTrue(is_spo2_ok(95.5))
        
        # Test boundary values
        self.assertTrue(is_temperature_ok(95.0))
        self.assertTrue(is_temperature_ok(102.0))
        self.assertFalse(is_temperature_ok(94.99))
        self.assertFalse(is_temperature_ok(102.01))


if __name__ == '__main__':
    unittest.main()
