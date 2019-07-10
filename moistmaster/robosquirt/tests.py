from unittest import TestCase
from unittest.mock import patch

from robosquirt import solenoid


class ValveTest(TestCase):

    @patch("robosquirt.solenoid.OutputPin")
    def test_valve(self, mock_pin):

        test_valve = solenoid.Valve(0)
        self.assertFalse(test_valve.is_open)
        self.assertEqual(test_valve.status, "closed")

        test_valve.open()
        self.assertTrue(test_valve.is_open)
        self.assertEqual(test_valve.status, "open")
        test_valve.pin.send_high.assert_called_once()

        test_valve.close()
        self.assertFalse(test_valve.is_open)
        test_valve.pin.send_low.assert_called_once()

        test_valve.toggle()  # Toggling opens the valve again.
        self.assertTrue(test_valve.is_open)
        self.assertEqual(test_valve.pin.send_high.call_count, 2)

        test_valve.toggle()  # Toggling again closes the valve.
        self.assertFalse(test_valve.is_open)
        self.assertEqual(test_valve.pin.send_low.call_count, 2)

        test_valve.test()
        self.assertFalse(test_valve.is_open)

        self.assertEqual(test_valve.real_status, "closed")
