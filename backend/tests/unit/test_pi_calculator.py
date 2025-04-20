from app.libs.pi_calculator import PiCalculator


class TestPiCalculator:
    """Test cases for the Pi calculator."""
    
    def setup_method(self):
        """Setup method run before each test."""
        self.calculator = PiCalculator()
    
    def test_calculate_pi_small_precision(self):
        """Test calculating Pi to a small precision (10 places)."""
        pi_value = self.calculator.calculate_pi(10)
        assert self.calculator.verify_accuracy(pi_value, 10)
        assert len(pi_value) == 12  
    
    def test_calculate_pi_medium_precision(self):
        """Test calculating Pi to a medium precision (50 places)."""
        pi_value = self.calculator.calculate_pi(1000)
        assert self.calculator.verify_accuracy(pi_value, 1000)
        assert len(pi_value) == 1002
    
    def test_calculate_pi_large_precision(self):
        """Test calculating Pi to a large precision (100 places)."""
        pi_value = self.calculator.calculate_pi(10000)
        assert self.calculator.verify_accuracy(pi_value, 10000)
        assert len(pi_value) == 10002
    