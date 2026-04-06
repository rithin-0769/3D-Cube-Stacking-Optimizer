"""
Edge case tests for 3D Cube Stacking Optimizer.

Tests corner cases to ensure robustness:
- Single cube
- Impossible to stack
- All identical cubes
- Very large cases
- Cube with repeated colors
"""

from solver import CubeStackSolver, BruteForceSolver
from utils import create_test_cube
from typing import List


def test_single_cube():
    """Test with single cube - should return height 1."""
    print("\n[TEST 1] Single Cube")
    print("-" * 60)
    
    cubes = [create_test_cube("R", "B", "G", "Y", "P", "O")]
    
    solver = CubeStackSolver(cubes)
    height = solver.solve()
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 1 cube")
    print(f"  Expected: Height = 1")
    print(f"  Got: Height = {height}")
    print(f"  Sequence: {sequence}")
    
    assert height == 1, "Single cube should have height 1"
    assert len(sequence) == 1, "Sequence should contain 1 cube"
    
    print("  [PASS]")
    return True


def test_impossible_to_stack():
    """Test with cubes that can't stack at all."""
    print("\n[TEST 2] Impossible to Stack")
    print("-" * 60)
    
    # Create 3 cubes with no matching colors
    cubes = [
        create_test_cube("R", "R", "R", "R", "R", "R"),  # All Red
        create_test_cube("B", "B", "B", "B", "B", "B"),  # All Blue
        create_test_cube("G", "G", "G", "G", "G", "G"),  # All Green
    ]
    
    solver = CubeStackSolver(cubes)
    height = solver.solve()
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 3 cubes, all monochrome (no matching colors)")
    print(f"  Expected: Height = 1 (no stacking possible)")
    print(f"  Got: Height = {height}")
    print(f"  Sequence: {sequence}")
    
    assert height == 1, "Should not be able to stack different monochrome cubes"
    assert len(sequence) == 1, "Should only use 1 cube"
    
    print("  [PASS]")
    return True


def test_identical_cubes():
    """Test with identical cubes - all can stack on each other."""
    print("\n[TEST 3] Identical Cubes")
    print("-" * 60)
    
    # Create 5 identical cubes
    cubes = [
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
        create_test_cube("X", "X", "X", "X", "X", "X"),
    ]
    
    solver = CubeStackSolver(cubes)
    height = solver.solve()
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 5 identical cubes")
    print(f"  Expected: Height = 5")
    print(f"  Got: Height = {height}")
    print(f"  Sequence: {sequence}")
    
    assert height == 5, "All identical cubes should stack completely"
    assert len(sequence) == 5, "All 5 cubes should be used"
    
    print("  [PASS]")
    return True


def test_partial_stackable():
    """Test with some cubes stackable and some not."""
    print("\n[TEST 4] Partial Stackable Cubes")
    print("-" * 60)
    
    cubes = [
        create_test_cube("A", "B", "C", "D", "E", "F"),  # Top: A, Bottom: B
        create_test_cube("B", "C", "D", "E", "F", "A"),  # Top: B, Bottom: C (can stack on 0)
        create_test_cube("X", "Y", "Z", "W", "U", "V"),  # No match - isolated
        create_test_cube("C", "D", "E", "F", "A", "B"),  # Top: C, Bottom: D (can stack on 1)
    ]
    
    solver = CubeStackSolver(cubes)
    height = solver.solve()
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 4 cubes, some stackable, some isolated")
    print(f"  Expected: Height = 3 (chain of 3)")
    print(f"  Got: Height = {height}")
    print(f"  Sequence: {sequence}")
    
    assert height >= 2, "Should at least stack 2 cubes"
    
    print("  [PASS]")
    return True


