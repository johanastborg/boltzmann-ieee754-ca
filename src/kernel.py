import struct
import math

class CollisionKernel:
    """
    Implements the core logic for the Cellular Automaton collision function.

    This kernel incorporates floating-point round-off errors as a source of
    pseudo-randomness (a 'seed') to drive the 2nd Law simulation. By extracting
    the least significant bits of floating-point results, we introduce
    microscopic irreversibility and chaos that mimics thermal fluctuations.
    """

    def __init__(self, chaos_factor=1.0):
        self.chaos_factor = chaos_factor

    def _extract_roundoff_seed(self, value: float) -> int:
        """
        Extracts the lower bits of the floating-point mantissa to serve as a seed.

        Args:
            value (float): The floating point value to inspect.

        Returns:
            int: An integer derived from the least significant bits of the float's representation.
        """
        if value == 0.0:
            return 0

        # Pack the float into 8 bytes (IEEE 754 double precision)
        packed = struct.pack('!d', value)
        # Unpack as a 64-bit unsigned integer
        int_rep = struct.unpack('!Q', packed)[0]

        # We are interested in the "noise" at the bottom of the mantissa.
        # The mantissa is 52 bits. Let's take the lowest 16 bits.
        seed = int_rep & 0xFFFF
        return seed

    def collide(self, cell_value: float, neighbors: list[float]) -> float:
        """
        Calculates the new state of a cell based on its current value and its neighbors.

        The collision logic computes an interaction potential. The floating-point
        arithmetic specifics (round-off) of this potential are used to decide
        how the cell evolves, introducing entropy.

        Args:
            cell_value (float): Current state of the cell.
            neighbors (list[float]): Values of neighboring cells.

        Returns:
            float: The new state of the cell.
        """
        # 1. Calculate a local potential / energy sum
        # We use a multiplier that is likely to produce long mantissas (irrational-ish)
        potential = sum(neighbors) * math.pi + cell_value

        # 2. Extract the "seed" from the floating point round-off of this potential
        # This represents the sensitivity to initial conditions (butterfly effect)
        seed = self._extract_roundoff_seed(potential)

        # 3. Apply the logic based on the seed
        # Use the seed to generate a fluctuation
        # We normalize the seed to a small range centered around 0
        fluctuation = (seed % 101 - 50) / 1000.0  # Small fluctuation

        # 4. Update rule: Relaxation towards average + fluctuation
        avg_neighbors = sum(neighbors) / len(neighbors) if neighbors else 0

        # Diffusive step (smoothing)
        new_value = cell_value + 0.1 * (avg_neighbors - cell_value)

        # Entropy step (chaotic fluctuation based on round-off)
        # This prevents the system from settling into a perfectly uniform state too easily,
        # simulating thermal noise.
        new_value += fluctuation * self.chaos_factor

        # Ensure values stay within reasonable bounds (e.g., non-negative energy)
        return max(0.0, new_value)

    def multi_cell_collision(self, cells: list[float]) -> list[float]:
        """
        Simulates a collision/interaction between multiple cells directly (e.g. partition interaction).
        Preserves total sum (energy) but redistributes it based on round-off seeds.
        """
        total = sum(cells)
        count = len(cells)
        if count == 0:
            return []

        # Calculate a 'complex' interaction value to harvest round-off noise
        interaction_val = 1.0
        for c in cells:
            # Avoid multiplication by zero for the noise seed generation
            interaction_val *= (c + 1.0000001)

        seed = self._extract_roundoff_seed(interaction_val)

        # Generate random weights from the seed using a simple LCG-like step derived from the seed
        weights = []
        current_seed = seed
        for _ in range(count):
            current_seed = (current_seed * 1103515245 + 12345) & 0x7FFFFFFF
            weights.append(float(current_seed))

        total_weight = sum(weights)
        if total_weight == 0:
            return [total / count] * count

        # Redistribute total energy according to these chaotic weights
        new_cells = [(w / total_weight) * total for w in weights]

        return new_cells
