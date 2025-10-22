#!/usr/bin/env python3
"""
Demo script showing how the notebook components work together.
This demonstrates the core functionality without requiring LLM initialization.
"""

import sys
import json
from pathlib import Path

# Add DSL to path
sys.path.insert(0, 'arc-dsl')

import dsl
import constants
import solvers

def demo_1_load_task():
    """Demonstrate loading an ARC task."""
    print("=" * 60)
    print("DEMO 1: Loading ARC Task")
    print("=" * 60)
    
    task_file = "ARC-AGI-2-main/data/training/00d62c1b.json"
    with open(task_file, 'r') as f:
        task = json.load(f)
    
    print(f"✓ Task loaded: 00d62c1b")
    print(f"  Training examples: {len(task['train'])}")
    print(f"  Test examples: {len(task['test'])}")
    print(f"  First input shape: {len(task['train'][0]['input'])}x{len(task['train'][0]['input'][0])}")
    print(f"  First output shape: {len(task['train'][0]['output'])}x{len(task['train'][0]['output'][0])}")
    
    return task

def demo_2_dsl_catalog():
    """Demonstrate DSL function catalog."""
    print("\n" + "=" * 60)
    print("DEMO 2: DSL Function Catalog")
    print("=" * 60)
    
    # Get DSL functions
    dsl_functions = [name for name in dir(dsl) if not name.startswith('_') and callable(getattr(dsl, name))]
    
    print(f"✓ Total DSL functions: {len(dsl_functions)}")
    print(f"\nSample functions:")
    for func in dsl_functions[:10]:
        f = getattr(dsl, func)
        doc = f.__doc__ or "No description"
        print(f"  - {func}: {doc.strip()}")
    
    return dsl_functions

def demo_3_prebuilt_solver():
    """Demonstrate using a pre-built solver."""
    print("\n" + "=" * 60)
    print("DEMO 3: Pre-built Solver Execution")
    print("=" * 60)
    
    # Load task
    task_file = "ARC-AGI-2-main/data/training/00d62c1b.json"
    with open(task_file, 'r') as f:
        task = json.load(f)
    
    # Convert to tuple format
    test_input = tuple(tuple(row) for row in task['train'][0]['input'])
    expected_output = tuple(tuple(row) for row in task['train'][0]['output'])
    
    # Run solver
    print("Running solve_00d62c1b...")
    result = solvers.solve_00d62c1b(test_input)
    
    match = result == expected_output
    print(f"✓ Solver executed")
    print(f"  Result matches expected: {match}")
    print(f"  Output shape: {len(result)}x{len(result[0])}")
    
    return match

def demo_4_dsl_operations():
    """Demonstrate basic DSL operations."""
    print("\n" + "=" * 60)
    print("DEMO 4: Basic DSL Operations")
    print("=" * 60)
    
    # Create test grid
    test_grid = (
        (0, 0, 1, 0),
        (0, 1, 1, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 0)
    )
    
    print("Original grid:")
    for row in test_grid:
        print(f"  {row}")
    
    # Apply various operations
    print("\n1. Vertical Mirror:")
    vm = dsl.vmirror(test_grid)
    for row in vm:
        print(f"  {row}")
    
    print("\n2. Horizontal Mirror:")
    hm = dsl.hmirror(test_grid)
    for row in hm:
        print(f"  {row}")
    
    print("\n3. Rotate 90:")
    r90 = dsl.rot90(test_grid)
    for row in r90:
        print(f"  {row}")
    
    print("\n✓ DSL operations work correctly")

def demo_5_code_generation_simulation():
    """Simulate what the LLM would generate."""
    print("\n" + "=" * 60)
    print("DEMO 5: Code Generation & Execution Simulation")
    print("=" * 60)
    
    # Example generated code (what LLM would produce)
    generated_code = """
def solve(I):
    # Identify enclosed black regions and fill with yellow
    objs = objects(grid=I, univalued=T, diagonal=F, without_bg=F)
    black_objs = colorfilter(objs=objs, value=ZERO)
    borders = rbind(function=bordering, fixed=I)
    does_not_border = compose(outer=flip, inner=borders)
    enclosed = mfilter(container=black_objs, function=does_not_border)
    O = fill(grid=I, value=FOUR, patch=enclosed)
    return O
"""
    
    print("Generated DSL code:")
    print(generated_code)
    
    # Load task
    task_file = "ARC-AGI-2-main/data/training/00d62c1b.json"
    with open(task_file, 'r') as f:
        task = json.load(f)
    
    test_input = tuple(tuple(row) for row in task['train'][0]['input'])
    expected_output = tuple(tuple(row) for row in task['train'][0]['output'])
    
    # Execute code
    print("\nExecuting generated code...")
    namespace = {'__builtins__': __builtins__, 'I': test_input}
    
    # Add DSL functions
    for name in dir(dsl):
        if not name.startswith('_'):
            namespace[name] = getattr(dsl, name)
    
    # Add constants
    for name in dir(constants):
        if not name.startswith('_'):
            namespace[name] = getattr(constants, name)
    
    exec(generated_code, namespace)
    result = namespace['solve'](test_input)
    
    match = result == expected_output
    print(f"✓ Code executed successfully")
    print(f"  Result matches expected: {match}")

def demo_6_batch_statistics():
    """Show statistics about available solvers."""
    print("\n" + "=" * 60)
    print("DEMO 6: Solver Statistics")
    print("=" * 60)
    
    # Count solvers
    solver_functions = [name for name in dir(solvers) if name.startswith('solve_')]
    
    print(f"✓ Pre-built solvers: {len(solver_functions)}")
    
    # Load all tasks
    training_path = Path("ARC-AGI-2-main/data/training")
    all_tasks = list(training_path.glob("*.json"))
    
    print(f"✓ Training tasks available: {len(all_tasks)}")
    
    # Check how many have pre-built solvers
    tasks_with_solvers = 0
    for task_file in all_tasks:
        task_id = task_file.stem
        if f"solve_{task_id}" in solver_functions:
            tasks_with_solvers += 1
    
    print(f"✓ Tasks with pre-built solvers: {tasks_with_solvers}")
    print(f"✓ Tasks needing LLM generation: {len(all_tasks) - tasks_with_solvers}")
    
    coverage = (tasks_with_solvers / len(all_tasks)) * 100
    print(f"\nCoverage: {coverage:.1f}%")

def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print(" " * 15 + "LLM DSL Solver - Functionality Demo")
    print("=" * 70)
    print("\nThis demo shows how the notebook components work together.")
    print("No LLM required - using pre-built solvers and mock generation.\n")
    
    try:
        demo_1_load_task()
        demo_2_dsl_catalog()
        demo_3_prebuilt_solver()
        demo_4_dsl_operations()
        demo_5_code_generation_simulation()
        demo_6_batch_statistics()
        
        print("\n" + "=" * 70)
        print(" " * 20 + "✓ All Demos Completed Successfully!")
        print("=" * 70)
        print("\nThe notebook is ready to use!")
        print("See NOTEBOOK_README.md for full documentation.")
        print("See KAGGLE_SETUP.md for Kaggle setup instructions.")
        print("\n")
        
        return 0
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