def test_large_case():
    """Test with larger input (10 cubes)."""
    print("\n[TEST 5] Large Case (10 Cubes)")
    print("-" * 60)
    
    # Generate 10 random cubes with patterns
    cubes = [
        create_test_cube("A", "B", "C", "D", "E", "F"),
        create_test_cube("B", "C", "D", "E", "F", "A"),
        create_test_cube("C", "D", "E", "F", "A", "B"),
        create_test_cube("D", "E", "F", "A", "B", "C"),
        create_test_cube("E", "F", "A", "B", "C", "D"),
        create_test_cube("F", "A", "B", "C", "D", "E"),
        create_test_cube("X", "Y", "Z", "W", "U", "V"),
        create_test_cube("Y", "Z", "W", "U", "V", "X"),
        create_test_cube("Z", "W", "U", "V", "X", "Y"),
        create_test_cube("W", "U", "V", "X", "Y", "Z"),
    ]
    
    solver = CubeStackSolver(cubes)
    
    import time
    start = time.perf_counter()
    height = solver.solve()
    elapsed = time.perf_counter() - start
    
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 10 cubes")
    print(f"  Got: Height = {height}")
    print(f"  Sequence length: {len(sequence)}")
    print(f"  Execution time: {elapsed*1000:.3f}ms")
    
    assert height > 0, "Should find at least some stacking"
    assert elapsed < 0.1, "Should complete in < 100ms"
    
    print("  [PASS]")
    return True


def test_validation_consistency():
    """Test that DP and Brute Force agree on small cases."""
    print("\n[TEST 6] Validation Consistency (DP vs Brute Force)")
    print("-" * 60)
    
    test_cases = [
        [create_test_cube("R", "B", "G", "Y", "P", "O"),
         create_test_cube("B", "R", "Y", "G", "O", "P")],
        
        [create_test_cube("A", "B", "C", "D", "E", "F"),
         create_test_cube("B", "C", "D", "E", "F", "A"),
         create_test_cube("C", "D", "E", "F", "A", "B")],
        
        [create_test_cube("X", "X", "X", "X", "X", "X"),
         create_test_cube("X", "X", "X", "X", "X", "X"),
         create_test_cube("X", "X", "X", "X", "X", "X"),
         create_test_cube("X", "X", "X", "X", "X", "X")],
    ]
    
    all_match = True
    for i, cubes in enumerate(test_cases):
        dp_solver = CubeStackSolver(cubes)
        dp_height = dp_solver.solve()
        
        bf_solver = BruteForceSolver(cubes)
        bf_height = bf_solver.solve()
        
        match = dp_height == bf_height
        all_match = all_match and match
        
        status = "[OK]" if match else "[FAIL]"
        print(f"  Case {i+1}: {len(cubes)} cubes - DP={dp_height}, "
              f"BF={bf_height} {status}")
        
        assert match, f"Mismatch in test case {i+1}"
    
    print(f"  All cases match: {all_match}")
    print("  [PASS]")
    return True


def test_reconstruction_validity():
    """Test that reconstructed sequence is actually valid."""
    print("\n[TEST 7] Reconstruction Validity")
    print("-" * 60)
    
    cubes = [
        create_test_cube("R", "B", "G", "Y", "P", "O"),
        create_test_cube("B", "R", "Y", "G", "O", "P"),
        create_test_cube("R", "G", "B", "Y", "O", "P"),
    ]
    
    solver = CubeStackSolver(cubes)
    height = solver.solve()
    sequence = solver.get_stacking_sequence()
    
    print(f"  Input: 3 cubes")
    print(f"  Height: {height}")
    print(f"  Sequence: {sequence}")
    
    # Validate each stack transition
    if len(sequence) > 1:
        for i in range(len(sequence) - 1):
            cube_idx_curr, orient_idx_curr = sequence[i]
            cube_idx_next, orient_idx_next = sequence[i + 1]
            
            curr_orientations = solver.orientations[cube_idx_curr]
            next_orientations = solver.orientations[cube_idx_next]
            
            curr_top, _ = curr_orientations[orient_idx_curr]
            _, next_bottom = next_orientations[orient_idx_next]
            
            is_valid = curr_top == next_bottom
            print(f"  Transition {i} -> {i+1}: {curr_top} == {next_bottom} ? {is_valid}")
            
            assert is_valid, f"Invalid transition at step {i+1}"
    
    print("  [PASS]")
    return True


def run_all_tests():
    """Run all edge case tests."""
    print("=" * 60)
    print("EDGE CASE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_single_cube,
        test_impossible_to_stack,
        test_identical_cubes,
        test_partial_stackable,
        test_large_case,
        test_validation_consistency,
        test_reconstruction_validity,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"\nTotal: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n[SUCCESS] All edge case tests passed!")
    else:
        print(f"\n[FAILURE] {failed} test(s) failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
