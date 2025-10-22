#!/usr/bin/env python3
"""
Training script for DSL-based ARC-AGI-2 solver.

This script implements a program synthesis approach that:
1. Searches through DSL program combinations
2. Validates programs against training examples
3. Selects the best program for each task
4. Applies learned programs to test cases
"""

import sys
import json
import os
import inspect
from pathlib import Path
from typing import List, Dict, Tuple, Any, Callable, Optional
from collections import defaultdict
import random

# Add DSL to path
sys.path.insert(0, 'arc-dsl')

import dsl
import constants
import solvers


class DSLProgramSynthesizer:
    """Synthesizes DSL programs by searching through combinations."""
    
    def __init__(self, max_depth=3, timeout_per_task=30):
        self.max_depth = max_depth
        self.timeout_per_task = timeout_per_task
        self.dsl_functions = self._extract_dsl_functions()
        self.simple_transforms = self._get_simple_transforms()
        
    def _extract_dsl_functions(self) -> Dict[str, Callable]:
        """Extract all DSL functions."""
        functions = {}
        for name in dir(dsl):
            if not name.startswith('_'):
                obj = getattr(dsl, name)
                if callable(obj):
                    functions[name] = obj
        return functions
    
    def _get_simple_transforms(self) -> List[str]:
        """Get list of simple grid transformation functions."""
        # Focus on common transformation patterns
        transforms = [
            'identity',
            'vmirror', 'hmirror', 'dmirror', 'cmirror',
            'rot90', 'rot180', 'rot270',
            'upscale', 'downscale',
            'trim', 'compress',
        ]
        return [t for t in transforms if t in self.dsl_functions]
    
    def _try_simple_transform(self, train_examples: List[Dict]) -> Optional[str]:
        """Try simple single-function transformations."""
        for func_name in self.simple_transforms:
            func = self.dsl_functions[func_name]
            
            # Test if this function works for all training examples
            all_match = True
            for example in train_examples:
                try:
                    I = tuple(tuple(row) for row in example['input'])
                    expected = tuple(tuple(row) for row in example['output'])
                    
                    result = func(I)
                    if result != expected:
                        all_match = False
                        break
                except:
                    all_match = False
                    break
            
            if all_match:
                return f"def solve(I):\n    O = {func_name}(I)\n    return O"
        
        return None
    
    def _try_prebuilt_solver(self, task_id: str, train_examples: List[Dict]) -> Optional[str]:
        """Check if a pre-built solver exists and works."""
        solver_name = f"solve_{task_id}"
        
        if hasattr(solvers, solver_name):
            solver_func = getattr(solvers, solver_name)
            
            # Validate it works on training examples
            all_match = True
            for example in train_examples:
                try:
                    I = tuple(tuple(row) for row in example['input'])
                    expected = tuple(tuple(row) for row in example['output'])
                    
                    result = solver_func(I)
                    if result != expected:
                        all_match = False
                        break
                except Exception as e:
                    all_match = False
                    break
            
            if all_match:
                # Extract source code and wrap it
                source = inspect.getsource(solver_func)
                # The source is the actual function, we can return it as-is
                # but rename it to 'solve' for consistency
                source = source.replace(f"def {solver_name}(", "def solve(")
                return source
        
        return None
    
    def _try_color_mapping(self, train_examples: List[Dict]) -> Optional[str]:
        """Try simple color mapping transformations."""
        # Check if output is just input with colors remapped
        for example in train_examples:
            I = example['input']
            O = example['output']
            
            if len(I) != len(O) or len(I[0]) != len(O[0]):
                return None
        
        # Try to find a consistent color mapping
        color_map = {}
        for example in train_examples:
            I = example['input']
            O = example['output']
            
            for i in range(len(I)):
                for j in range(len(I[0])):
                    in_color = I[i][j]
                    out_color = O[i][j]
                    
                    if in_color in color_map:
                        if color_map[in_color] != out_color:
                            return None
                    else:
                        color_map[in_color] = out_color
        
        # If we found a consistent mapping, generate code
        if color_map:
            map_str = str(color_map)
            code = f"""def solve(I):
    color_map = {map_str}
    O = tuple(tuple(color_map.get(cell, cell) for cell in row) for row in I)
    return O"""
            return code
        
        return None
    
    def _try_combined_transforms(self, train_examples: List[Dict]) -> Optional[str]:
        """Try combinations of 2-3 simple transforms."""
        # Try pairs of transformations
        for func1_name in self.simple_transforms[:10]:  # Limit to avoid explosion
            for func2_name in self.simple_transforms[:10]:
                func1 = self.dsl_functions[func1_name]
                func2 = self.dsl_functions[func2_name]
                
                all_match = True
                for example in train_examples:
                    try:
                        I = tuple(tuple(row) for row in example['input'])
                        expected = tuple(tuple(row) for row in example['output'])
                        
                        temp = func1(I)
                        result = func2(temp)
                        
                        if result != expected:
                            all_match = False
                            break
                    except:
                        all_match = False
                        break
                
                if all_match:
                    code = f"""def solve(I):
    x1 = {func1_name}(I)
    O = {func2_name}(x1)
    return O"""
                    return code
        
        return None
    
    def synthesize_program(self, task_id: str, train_examples: List[Dict]) -> Tuple[Optional[str], str]:
        """
        Synthesize a DSL program for the given task.
        
        Returns:
            (program_code, method_used)
        """
        # Strategy 1: Check for pre-built solver
        program = self._try_prebuilt_solver(task_id, train_examples)
        if program:
            return program, "prebuilt"
        
        # Strategy 2: Try simple single transforms
        program = self._try_simple_transform(train_examples)
        if program:
            return program, "simple_transform"
        
        # Strategy 3: Try color mapping
        program = self._try_color_mapping(train_examples)
        if program:
            return program, "color_mapping"
        
        # Strategy 4: Try combined transforms
        program = self._try_combined_transforms(train_examples)
        if program:
            return program, "combined_transforms"
        
        # No program found
        return None, "none"


