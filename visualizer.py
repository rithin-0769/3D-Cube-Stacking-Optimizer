"""
Visualization module for console-based output.

Provides functions to display:
- Cube configurations
- Stacking sequences
- DP tables
- Solution comparisons
"""

from typing import List, Tuple, Dict, Optional
from solver import CubeStackSolver, BruteForceSolver, compare_solutions
from utils import generate_all_orientations


class Visualizer:
    """Console-based visualizer for cube stacking solutions."""
    
    @staticmethod
    def print_header(text: str, width: int = 80):
        """Print a formatted header."""
        print("\n" + "=" * width)
        print(text.center(width))
        print("=" * width)
    
    @staticmethod
    def print_subheader(text: str, width: int = 80):
        """Print a formatted subheader."""
        print(f"\n{text}")
        print("-" * len(text))
    
    @staticmethod
    def print_cube_info(cubes: List[List[str]]):
        """Display information about input cubes."""
        Visualizer.print_subheader("INPUT CUBES")
        for i, cube in enumerate(cubes):
            top, bottom, front, back, left, right = cube
            print(f"\nCube {i}:")
            print(f"  Top:    {top}")
            print(f"  Bottom: {bottom}")
            print(f"  Front:  {front}, Back:  {back}")
            print(f"  Left:   {left}, Right: {right}")
            
            orientations = generate_all_orientations(cube)
            print(f"  Orientations: {len(orientations)}")
            for j, (top_o, bottom_o) in enumerate(orientations):
                print(f"    {j+1}. Top: {top_o:10} -> Bottom: {bottom_o:10}")
    
    @staticmethod
    def print_solution(solver: CubeStackSolver, cubes: List[List[str]]):
        """Display the solution from a DP solver."""
        Visualizer.print_subheader("SOLUTION")
        
        max_height = solver.max_height
        sequence = solver.get_stacking_sequence()
        
        print(f"\n[HEIGHT] Maximum Tower Height: {max_height}")
        print(f"\n[SEQUENCE] Stacking Sequence (Bottom to Top):")
        
        for idx, (cube_i, orient_j) in enumerate(sequence):
            orientations = generate_all_orientations(cubes[cube_i])
            top, bottom = orientations[orient_j]
            
            indent = "  " * idx
            if idx == 0:
                print(f"{indent}[Base] Cube {cube_i} (Orientation {orient_j})")
                print(f"{indent}       Top: {top}")
            else:                
                print(f"{indent}+-- On top: Cube {cube_i} (Orientation {orient_j})")
                print(f"{indent}    Bottom: {bottom}")
                if idx < len(sequence) - 1:
                    print(f"{indent}    Top:    {top}")
                else:
                    print(f"{indent}    Top:    {top}")
    
    @staticmethod
    def print_solution_compact(solver: CubeStackSolver, cubes: List[List[str]]):
        """Display solution in compact format."""
        Visualizer.print_subheader("COMPACT VIEW")
        
        sequence = solver.get_stacking_sequence()
        cube_indices = [str(idx) for idx, _ in sequence]
        orient_indices = [str(orient) for _, orient in sequence]
        
        print(f"Cube sequence:      {' -> '.join(cube_indices)}")
        print(f"Orientation usage:  {' -> '.join(orient_indices)}")
        print(f"Height achieved:    {len(sequence)}")
    
    @staticmethod
    def print_dp_table(solver: CubeStackSolver):
        """Display the DP table."""
        print(solver.get_dp_table_display())
    
    @staticmethod
    def print_comparison(results: Dict):
        """Display comparison between DP and Brute Force."""
        Visualizer.print_header("DP vs BRUTE FORCE COMPARISON")
        
        print(f"\nProblem Size: {results['num_cubes']} cubes")
        print(f"\nResults:")
        print(f"  DP Solution Height:        {results['dp_height']}")
        print(f"  Brute Force Height:        {results['bf_height']}")
        print(f"  Solutions Match:           {results['match']}")
        
        print(f"\nExecution Time:")
        print(f"  DP Time:                   {results['dp_time']:.6f} seconds")
        print(f"  Brute Force Time:          {results['bf_time']}")
        
        if isinstance(results['bf_time'], float) and results['dp_time'] > 0:
            speedup = results['bf_time'] / results['dp_time']
            print(f"  Speedup Factor:            {speedup:.2f}x faster")
        
        print(f"\nComplexity Analysis:")
        print(f"  DP Complexity:             O(n² × m²) ≈ O({results['num_cubes']}² × 6²)")
        print(f"  Brute Force Complexity:    O((n×m)!) ≈ O(({results['num_cubes']}×6)!)")
        print(f"  Improvement:               Exponential speedup")
    
    @staticmethod
    def print_step_by_step(solver: CubeStackSolver, cubes: List[List[str]]):
        """Show step-by-step visualization of building the tower."""
        Visualizer.print_subheader("STEP-BY-STEP TOWER BUILDING")
        
        sequence = solver.get_stacking_sequence()
        
        for step_num, (cube_i, orient_j) in enumerate(sequence):
            orientations = generate_all_orientations(cubes[cube_i])
            top, bottom = orientations[orient_j]
            
            print(f"\nStep {step_num + 1}:")
            print(f"  Place Cube {cube_i} (Orientation {orient_j})")
            print(f"  Bottom face: {bottom}, Top face: {top}")
            
            if step_num > 0:
                prev_cube_i, prev_orient_j = sequence[step_num - 1]
                prev_orientations = generate_all_orientations(cubes[prev_cube_i])
                prev_top, _ = prev_orientations[prev_orient_j]
                print(f"  ✓ Valid placement: {prev_top} (below) == {bottom} (bottom of new cube)")
            
            # Draw pyramid
            pyramid = " " * (len(sequence) - step_num - 1) + "█" * (step_num + 1)
            print(f"  Tower: {pyramid}")
    
    @staticmethod
    def print_performance_stats(num_cubes: int, orientations_per_cube: int = 6):
        """Print theoretical performance statistics."""
        Visualizer.print_subheader("PERFORMANCE STATISTICS")
        
        total_states = num_cubes * orientations_per_cube
        dp_ops = total_states * total_states
        bf_ops = 1
        for i in range(num_cubes):
            bf_ops *= orientations_per_cube
        
        print(f"\nProblem Parameters:")
        print(f"  Number of cubes:           {num_cubes}")
        print(f"  Orientations per cube:     {orientations_per_cube}")
        print(f"  Total possible states:     {total_states}")
        
        print(f"\nDP Algorithm:")
        print(f"  Approximate operations:    {dp_ops:,}")
        print(f"  Time Complexity:           O(n² × m²) where n={num_cubes}, m={orientations_per_cube}")
        
        print(f"\nBrute Force Algorithm:")
        print(f"  Approximate permutations:  {bf_ops:,}")
        print(f"  Time Complexity:           O((n × m)!) for {num_cubes} cubes")
        
        if bf_ops > 0 and dp_ops > 0:
            improvement = bf_ops / dp_ops
            print(f"\nEfficiency Improvement:    {improvement:.2e}x faster with DP")


