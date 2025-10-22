#!/usr/bin/env python3
"""
Testing script for trained DSL programs.

This script:
1. Loads trained programs from training phase
2. Applies them to test/evaluation data
3. Generates predictions
4. Computes accuracy metrics
"""

import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add DSL to path
sys.path.insert(0, 'arc-dsl')

import dsl
import constants


class DSLTester:
    """Tests trained DSL programs on new data."""
    
    def __init__(self, trained_programs: Dict[str, Any]):
        self.trained_programs = trained_programs
        
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
            return None
    
    def test_on_task(self, task_id: str, task_data: Dict) -> Dict:
        """Test on a single task."""
        result = {
            'task_id': task_id,
            'has_program': False,
            'predictions': [],
            'test_accuracy': None
        }
        
        # Get trained program for this task
        if task_id in self.trained_programs:
            program_info = self.trained_programs[task_id]
            program = program_info.get('program')
            
            if program:
                result['has_program'] = True
                
                # Generate predictions for test cases
                for test_example in task_data['test']:
                    predicted = self.execute_program(program, test_example['input'])
                    
                    if predicted is None:
                        # If execution failed, return zero grid
                        predicted = [[0] * len(test_example['input'][0]) 
                                   for _ in range(len(test_example['input']))]
                    
                    result['predictions'].append(predicted)
                    
                    # If test output is available, compute accuracy
                    if 'output' in test_example:
                        if predicted == test_example['output']:
                            if result['test_accuracy'] is None:
                                result['test_accuracy'] = 1.0
                        else:
                            result['test_accuracy'] = 0.0
        
        # If no program, return zero predictions
        if not result['has_program']:
            for test_example in task_data['test']:
                predicted = [[0] * len(test_example['input'][0]) 
                           for _ in range(len(test_example['input']))]
                result['predictions'].append(predicted)
        
        return result
    
    def test_all(self, data_path: str, split: str = 'evaluation') -> Dict[str, Any]:
        """Test on all tasks in a split (evaluation or training)."""
        data_dir = Path(data_path) / split
        task_files = sorted(list(data_dir.glob("*.json")))
        
        print(f"Testing on {len(task_files)} tasks from {split} split...")
        
        results = {}
        stats = {
            'total': len(task_files),
            'with_programs': 0,
            'correct': 0,
            'avg_accuracy': 0.0
        }
        
        for i, task_file in enumerate(task_files):
            task_id = task_file.stem
            
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            result = self.test_on_task(task_id, task_data)
            results[task_id] = result
            
            # Update stats
            if result['has_program']:
                stats['with_programs'] += 1
            
            if result['test_accuracy'] is not None:
                if result['test_accuracy'] == 1.0:
                    stats['correct'] += 1
                stats['avg_accuracy'] += result['test_accuracy']
            
            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(task_files)} tasks...")
        
        if stats['total'] > 0:
            stats['avg_accuracy'] /= stats['total']
        
        print(f"\nTesting complete!")
        print(f"  Tasks with programs: {stats['with_programs']}/{stats['total']}")
        if stats['with_programs'] > 0:
            print(f"  Correct predictions: {stats['correct']}/{stats['total']} ({stats['correct']/stats['total']:.1%})")
            print(f"  Average accuracy: {stats['avg_accuracy']:.1%}")
        
        return {
            'results': results,
            'stats': stats
        }
    
    def generate_submission(self, results: Dict, output_file: str = "test_submission.json"):
        """Generate submission file."""
        submission = {}
        
        for task_id, result in results.items():
            predictions = result['predictions']
            
            # ARC submission format: 2 attempts per test case
            submission[task_id] = [
                {'attempt_1': pred, 'attempt_2': pred}
                for pred in predictions
            ]
        
        with open(output_file, 'w') as f:
            json.dump(submission, f, indent=2)
        
        print(f"Submission saved to {output_file}")


def main():
    """Main testing script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test trained DSL programs')
    parser.add_argument('--data-path', default='ARC-AGI-2-main/data',
                        help='Path to ARC data directory')
    parser.add_argument('--trained-programs', default='trained_programs.json',
                        help='Path to trained programs file')
    parser.add_argument('--split', default='evaluation',
                        choices=['training', 'evaluation'],
                        help='Which split to test on')
    parser.add_argument('--output', default='test_submission.json',
                        help='Output submission file')
    
    args = parser.parse_args()
    
    # Load trained programs
    print(f"Loading trained programs from {args.trained_programs}...")
    with open(args.trained_programs, 'r') as f:
        trained_data = json.load(f)
    
    trained_programs = trained_data.get('results', {})
    print(f"Loaded {len(trained_programs)} trained programs")
    
    # Create tester
    tester = DSLTester(trained_programs)
    
    # Test on specified split
    test_results = tester.test_all(args.data_path, args.split)
    
    # Generate submission
    tester.generate_submission(test_results['results'], args.output)
    
    return 0


if __name__ == '__main__':
    exit(main())