class ARCTrainer:
    """Trains DSL programs on ARC tasks."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.synthesizer = DSLProgramSynthesizer()
        self.learned_programs = {}
        
    def load_task(self, task_file: Path) -> Dict:
        """Load a task from JSON file."""
        with open(task_file, 'r') as f:
            return json.load(f)
    
    def execute_program(self, code: str, input_grid: List[List[int]]) -> Optional[List[List[int]]]:
        """Execute a DSL program on an input grid."""
        if not code:
            return None
        
        try:
            # Convert input to tuple format
            I = tuple(tuple(row) for row in input_grid)
            
            # Create execution namespace
            namespace = {
                '__builtins__': __builtins__,
                'I': I,
            }
            
            # Add all DSL functions
            for name in dir(dsl):
                if not name.startswith('_'):
                    namespace[name] = getattr(dsl, name)
            
            # Add all constants
            for name in dir(constants):
                if not name.startswith('_'):
                    namespace[name] = getattr(constants, name)
            
            # Execute the code
            exec(code, namespace)
            
            # Call the solve function
            if 'solve' in namespace:
                result = namespace['solve'](I)
                # Convert back to list format
                if isinstance(result, tuple):
                    return [list(row) for row in result]
                return result
            
            return None
        
        except Exception as e:
            # print(f"Error executing program: {e}")
            return None
    
    def validate_program(self, code: str, train_examples: List[Dict]) -> float:
        """Validate a program against training examples."""
        if not code:
            return 0.0
        
        correct = 0
        total = len(train_examples)
        
        for example in train_examples:
            predicted = self.execute_program(code, example['input'])
            if predicted == example['output']:
                correct += 1
        
        return correct / total if total > 0 else 0.0
    
    def train_on_task(self, task_id: str, task_data: Dict) -> Dict:
        """Train on a single task."""
        result = {
            'task_id': task_id,
            'program': None,
            'method': 'none',
            'train_accuracy': 0.0,
            'test_predictions': []
        }
        
        # Synthesize program
        program, method = self.synthesizer.synthesize_program(task_id, task_data['train'])
        
        if program:
            # Validate on training data
            train_accuracy = self.validate_program(program, task_data['train'])
            
            result['program'] = program
            result['method'] = method
            result['train_accuracy'] = train_accuracy
            
            # Generate test predictions
            for test_example in task_data['test']:
                predicted = self.execute_program(program, test_example['input'])
                if predicted is None:
                    # If execution failed, return empty grid
                    predicted = [[0] * len(test_example['input'][0]) for _ in range(len(test_example['input']))]
                result['test_predictions'].append(predicted)
        else:
            # No program found - return zero predictions
            for test_example in task_data['test']:
                predicted = [[0] * len(test_example['input'][0]) for _ in range(len(test_example['input']))]
                result['test_predictions'].append(predicted)
        
        return result
    
    def train_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Train on all tasks in the training data."""
        training_path = Path(self.data_path) / "training"
        task_files = sorted(list(training_path.glob("*.json")))
        
        if limit:
            task_files = task_files[:limit]
        
        print(f"Training on {len(task_files)} tasks...")
        
        results = {}
        stats = {
            'total': len(task_files),
            'solved': 0,
            'methods': defaultdict(int),
            'avg_accuracy': 0.0
        }
        
        for i, task_file in enumerate(task_files):
            task_id = task_file.stem
            task_data = self.load_task(task_file)
            
            result = self.train_on_task(task_id, task_data)
            results[task_id] = result
            
            # Update stats
            if result['train_accuracy'] == 1.0:
                stats['solved'] += 1
            stats['methods'][result['method']] += 1
            stats['avg_accuracy'] += result['train_accuracy']
            
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(task_files)} tasks...")
        
        stats['avg_accuracy'] /= len(task_files)
        
        print(f"\nTraining complete!")
        print(f"  Solved: {stats['solved']}/{stats['total']} ({stats['solved']/stats['total']:.1%})")
        print(f"  Average accuracy: {stats['avg_accuracy']:.1%}")
        print(f"  Methods used:")
        for method, count in stats['methods'].items():
            print(f"    {method}: {count}")
        
        return {
            'results': results,
            'stats': stats
        }
    
    def save_trained_programs(self, training_results: Dict, output_file: str = "trained_programs.json"):
        """Save trained programs and statistics."""
        with open(output_file, 'w') as f:
            json.dump(training_results, f, indent=2)
        
        print(f"Trained programs saved to {output_file}")
    
    def generate_submission(self, results: Dict, output_file: str = "submission.json"):
        """Generate submission file for evaluation data."""
        submission = {}
        
        for task_id, result in results.items():
            predictions = result['test_predictions']
            
            # ARC submission format: 2 attempts per test case
            submission[task_id] = [
                {'attempt_1': pred, 'attempt_2': pred}
                for pred in predictions
            ]
        
        with open(output_file, 'w') as f:
            json.dump(submission, f, indent=2)
        
        print(f"Submission saved to {output_file}")


def main():
    """Main training script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train DSL programs on ARC-AGI-2 tasks')
    parser.add_argument('--data-path', default='ARC-AGI-2-main/data',
                        help='Path to ARC data directory')
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit number of tasks to train on')
    parser.add_argument('--output', default='trained_programs.json',
                        help='Output file for trained programs')
    parser.add_argument('--submission', default='submission.json',
                        help='Output submission file')
    
    args = parser.parse_args()
    
    # Create trainer
    trainer = ARCTrainer(args.data_path)
    
    # Train on all tasks
    training_results = trainer.train_all(limit=args.limit)
    
    # Save trained programs
    trainer.save_trained_programs(training_results, args.output)
    
    # Generate submission
    trainer.generate_submission(training_results['results'], args.submission)
    
    return 0


if __name__ == '__main__':
    exit(main())
