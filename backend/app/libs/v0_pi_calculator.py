import mpmath 

# base, regular Chudnovsky with mpmath

class PiCalculator: 
    """ Pi calculator using the Chudnovsky algorithm """
    
    def calculate_pi(self, decimal_places: int) -> str:
        # Set precision a bit higher to ensure accuracy during calculation
        mpmath.mp.dps = decimal_places + 10  # internal precision buffer
        pi_val = self._chudnovsky_pi()
        
        # Return pi to the requested number of decimal places
        return str(pi_val)[:decimal_places + 2]  # +2 to account for "3."

    def _chudnovsky_pi(self):
        """Internal method to compute pi using the Chudnovsky algorithm"""

        # Constants used in the Chudnovsky algorithm
        C = 426880 * mpmath.sqrt(10005)
        M = 1
        L = 13591409
        X = 1
        K = 6
        S = L

        for i in range(1, mpmath.mp.dps):
            M = M * (K**3 - 16*K) // (i**3)
            L += 545140134
            X *= -262537412640768000
            term = mpmath.mpf(M * L) / X
            S += term
            K += 12

            # Break early if the term is very small
            if abs(term) < mpmath.mpf(10) ** -(mpmath.mp.dps + 5):
                break

        return C / S
    
    def verify_accuracy(self, calculated_pi: str, decimal_places: int) -> bool:
        """
        Verify the accuracy of the calculated pi value by comparing with mpmath's pi.
        
        Args:
            calculated_pi: The calculated value of pi
            decimal_places: Number of decimal places to verify
            
        Returns:
            True if the calculated value matches mpmath's pi to the specified decimal places
        """
        mpmath.mp.dps = decimal_places + 10
        reference_pi = str(mpmath.pi)[:decimal_places + 2]  # +2 accounts for "3."

        if reference_pi != calculated_pi:
            print(f"Reference: {reference_pi}")
            print(f"Calculated: {calculated_pi}")

            # Find how many decimal places match
            match_length = 0
            for i in range(min(len(reference_pi), len(calculated_pi))):
                if reference_pi[i] == calculated_pi[i]:
                    match_length += 1
                else:
                    break
                
            # Subtract 2 to account for "3." at the beginning
            matching_decimals = match_length - 2 if match_length >= 2 else 0
            print(f"Matching decimal places: {matching_decimals} of {decimal_places} requested")

        return calculated_pi == reference_pi