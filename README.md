# Cellular Automaton with Floating-Point Round-Off Kernel

This project implements a unique Cellular Automaton (CA) where the collision function logic is driven by the microscopic "noise" inherent in floating-point arithmetic.

## Concept

In standard computational physics, floating-point round-off errors are usually considered a nuisance to be minimized. However, in this "2nd Law simulation", we explicitly harvest these round-off errors (extracted from the least significant bits of the mantissa) and use them as a "seed" for the stochastic evolution of the system.

This mimics the physical reality where microscopic chaos and uncertainty (quantum fluctuations, thermal noise) drive the macroscopic emergence of the Second Law of Thermodynamics (entropy increase).

## Kernel Logic

The core logic is located in `src/kernel.py`.

The `CollisionKernel` class performs the following:
1.  **Interaction Calculation**: Computes a potential based on the cell and its neighbors.
2.  **Round-Off Extraction**: Inspects the IEEE 754 floating-point representation of the result to extract the lowest bits of the mantissa.
3.  **Stochastic Update**: Uses these bits as a pseudo-random seed to introduce fluctuations in the cell's value, breaking time-reversibility and simulating entropy.

## Running the Simulation

To run the simulation:

```bash
python3 -m src.simulation
```

This will initialize a random grid and evolve it, printing the state of the center cells before and after the simulation.

## Structure

*   `src/kernel.py`: Contains the `CollisionKernel` logic.
*   `src/simulation.py`: A simple grid-based CA simulation runner.
*   `tests/`: Contains unit tests.
