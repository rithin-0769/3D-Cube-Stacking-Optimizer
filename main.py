"""
Main module for 3D Cube Stacking Optimizer.

Handles:
- User input (manual or predefined test cases)
- Running the solver
- Displaying results
- Testing multiple cases
"""

from typing import List, Optional
from solver import CubeStackSolver, compare_solutions
from visualizer import Visualizer, visualize_solution
from utils import create_test_cube
import sys


# ============================================================================
# TEST CASES
# ============================================================================

def get_test_cases() -> List[List[List[str]]]:
    """
    Predefined test cases for demonstration.
    
    Returns:
        List of test cases, each with multiple cubes
    """
    test_cases = []
    
    # Test Case 1: Simple 2-cube case (stackable)
    test_cases.append([
        create_test_cube("R", "B", "G", "Y", "P", "O"),  # Cube 0: Red on top
        create_test_cube("B", "R", "Y", "G", "O", "P"),  # Cube 1: Blue on top (matches Red bottom)
    ])
    
    # Test Case 2: 3 cubes - chain stackable
    test_cases.append([
        create_test_cube("Red", "Blue", "Green", "Yellow", "Purple", "Orange"),
        create_test_cube("Blue", "Green", "Red", "Yellow", "Orange", "Purple"),
        create_test_cube("Green", "Red", "Blue", "Yellow", "Purple", "Orange"),
    ])
    
    # Test Case 3: Multiple cubes with limited stacking
    test_cases.append([
        create_test_cube("A", "B", "C", "D", "E", "F"),
        create_test_cube("B", "C", "A", "D", "E", "F"),
        create_test_cube("C", "D", "A", "B", "E", "F"),
        create_test_cube("D", "A", "B", "C", "E", "F"),
    ])
    
    # Test Case 4: Complex case with alternating colors
    test_cases.append([
        create_test_cube("W", "B", "R", "G", "Y", "P"),
        create_test_cube("B", "W", "G", "R", "P", "Y"),
        create_test_cube("R", "G", "W", "B", "Y", "P"),
        create_test_cube("G", "R", "B", "W", "P", "Y"),
        create_test_cube("Y", "P", "W", "B", "R", "G"),
    ])
    
    # Test Case 5: All same color (impossible to stack - all need matching tops/bottoms)
    test_cases.append([
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
    ])
    
    # Test Case 6: Large case (brute force comparison will skip)
    test_cases.append([
        create_test_cube("C1T", "C1B", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C1B", "C2T", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C2T", "C3T", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C3T", "C4T", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C4T", "C5T", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C5T", "C6T", "C1F", "C1K", "C1L", "C1R"),
        create_test_cube("C6T", "C1T", "C1F", "C1K", "C1L", "C1R"),
    ])
    
    return test_cases


# ============================================================================
# USER INPUT FUNCTIONS
# ============================================================================

def get_cube_from_user() -> Optional[List[str]]:
    """
    Interactively get cube configuration from user with validation.
    
    Returns:
        List of 6 colors for [top, bottom, front, back, left, right]
        or None if user cancels
    """
    print("\nEnter cube configuration (6 colors):")
    print("Format: top bottom front back left right")
    print("Example: Red Blue Green Yellow Purple Orange")
    
    while True:
        try:
            user_input = input("\nCube colors: ").strip()
            
            # Validate input is not empty
            if not user_input:
                print("[ERROR] Input cannot be empty. Please try again.")
                continue
            
            colors = user_input.split()
            
            # Validate exactly 6 colors
            if len(colors) != 6:
                print(f"[ERROR] Expected 6 colors, got {len(colors)}")
                print("Example: Red Blue Green Yellow Purple Orange")
                continue
            
            # Validate no empty colors
            if any(not c.strip() for c in colors):
                print("[ERROR] Color names cannot be empty")
                continue
            
            # Validate color names are alphanumeric
            for i, color in enumerate(colors):
                if not color.replace("_", "").replace("-", "").isalnum():
                    print(f"[ERROR] Invalid color name '{color}' - use alphanumeric only")
                    continue
            
            return colors
            
        except KeyboardInterrupt:
            print("\n[CANCELLED] Input cancelled by user")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            continue


def get_manual_input() -> Optional[List[List[str]]]:
    """
    Get manual cube input from user.
    
    Returns:
        List of cubes or None if user cancels
    """
    print("\n" + "=" * 60)
    print("MANUAL INPUT MODE")
    print("=" * 60)
    
    cubes = []
    cube_num = 1
    
    while True:
        print(f"\n--- Cube {cube_num} ---")
        cube = get_cube_from_user()
        
        if cube is None:
            break
        
        cubes.append(cube)
        cube_num += 1
        
        cont = input(f"\nAdd another cube? (y/n): ").strip().lower()
        if cont != 'y':
            break
    
    if len(cubes) == 0:
        print("❌ No cubes provided")
        return None
    
    return cubes


def display_test_case_menu() -> Optional[List[List[str]]]:
    """
    Display menu for predefined test cases.
    
    Returns:
        Selected test case or None
    """
    test_cases = get_test_cases()
    
    print("\n" + "=" * 60)
    print("SELECT TEST CASE")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n{i + 1}. {len(test_case)} cubes")
        for j, cube in enumerate(test_case):
            print(f"   Cube {j}: {' '.join(cube)}")
    
    print(f"\n{len(test_cases) + 1}. Custom Input")
    print(f"{len(test_cases) + 2}. Run All Test Cases")
    
    while True:
        try:
            choice = input("\nSelect: ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(test_cases):
                return test_cases[choice_num - 1]
            elif choice_num == len(test_cases) + 1:
                return get_manual_input()
            elif choice_num == len(test_cases) + 2:
                return "ALL"
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
        except KeyboardInterrupt:
            return None


# ============================================================================
# SOLVER EXECUTION
# ============================================================================

def solve_and_display(cubes: List[List[str]], show_dp_table: bool = True,
                     show_comparison: bool = False, test_name: str = ""):
    """
    Solve and display results for given cubes.
    
    Args:
        cubes: List of cube configurations
        show_dp_table: Whether to show DP table
        show_comparison: Whether to compare DP vs Brute Force
        test_name: Name of test for display
    """
    if test_name:
        print(f"\n\n{'=' * 80}")
        print(f"TEST: {test_name}")
        print(f"{'=' * 80}")
    
    visualize_solution(
        cubes,
        show_dp_table=show_dp_table,
        show_step_by_step=True,
        show_comparison=show_comparison
    )


def run_all_tests():
    """Run all predefined test cases."""
    test_cases = get_test_cases()
    
    for i, test_case in enumerate(test_cases):
        test_name = f"Test Case {i + 1}: {len(test_case)} Cubes"
        show_comparison = len(test_case) <= 6  # Only compare for small cases
        solve_and_display(test_case, show_comparison=show_comparison, 
                         test_name=test_name)
    
    print(f"\n\n{'=' * 80}")
    print("ALL TESTS COMPLETED")
    print(f"{'=' * 80}")


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    """Main entry point."""
    while True:
        try:
            print("\n" + "=" * 60)
            print("3D CUBE STACKING OPTIMIZER")
            print("=" * 60)
            print("\nOptions:")
            print("1. View test cases")
            print("2. Run all tests")
            print("3. Custom input")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                selected = display_test_case_menu()
                
                if selected is None:
                    continue
                elif selected == "ALL":
                    run_all_tests()
                elif isinstance(selected, list) and len(selected) > 0:
                    show_comp = len(selected) <= 6
                    solve_and_display(selected, show_comparison=show_comp)
            
            elif choice == "2":
                run_all_tests()
            
            elif choice == "3":
                cubes = get_manual_input()
                if cubes:
                    show_comp = len(cubes) <= 6
                    solve_and_display(cubes, show_comparison=show_comp)
            
            elif choice == "4":
                print("\n[EXIT] Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")
        
        except KeyboardInterrupt:
            print("\n\n[EXIT] Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # If command-line args provided, run test case directly
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            run_all_tests()
        elif sys.argv[1] == "--test":
            test_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            test_cases = get_test_cases()
            if 1 <= test_num <= len(test_cases):
                show_comp = len(test_cases[test_num - 1]) <= 6
                solve_and_display(test_cases[test_num - 1], 
                                show_comparison=show_comp,
                                test_name=f"Test Case {test_num}")
            else:
                print(f"❌ Invalid test number: {test_num}")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: python main.py [--all | --test <num>]")
    else:
        # Run interactive mode
        main()
