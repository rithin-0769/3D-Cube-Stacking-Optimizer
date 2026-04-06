"""
Core solver module using Dynamic Programming approach.

Implements the Longest Increasing Subsequence (LIS) variant:
- dp[i] = maximum height of stack ending at cube i with orientation j
- For each cube, we try all orientations
- We can stack cube i on cube k if colors match

Time Complexity: O(n² * m²) where n=number of cubes, m=orientations per cube
Space Complexity: O(n * m) for DP table and parent tracking
"""

from typing import List, Tuple, Optional, Dict
from utils import generate_all_orientations, validate_stacking
import time


class CubeStackSolver:
    """Solves the 3D Cube Stacking problem using Dynamic Programming."""
    
    def __init__(self, cubes: List[List[str]]):
        """
        Initialize solver with list of cubes.
        
        Args:
            cubes: List of cubes, each cube is [top, bottom, front, back, left, right]
        """
        self.cubes = cubes
        self.num_cubes = len(cubes)
        
        # Pre-generate all orientations for all cubes
        self.orientations: List[List[Tuple[str, str]]] = []
        for cube in cubes:
            self.orientations.append(generate_all_orientations(cube))
        
        # DP table and tracking
        self.dp: List[int] = []
        self.parent: List[Optional[Tuple[int, int]]] = []
        self.max_height = 0
        self.best_state = None
    
    def solve(self) -> int:
        """
        Solve using Dynamic Programming (Longest Increasing Subsequence variant).
        
        PROBLEM TRANSFORMATION:
        Classic LIS: Find longest increasing sequence in array of numbers
        Our variant: Find longest "stackable" sequence in array of cubes with orientations
        
        KEY INSIGHT:
        - Instead of comparing numbers (a[i] < a[j]), we compare colors
        - If top_color[cube_k] == bottom_color[cube_i], we CAN stack i on k
        - This creates a valid ordering constraint just like a > b in LIS
        
        ALGORITHM (Classic DP Pattern):
        1. Initialize dp[state] = 1 (base case: each cube alone is height 1)
        2. For each current state (cube i, orientation j):
           For each previous state (cube k, orientation l):
              If constraint satisfied (colors match):
                 dp[current] = max(dp[current], dp[previous] + 1)
        3. Track parent to reconstruct solution
        4. Return maximum dp value
        
        TIME COMPLEXITY: O(n² × m²)
          - n = number of cubes
          - m = orientations per cube (always 6)
          - Two nested loops over cubes and orientations
        
        SPACE COMPLEXITY: O(n × m)
          - DP array stores one value per state
          - Parent array for reconstruction
        
        Returns:
            Maximum height achievable
        """
        if self.num_cubes == 0:
            return 0
        
        # Initialize DP arrays
        # State indexing: each (cube, orientation) pair gets unique index
        # dp is indexed as: cube_idx * len(orientations) + orientation_idx
        total_states = sum(len(orients) for orients in self.orientations)
        
        self.dp = [1] * total_states  # Base case: height 1 for each state
        self.parent = [None] * total_states  # For reconstruction
        
        self.max_height = 1
        self.best_state = 0
        
        # DP TABLE FILLING: Process all cubes in order (ensure i < k)
        # Standard two-pointer pattern from LIS algorithm
        for i in range(self.num_cubes):
            for j, (top_i, bottom_i) in enumerate(self.orientations[i]):
                state_i = self._get_state_idx(i, j)
                
                # CONSTRAINT CHECK: Try to extend from all previous states
                # This is the core of the LIS pattern - checking if we can extend
                for k in range(i):  # Only check earlier cubes (no cycles)
                    for l, (top_k, bottom_k) in enumerate(self.orientations[k]):
                        state_k = self._get_state_idx(k, l)
                        
                        # STACKING CONDITION: Can only stack if colors match
                        # This replaces the "a[k] < a[i]" condition from classic LIS
                        if validate_stacking(top_k, bottom_i):
                            # TRANSITION: Add 1 to previous height
                            new_height = self.dp[state_k] + 1
                            
                            # RELAXATION: Keep maximum (standard DP relaxation)
                            if new_height > self.dp[state_i]:
                                self.dp[state_i] = new_height
                                self.parent[state_i] = (k, l)  # Remember choice
                
                # Track global maximum
                if self.dp[state_i] > self.max_height:
                    self.max_height = self.dp[state_i]
                    self.best_state = state_i
        
        return self.max_height
    
    def get_stacking_sequence(self) -> List[Tuple[int, int]]:
        """
        Reconstruct the sequence of cubes to stack.
        
        Returns:
            List of (cube_index, orientation_index) tuples in bottom-to-top order
        """
        if self.best_state is None or self.num_cubes == 0:
            return []
        
        sequence = []
        current_state = self.best_state
        
        while current_state is not None:
            cube_idx, orient_idx = self._decode_state_idx(current_state)
            sequence.append((cube_idx, orient_idx))
            
            if self.parent[current_state] is None:
                break
            
            cube_idx_next, orient_idx_next = self.parent[current_state]
            current_state = self._get_state_idx(cube_idx_next, orient_idx_next)
        
        return list(reversed(sequence))
    
    def _get_state_idx(self, cube_idx: int, orient_idx: int) -> int:
        """Convert (cube_idx, orient_idx) to linear state index."""
        offset = 0
        for i in range(cube_idx):
            offset += len(self.orientations[i])
        return offset + orient_idx
    
    def _decode_state_idx(self, state_idx: int) -> Tuple[int, int]:
        """Convert linear state index back to (cube_idx, orient_idx)."""
        offset = 0
        for i in range(self.num_cubes):
            if offset + len(self.orientations[i]) > state_idx:
                return (i, state_idx - offset)
            offset += len(self.orientations[i])
        return (0, 0)
    
    def get_dp_table_display(self) -> str:
        """
        Return a formatted string of the DP table for debugging.
        
        Returns:
            Formatted DP table as string
        """
        if not self.dp:
            return "DP table not computed yet"
        
        output = []
        output.append("\n" + "=" * 80)
        output.append("DYNAMIC PROGRAMMING TABLE")
        output.append("=" * 80)
        
        for i in range(self.num_cubes):
            output.append(f"\nCube {i}:")
            for j, (top, bottom) in enumerate(self.orientations[i]):
                state_idx = self._get_state_idx(i, j)
                height = self.dp[state_idx]
                parent_info = ""
                if self.parent[state_idx] is not None:
                    pk, pl = self.parent[state_idx]
                    parent_info = f" (from Cube {pk}, Orient {pl})"
                
                marker = " <-- MAX" if state_idx == self.best_state else ""
                output.append(f"  Orient {j} (Top: {top:10} -> Bottom: {bottom:10}): "
                            f"Height = {height}{parent_info}{marker}")
        
        return "\n".join(output)


