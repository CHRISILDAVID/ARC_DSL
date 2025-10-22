# ARC-DSL: LLM-Based Solver for ARC-AGI-2

This repository contains a comprehensive solution for solving ARC (Abstraction and Reasoning Corpus) tasks using Large Language Models (LLMs) combined with Domain Specific Language (DSL) programs.

## 🎯 What's New

**LLM-Based DSL Solver** - A Jupyter notebook that leverages open-source LLMs to intelligently search through and apply DSL transformations to solve ARC-AGI-2 tasks.

### Key Features

- 🤖 **LLM Integration**: Uses open-source models (Phi-3, Mistral, Llama) to analyze tasks
- 🔧 **184 DSL Functions**: Comprehensive library of transformation primitives
- 📊 **400 Pre-built Solvers**: Immediate solutions for 39.1% of tasks
- 🎨 **Visual Interface**: Intuitive grid visualization with ARC color scheme
- ⚙️ **Kaggle Ready**: Optimized for P100 GPU with configurable paths
- 📈 **Batch Processing**: Efficiently process multiple tasks
- 🔄 **Extensible**: Framework for adding custom DSL operations

## 📁 Repository Structure

```
ARC_DSL/
├── llm_dsl_solver.ipynb       # 🌟 Main notebook (START HERE)
├── QUICK_REFERENCE.md         # Fast lookup guide
├── KAGGLE_SETUP.md            # Step-by-step Kaggle setup
├── NOTEBOOK_README.md         # Detailed documentation
├── SUMMARY.md                 # Technical implementation details
├── demo_notebook_usage.py     # Demo script (no LLM needed)
├── test_notebook_components.py # Validation tests
├── arc-dsl/                   # DSL module
│   ├── dsl.py                # 184 DSL functions
│   ├── solvers.py            # 400 pre-built solvers
│   ├── constants.py          # Color/direction constants
│   └── arc_types.py          # Type definitions
└── ARC-AGI-2-main/           # ARC-AGI-2 dataset
    └── data/
        ├── training/         # 1,000 training tasks
        └── evaluation/       # 120 evaluation tasks
```

## 🚀 Quick Start

### Option 1: Kaggle (Recommended)

1. **Upload to Kaggle**:
   - Upload `llm_dsl_solver.ipynb`
   - Add `arc-dsl` and `ARC-AGI-2-main` as datasets

2. **Configure Paths** (first cell):
   ```python
   DSL_MODULE_PATH = "/kaggle/input/arc-dsl/arc-dsl"
   ARC_DATA_PATH = "/kaggle/input/arc-agi-2/ARC-AGI-2-main/data"
   ```

3. **Enable GPU P100** in Settings

4. **Run All Cells**

**See [KAGGLE_SETUP.md](KAGGLE_SETUP.md) for detailed instructions.**

### Option 2: Local

1. **Install Dependencies**:
   ```bash
   pip install transformers torch accelerate matplotlib numpy jupyter
   ```

2. **Configure Paths** in notebook:
   ```python
   DSL_MODULE_PATH = "./arc-dsl"
   ARC_DATA_PATH = "./ARC-AGI-2-main/data"
   ```

3. **Run Notebook**:
   ```bash
   jupyter notebook llm_dsl_solver.ipynb
   ```

## 📊 Statistics

| Metric | Value |
|--------|-------|
| DSL Functions | 184 |
| Pre-built Solvers | 400 |
| Training Tasks | 1,000 |
| Evaluation Tasks | 120 |
| Pre-built Coverage | 39.1% |
| Tasks Need LLM | 609 |

## 🔧 LLM Model Options

| Model | Memory | Speed | Accuracy | Best For |
|-------|--------|-------|----------|----------|
| **Phi-3-mini** (default) | 7.5GB | Medium | Good | Balanced |
| Mistral-7B | 14GB | Slow | Better | Accuracy |
| TinyLlama | 2.5GB | Fast | Lower | Speed |

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Fast lookup and common tasks
- **[KAGGLE_SETUP.md](KAGGLE_SETUP.md)** - Detailed Kaggle setup instructions
- **[NOTEBOOK_README.md](NOTEBOOK_README.md)** - Complete notebook documentation
- **[SUMMARY.md](SUMMARY.md)** - Technical implementation details

