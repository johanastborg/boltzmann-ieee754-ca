import random
import time
from src.kernel import CollisionKernel

class Simulation:
    def __init__(self, width=20, height=20, steps=100):
        self.width = width
        self.height = height
        self.steps = steps
        self.grid = [[random.random() * 10.0 for _ in range(width)] for _ in range(height)]
        self.kernel = CollisionKernel(chaos_factor=1.5)

    def get_neighbors(self, x, y):
        neighbors = []
        # Von Neumann neighborhood with wrap-around (toroidal)
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            nx, ny = (x + dx) % self.width, (y + dy) % self.height
            neighbors.append(self.grid[ny][nx])
        return neighbors

    def step(self):
        new_grid = [[0.0 for _ in range(self.width)] for _ in range(self.height)]

        # In a real synchronous CA, we read from old grid and write to new grid
        for y in range(self.height):
            for x in range(self.width):
                cell_val = self.grid[y][x]
                neighbors = self.get_neighbors(x, y)
                new_val = self.kernel.collide(cell_val, neighbors)
                new_grid[y][x] = new_val

        self.grid = new_grid

    def run(self):
        print(f"Starting simulation on {self.width}x{self.height} grid for {self.steps} steps.")
        print("Initial state (center 3x3):")
        self.print_center()

        for i in range(self.steps):
            self.step()

        print(f"\nFinal state after {self.steps} steps (center 3x3):")
        self.print_center()

        # Calculate total energy to check drift (should be roughly conserved or drifting due to our noise)
        total_energy = sum(sum(row) for row in self.grid)
        print(f"\nTotal System Energy: {total_energy:.4f}")

    def print_center(self):
        cy, cx = self.height // 2, self.width // 2
        for y in range(cy - 1, cy + 2):
            row_str = " ".join(f"{self.grid[y][x]:.2f}" for x in range(cx - 1, cx + 2))
            print(f"[ {row_str} ]")

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