class BruteForceSolver:
    """Brute force solver for comparison and validation."""
    
    def __init__(self, cubes: List[List[str]]):
        """Initialize brute force solver."""
        self.cubes = cubes
        self.num_cubes = len(cubes)
        self.orientations: List[List[Tuple[str, str]]] = []
        
        for cube in cubes:
            self.orientations.append(generate_all_orientations(cube))
        
        self.max_height = 0
        self.best_sequence = []
    
    def solve(self) -> int:
        """
        Solve using brute force recursion.
        
        Time Complexity: O((n*m)!) in worst case where n=cubes, m=orientations
        """
        self.best_sequence = []
        self.max_height = 0
        
        # Try all permutations of cubes with all possible orientations
        self._backtrack([], set())
        
        return self.max_height
    
    def _backtrack(self, sequence: List[Tuple[int, int]], used: set):
        """Recursively try all valid cube placements."""
        # Update best sequence
        if len(sequence) > self.max_height:
            self.max_height = len(sequence)
            self.best_sequence = sequence.copy()
        
        # Try adding each unused cube
        for cube_idx in range(self.num_cubes):
            if cube_idx in used:
                continue
            
            # Try all orientations
            for orient_idx, (top, bottom) in enumerate(self.orientations[cube_idx]):
                can_place = True
                
                if sequence:
                    # Check if can stack on top of last cube
                    last_cube_idx, last_orient_idx = sequence[-1]
                    last_top, last_bottom = self.orientations[last_cube_idx][last_orient_idx]
                    
                    if not validate_stacking(last_top, bottom):
                        can_place = False
                
                if can_place:
                    sequence.append((cube_idx, orient_idx))
                    used.add(cube_idx)
                    self._backtrack(sequence, used)
                    sequence.pop()
                    used.remove(cube_idx)
    
    def get_best_sequence(self) -> List[Tuple[int, int]]:
        """Get the best sequence found by brute force."""
        return self.best_sequence


def compare_solutions(cubes: List[List[str]]) -> Dict:
    """
    Compare DP and Brute Force solutions with timing.
    
    Returns:
        Dictionary with results and timing information
    """
    results = {
        'num_cubes': len(cubes),
        'dp_height': 0,
        'bf_height': 0,
        'dp_time': 0,
        'bf_time': 0,
        'dp_sequence': [],
        'bf_sequence': [],
        'match': False
    }
    
    # Run DP solution
    dp_solver = CubeStackSolver(cubes)
    start = time.time()
    results['dp_height'] = dp_solver.solve()
    results['dp_time'] = time.time() - start
    results['dp_sequence'] = dp_solver.get_stacking_sequence()
    
    # Only run brute force for small inputs (n <= 6)
    if len(cubes) <= 6:
        bf_solver = BruteForceSolver(cubes)
        start = time.time()
        results['bf_height'] = bf_solver.solve()
        results['bf_time'] = time.time() - start
        results['bf_sequence'] = bf_solver.get_best_sequence()
        results['match'] = results['dp_height'] == results['bf_height']
    else:
        results['bf_height'] = "N/A (too large)"
        results['bf_time'] = "N/A"
        results['bf_sequence'] = []
        results['match'] = "N/A"
    
    return results


if __name__ == "__main__":
    from utils import create_test_cube
    
    print("=" * 60)
    print("SOLVER TEST")
    print("=" * 60)
    
    # Test case 1: Simple 2 cubes
    test_cubes = [
        create_test_cube("R", "B", "G", "Y", "P", "O"),
        create_test_cube("B", "R", "Y", "G", "O", "P")
    ]
    
    print("\nTest Case: 2 Cubes")
    solver = CubeStackSolver(test_cubes)
    height = solver.solve()
    print(f"Maximum Height: {height}")
    print(f"Sequence: {solver.get_stacking_sequence()}")
    print(solver.get_dp_table_display())
