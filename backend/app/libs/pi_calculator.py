import mpmath 
import concurrent.futures

# Chudnovsky + binary split with mpmath + CPU Parallelization

class PiCalculator: 
    """ Pi calculator using the Chudnovsky algorithm """
    
    def calculate_pi(self, decimal_places: int) -> str:
        self.dps = decimal_places
        mpmath.mp.dps = self.dps + 10  # extra digits for accuracy
        n = self._terms_needed(self.dps)

        P, Q, T = self._parallel_binary_split(0, n)

        C = 426880 * mpmath.sqrt(10005)
        pi = C * Q / T

        return str(+pi)[:self.dps + 2]  # round and slice to desired length

    def _terms_needed(self, decimal_places: int) -> int:
        return int(decimal_places / 14.1816474627254776555) + 1

    def _split_task(self, a, b):
        mpmath.mp.dps = self.dps + 10  # reset in subprocess
        return self._binary_split(a, b)

    def _parallel_binary_split(self, a: int, b: int):
        threshold = 32  # don't parallelize small ranges

        if b - a <= threshold:
            return self._binary_split(a, b)

        mid = (a + b) // 2

        with concurrent.futures.ProcessPoolExecutor() as executor:
            left = executor.submit(self._split_task, a, mid)
            right = executor.submit(self._split_task, mid, b)

            P1, Q1, T1 = left.result()
            P2, Q2, T2 = right.result()

        P = P1 * P2
        Q = Q1 * Q2
        T = T1 * Q2 + P1 * T2

        return (P, Q, T)

    def _binary_split(self, a: int, b: int):
        if b - a == 1:
            k = a
            if k == 0:
                P = Q = mpmath.mpf(1)
            else:
                P = mpmath.mpf((6*k - 5) * (2*k - 1) * (6*k - 1))
                Q = mpmath.mpf(k**3 * 640320**3 // 24)
            T = P * (13591409 + 545140134 * k)
            if k % 2:
                T = -T
            return (P, Q, T)
        else:
            m = (a + b) // 2
            P1, Q1, T1 = self._binary_split(a, m)
            P2, Q2, T2 = self._binary_split(m, b)

            P = P1 * P2
            Q = Q1 * Q2
            T = T1 * Q2 + P1 * T2
            return (P, Q, T)
    
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