# LLM-Based DSL Solver for ARC-AGI-2

This notebook (`llm_dsl_solver.ipynb`) implements an LLM-based approach to solve ARC (Abstraction and Reasoning Corpus) tasks using Domain Specific Language (DSL) programs.

## Overview

The notebook combines:
- **Open-source LLM**: Uses models like Phi-3, Llama-2, or Mistral to analyze tasks
- **DSL Programs**: Leverages existing DSL primitives from arc-dsl
- **Sequential Application**: Applies DSL transformations based on task analysis
- **ARC-AGI-2 Support**: Works with both training and evaluation datasets

## Features

### 1. Configurable Paths
All file paths and dataset locations are defined as variables at the top of the notebook:
```python
DSL_MODULE_PATH = "./arc-dsl"
ARC_DATA_PATH = "./ARC-AGI-2-main/data"
TRAINING_DATA_PATH = f"{ARC_DATA_PATH}/training"
EVALUATION_DATA_PATH = f"{ARC_DATA_PATH}/evaluation"
LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
```

### 2. LLM Integration
- Supports multiple open-source models optimized for P100 GPU (16GB)
- Configurable temperature and token limits
- Automatic fallback to CPU if GPU unavailable
- Memory-efficient loading with float16 precision

### 3. DSL Function Catalog
- Automatically extracts 160+ DSL functions from the arc-dsl module
- Includes 400+ pre-built solver functions
- Formats function signatures and docstrings for LLM prompts

### 4. Task Analysis
- Loads ARC tasks from JSON files
- Visualizes input/output examples using matplotlib
- Analyzes transformation patterns
- Generates DSL code sequences

### 5. Solution Execution
- Executes generated DSL code on test inputs
- Validates solutions against expected outputs
- Computes accuracy metrics
- Generates predictions for test cases

### 6. Batch Processing
- Process multiple tasks efficiently
- Track success rates and accuracy
- Generate submission files for evaluation

## Usage

### On Kaggle (Recommended)

1. **Upload Files**:
   - Upload `llm_dsl_solver.ipynb` to Kaggle
   - Add `arc-dsl` folder as a dataset
   - Add ARC-AGI-2 data as a dataset

2. **Update Configuration**:
   ```python
   DSL_MODULE_PATH = "/kaggle/input/arc-dsl/arc-dsl"
   ARC_DATA_PATH = "/kaggle/input/arc-agi-2/ARC-AGI-2-main/data"
   ```

3. **Enable GPU**:
   - Settings → Accelerator → GPU P100

4. **Install Dependencies**:
   - Uncomment the pip install cell:
   ```python
   !pip install transformers torch accelerate matplotlib numpy
   ```

5. **Run All Cells**:
   - Kernel → Restart & Run All

### Local Usage

1. **Install Dependencies**:
   ```bash
   pip install transformers torch accelerate matplotlib numpy jupyter
   ```

2. **Update Paths**:
   - Edit the configuration cell with your local paths

3. **Run Notebook**:
   ```bash
   jupyter notebook llm_dsl_solver.ipynb
   ```

## Notebook Structure

### Section 1: Configuration
- Set paths for DSL module and data
- Configure LLM model and parameters
- Define GPU/CPU settings

### Section 2: Imports & Setup
- Load DSL modules (dsl, constants, arc_types, solvers)
- Extract DSL function catalog
- Build solver catalog

### Section 3: Data Loading
- Load ARC tasks from JSON files
- Visualize task examples
- Format tasks for LLM prompts

### Section 4: LLM Initialization
- Load tokenizer and model
- Configure for GPU/CPU
- Create text generation pipeline

### Section 5: Analysis & Generation
- Create prompts for task analysis
- Query LLM for solution strategies
- Extract Python code from responses

### Section 6: Execution
- Execute generated DSL code
- Validate against expected outputs
- Compute accuracy metrics

### Section 7: Batch Processing
- Process multiple tasks
- Generate submission files
- Track statistics

### Section 8: Extensions
- Template functions for additional DSL operations
- Suggestions for ARC-AGI-2-specific patterns

## LLM Model Options

### Recommended for P100 GPU (16GB):
- **Phi-3-mini-4k-instruct** (default): ~7.5GB, excellent reasoning
- **Mistral-7B-Instruct-v0.2**: ~14GB, strong performance
- **Llama-2-7b-chat-hf**: ~13GB, requires HF token

### For CPU or Limited Memory:
- **TinyLlama-1.1B-Chat-v1.0**: ~2.5GB, faster inference

## Extending DSL Programs

The original DSL was designed for ARC-AGI-1. For ARC-AGI-2, you may need to add:

1. **Pattern Detection**: Functions to identify repeating patterns
2. **Symmetry Analysis**: Detect horizontal/vertical/diagonal symmetries
3. **Region Operations**: Advanced object grouping and merging
4. **Color Mapping**: Complex color transformation rules
5. **Grid Interpolation**: Resolution changes and scaling

Template functions are provided in the "Additional DSL Programs" section.

## Expected Performance

- **Pre-built Solvers**: High accuracy on ~400 known tasks
- **LLM-Generated**: Variable accuracy (10-50%) depending on task complexity
- **Hybrid Approach**: Uses pre-built when available, LLM for new tasks

## Troubleshooting

### Out of Memory
- Reduce `MAX_NEW_TOKENS`
- Use smaller model (TinyLlama)
- Enable CPU mode: `USE_GPU = False`

### Module Not Found
- Verify `DSL_MODULE_PATH` is correct
- Ensure arc-dsl folder is uploaded to Kaggle

### LLM Errors
- Check internet connection for model download
- Verify HuggingFace token if using gated models
- Try alternative model from recommendations

### Code Execution Errors
- Some generated code may have syntax errors
- Manual verification recommended for important tasks
- Pre-built solvers are more reliable

## Performance Tips

1. **Batch Processing**: Process multiple tasks to amortize LLM loading time
2. **Cache Results**: Save generated code for reuse
3. **Pre-built First**: Check solver catalog before LLM generation
4. **Prompt Engineering**: Modify prompts for better results
5. **Temperature Tuning**: Lower temperature (0.1) for more deterministic outputs

## Output Files

- **submission.json**: Formatted predictions for evaluation
- Task predictions are formatted with attempt_1 and attempt_2

## Contributing

To add new DSL functions:
1. Implement in the extended_dsl_operations section
2. Add docstrings for LLM understanding
3. Update the DSL catalog
4. Test on sample tasks

## References

- [ARC-AGI-2 Repository](https://github.com/fchollet/ARC-AGI-2)
- [Original DSL Paper](arc-dsl/arc_dsl_writeup.pdf)
- [ARC Prize](https://arcprize.org/)

## License

This notebook is provided as-is for the ARC challenge. Please refer to the original DSL and ARC-AGI-2 licenses.
