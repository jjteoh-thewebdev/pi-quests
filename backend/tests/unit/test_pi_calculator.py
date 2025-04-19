import pytest
from app.libs.pi_calculator import PiCalculator


class TestPiCalculator:
    """Test cases for the Pi calculator."""
    
    def setup_method(self):
        """Setup method run before each test."""
        self.calculator = PiCalculator()
        
        # First 100 digits of Pi for testing
        self.known_pi_100 = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    
    def test_calculate_pi_small_precision(self):
        """Test calculating Pi to a small precision (10 places)."""
        pi_value = self.calculator.calculate_pi(10)
        assert pi_value.startswith("3.14159265")
        assert len(pi_value) == 12  # 3.1415926535 (10 decimal places + '3' + '.')
    
    def test_calculate_pi_medium_precision(self):
        """Test calculating Pi to a medium precision (50 places)."""
        pi_value = self.calculator.calculate_pi(50)
        expected = self.known_pi_100[:52]  # 3.141592... (50 decimal places + '3' + '.')
        assert pi_value.startswith(expected)
        assert len(pi_value) == 52  # 50 decimal places + '3' + '.'
    
    def test_calculate_pi_large_precision(self):
        """Test calculating Pi to a large precision (100 places)."""
        pi_value = self.calculator.calculate_pi(100)
        expected = self.known_pi_100
        assert pi_value.startswith(expected)
        assert len(pi_value) == 102  # 100 decimal places + '3' + '.'
    
    def test_validate_pi(self):
        """Test validating a calculated Pi value."""
        # Test with a valid Pi value
        valid_pi = "3.14159265358979323846"
        assert self.calculator.validate_pi(valid_pi, 20) is True
        
        # Test with an invalid Pi value
        invalid_pi = "3.14159265358979323847"  # Last digit changed
        assert self.calculator.validate_pi(invalid_pi, 20) is False 