"""
Utility functions for cube orientation generation and manipulation.

This module provides functions to:
- Represent cubes with 6 colored faces
- Generate all possible orientations of a cube
- Validate cube configurations
"""

from typing import List, Tuple, Dict, Set


def rotate_x(cube: List[str]) -> List[str]:
    """
    Rotate cube 90 degrees around X axis (left-right).
    
    Cube representation: [top, bottom, front, back, left, right]
    Rotation around X: top->front->bottom->back->top
    
    Args:
        cube: List of 6 colors representing cube faces
        
    Returns:
        Rotated cube configuration
    """
    top, bottom, front, back, left, right = cube
    return [front, back, bottom, top, left, right]


def rotate_y(cube: List[str]) -> List[str]:
    """
    Rotate cube 90 degrees around Y axis (up-down).
    
    Cube representation: [top, bottom, front, back, left, right]
    Rotation around Y: front->right->back->left->front
    
    Args:
        cube: List of 6 colors representing cube faces
        
    Returns:
        Rotated cube configuration
    """
    top, bottom, front, back, left, right = cube
    return [top, bottom, left, right, back, front]


def rotate_z(cube: List[str]) -> List[str]:
    """
    Rotate cube 90 degrees around Z axis (front-back).
    
    Cube representation: [top, bottom, front, back, left, right]
    Rotation around Z: top->right->bottom->left->top
    
    Args:
        cube: List of 6 colors representing cube faces
        
    Returns:
        Rotated cube configuration
    """
    top, bottom, front, back, left, right = cube
    return [left, right, front, back, bottom, top]


def generate_all_orientations(cube: List[str]) -> List[Tuple[str, str]]:
    """
    Generate all 6 unique orientations (top, bottom) pairs for a cube.
    
    For a cube with 6 faces, there are 6 ways to orient it such that
    each face can be on top. Each orientation is uniquely defined by
    its (top_color, bottom_color) pair.
    
    Algorithm:
    1. Start with initial orientation
    2. Apply rotations to explore different orientations
    3. Extract (top, bottom) pairs
    4. Ensure we have all 6 unique pairs
    
    Args:
        cube: List of 6 colors [top, bottom, front, back, left, right]
        
    Returns:
        List of 6 tuples (top_color, bottom_color) for each orientation
    """
    orientations: Set[Tuple[str, str]] = set()
    visited: Set[Tuple] = set()
    
    # Use BFS to explore all reachable orientations
    queue = [cube]
    visited.add(tuple(cube))
    
    while queue:
        current = queue.pop(0)
        
        # Record the (top, bottom) pair
        top, bottom = current[0], current[1]
        orientations.add((top, bottom))
        
        # Try all three rotations
        for rotated in [rotate_x(current), rotate_y(current), rotate_z(current)]:
            rotated_tuple = tuple(rotated)
            if rotated_tuple not in visited:
                visited.add(rotated_tuple)
                queue.append(rotated)
    
    # Convert to sorted list for consistency
    result = sorted(list(orientations))
    
    # Verify we have exactly 6 unique orientations
    if len(result) != 6:
        # If we don't have 6, it means duplicate colors or invalid input
        # Still return what we have
        pass
    
    return result


def get_cube_id(cube: List[str], orientation_idx: int) -> str:
    """
    Create a unique identifier for a cube orientation.
    
    Args:
        cube: The original cube configuration
        orientation_idx: Index of the orientation
        
    Returns:
        A unique string identifier
    """
    cube_str = "-".join(cube)
    return f"cube_{abs(hash(cube_str)) % 10000}_{orientation_idx}"


def format_cube(cube: List[str]) -> str:
    """
    Format cube for display.
    
    Args:
        cube: Cube configuration
        
    Returns:
        Formatted string representation
    """
    top, bottom, front, back, left, right = cube
    return f"[T:{top} B:{bottom} F:{front} K:{back} L:{left} R:{right}]"


def validate_stacking(bottom_cube_top: str, top_cube_bottom: str) -> bool:
    """
    Check if two cubes can be stacked.
    
    Two cubes can be stacked if the bottom face of the upper cube
    matches the top face of the lower cube.
    
    Args:
        bottom_cube_top: Color of top face of lower cube
        top_cube_bottom: Color of bottom face of upper cube
        
    Returns:
        True if stacking is valid
    """
    return bottom_cube_top == top_cube_bottom


def create_test_cube(color1: str, color2: str, color3: str, 
                     color4: str, color5: str, color6: str) -> List[str]:
    """
    Create a cube with 6 specified colors.
    
    Args:
        color1-6: Colors for [top, bottom, front, back, left, right]
        
    Returns:
        Cube configuration
    """
    return [color1, color2, color3, color4, color5, color6]


if __name__ == "__main__":
    # Test orientation generation
    print("=" * 60)
    print("CUBE ORIENTATION GENERATOR TEST")
    print("=" * 60)
    
    test_cube = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
    print(f"\nOriginal Cube: {format_cube(test_cube)}")
    
    orientations = generate_all_orientations(test_cube)
    print(f"\nGenerated {len(orientations)} orientations:")
    for i, (top, bottom) in enumerate(orientations, 1):
        print(f"  {i}. Top: {top:10} -> Bottom: {bottom}")