## 🎮 Demo

Run the demo to see how components work (no LLM required):

```bash
python3 demo_notebook_usage.py
```

This demonstrates:
- Loading ARC tasks
- Using DSL functions
- Running pre-built solvers
- Code generation and execution
- Batch statistics

## ✅ Validation

All components tested and validated:

```bash
python3 test_notebook_components.py
```

Expected output: `✓ All tests passed! Notebook is ready to use.`

## 🎯 How It Works

1. **Load Task**: Parse ARC task from JSON
2. **Check Solvers**: Look for pre-built solution (39.1% coverage)
3. **LLM Analysis**: If no solver, use LLM to analyze task patterns
4. **Generate Code**: LLM produces DSL program sequence
5. **Execute**: Run DSL operations on test input
6. **Validate**: Compare with expected output
7. **Iterate**: Refine based on results

## 🔄 Workflow

```mermaid
graph LR
    A[ARC Task] --> B{Pre-built?}
    B -->|Yes| C[Use Solver]
    B -->|No| D[LLM Analysis]
    D --> E[Generate DSL Code]
    E --> F[Execute]
    F --> G[Validate]
    C --> G
    G --> H[Prediction]
```

## 📈 Expected Performance

- **Pre-built Solvers**: ~99% accuracy on known tasks
- **LLM-Generated**: 10-50% accuracy (varies by task complexity)
- **Overall**: ~50-60% on training set

## ⏱️ Runtime (P100 GPU)

- Model download: 5-10 minutes (first time)
- 10 tasks: ~5-10 minutes
- 100 tasks: ~30-60 minutes
- Full dataset: ~5-10 hours

## 🔧 Configuration

All paths and settings are configurable as variables:

```python
# Paths (change for your environment)
DSL_MODULE_PATH = "./arc-dsl"
ARC_DATA_PATH = "./ARC-AGI-2-main/data"

# LLM Settings
LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
USE_GPU = True
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.1
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Out of Memory | Use TinyLlama or reduce MAX_NEW_TOKENS |
| Module Not Found | Verify DSL_MODULE_PATH is correct |
| Slow Execution | Use smaller model or reduce batch size |
| LLM Download Fails | Check internet connection |

See [NOTEBOOK_README.md](NOTEBOOK_README.md#troubleshooting) for more details.

## 🎓 Extending DSL

Add new operations for ARC-AGI-2 specific patterns:

```python
def extended_dsl_operations():
    def find_repeating_pattern(grid):
        """Detect repeating patterns in the grid."""
        # Your implementation
        pass
    
    def symmetry_detection(grid):
        """Detect symmetries in the grid."""
        # Your implementation
        pass
    
    return {
        'find_repeating_pattern': find_repeating_pattern,
        'symmetry_detection': symmetry_detection,
    }
```

## 📝 Citation

If you use this work, please cite:

```bibtex
@software{arc_dsl_llm_solver,
  title={LLM-Based DSL Solver for ARC-AGI-2},
  author={CHRISILDAVID},
  year={2024},
  url={https://github.com/CHRISILDAVID/ARC_DSL}
}
```

## 📄 License

This project builds upon:
- [arc-dsl](arc-dsl/) - Domain Specific Language for ARC
- [ARC-AGI-2](ARC-AGI-2-main/) - Abstraction and Reasoning Corpus v2

See respective LICENSE files for details.

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Fine-tune LLM on ARC tasks
- [ ] Add more DSL operations
- [ ] Improve prompt engineering
- [ ] Implement ensemble methods
- [ ] Add iterative refinement
- [ ] Optimize for speed

## 🌟 Acknowledgments

- Original ARC-DSL by the arc-dsl team
- ARC-AGI-2 by François Chollet and team
- Open-source LLM communities (Phi, Mistral, Llama)

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Questions**: See documentation files
- **Demo**: Run `demo_notebook_usage.py`

---

**Ready to start solving ARC tasks?** Open [llm_dsl_solver.ipynb](llm_dsl_solver.ipynb) and follow the instructions! 🚀
