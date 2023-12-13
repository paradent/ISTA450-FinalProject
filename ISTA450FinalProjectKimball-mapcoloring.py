"""
ISTA450 Final Project
Tyler Kimball
Fall 2023
Map Coloring CSP with backtracking and forward checking
"""
import time

class MapColoring:
    def __init__(self, regions, adjacent, algorithm='backtracking'):
        self.regions = regions
        self.adjacent = adjacent
        self.colors = {}
        self.remaining_colors = {region: set(range(1, len(regions) + 1)) for region in regions}
        self.algorithm = algorithm

    def is_safe(self, region, color):
        for neighbor in self.adjacent[region]:
            if neighbor in self.colors and self.colors[neighbor] == color:
                return False
        return True

    def forward_check(self, region, color):
        for neighbor in self.adjacent[region]:
            if neighbor not in self.colors and color in self.remaining_colors[neighbor]:
                self.remaining_colors[neighbor].remove(color)
                if not self.remaining_colors[neighbor]:
                    return False
        return True

    def color_map(self, region):
        for color in self.remaining_colors[region].copy():
            if self.is_safe(region, color):

                self.colors[region] = color
                if len(self.colors) == len(self.regions):
                    return True
                next_region = [r for r in self.regions if r not in self.colors][0]
    
                if self.algorithm == 'forwardchecking':
                    if not self.forward_check(region, color):
                        continue
                if self.color_map(next_region):
                    return True
                # Backtrack
                del self.colors[region]
                self.remaining_colors[region] = set(range(1, len(self.regions) + 1))
        return False

    def solve(self):
        start_region = self.regions[0]
        return self.color_map(start_region)


def measure_time(problem):
    start_time = time.time()
    assignments_before = len(problem.colors)
    problem.solve()
    end_time = time.time()
    assignments_after = len(problem.colors)

    return end_time - start_time, assignments_after - assignments_before

def main():
    regions = ["Phoenix", "Tucson", "Flagstaff", "Yuma", "Prescott", "Sedona"]
    adjacent = {
        "Phoenix": ["Tucson", "Flagstaff", "Yuma", "Prescott", "Sedona"],
        "Tucson": ["Phoenix", "Flagstaff"],
        "Flagstaff": ["Phoenix", "Tucson", "Prescott"],
        "Yuma": ["Phoenix", "Sedona"],
        "Prescott": ["Phoenix", "Flagstaff", "Sedona"],
        "Sedona": ["Phoenix", "Yuma", "Prescott"],
}

    backtracking = MapColoring(regions, adjacent, algorithm='backtracking')
    forwardchecking = MapColoring(regions, adjacent, algorithm='forwardchecking')

    backtracking_time, backtracking_assignments = measure_time(backtracking)
    forwardchecking_time, forwardchecking_assignments = measure_time(forwardchecking)

    print("Backtracking - Colors assigned:\n")
    for city, color in backtracking.colors.items():
        print(f"{city}: Color {color}")

    print("\nBacktracking:")
    print(f"Time: {backtracking_time:.6f} seconds")
    print(f"Assignments: {backtracking_assignments}")
    print("\n--------------------------------\n")

    print("Forward Checking: - Colors assigned:\n")
    for city, color in forwardchecking.colors.items():
        print(f"{city}: Color {color}")
        
    print("\nForward Checking:")
    print(f"Time: {forwardchecking_time:.6f} seconds")
    print(f"Assignments: {forwardchecking_assignments}")
    print("\n--------------------------------\n")

    if backtracking_time < forwardchecking_time:
        print("Backtracking is faster")
    elif backtracking_time > forwardchecking_time:
        print("Forward Checking is faster")
    else:
        print("Both algorithms have similar performance")


if __name__ == "__main__":
    main()
    