def visualize_solution(cubes: List[List[str]], show_dp_table: bool = True, 
                      show_step_by_step: bool = True,
                      show_comparison: bool = False):
    """
    Complete visualization pipeline.
    
    Args:
        cubes: List of cube configurations
        show_dp_table: Whether to display DP table details
        show_step_by_step: Whether to show step-by-step building
        show_comparison: Whether to compare with brute force
    """
    Visualizer.print_header("3D CUBE STACKING OPTIMIZER")
    
    # Show input
    Visualizer.print_cube_info(cubes)
    
    # Solve
    solver = CubeStackSolver(cubes)
    solver.solve()
    
    # Show solution
    Visualizer.print_solution(solver, cubes)
    Visualizer.print_solution_compact(solver, cubes)
    
    # Show details
    if show_dp_table:
        Visualizer.print_dp_table(solver)
    
    if show_step_by_step:
        Visualizer.print_step_by_step(solver, cubes)
    
    # Show comparison
    if show_comparison:
        results = compare_solutions(cubes)
        Visualizer.print_comparison(results)
    
    # Show stats
    Visualizer.print_performance_stats(len(cubes))
    
    Visualizer.print_header("VISUALIZATION COMPLETE")


if __name__ == "__main__":
    from utils import create_test_cube
    
    # Test visualization
    test_cubes = [
        create_test_cube("R", "B", "G", "Y", "P", "O"),
        create_test_cube("B", "R", "Y", "G", "O", "P"),
        create_test_cube("G", "Y", "R", "B", "P", "O")
    ]
    
    visualize_solution(test_cubes, show_comparison=True)
