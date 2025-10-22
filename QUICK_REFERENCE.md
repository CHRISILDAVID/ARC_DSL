# Quick Reference Card

## For Kaggle Users

### Setup (5 minutes)
```python
# 1. Upload notebook and data to Kaggle
# 2. Enable GPU P100
# 3. Update these paths:
DSL_MODULE_PATH = "/kaggle/input/arc-dsl/arc-dsl"
ARC_DATA_PATH = "/kaggle/input/arc-agi-2/ARC-AGI-2-main/data"

# 4. Install dependencies:
!pip install transformers torch accelerate matplotlib numpy
```

### Run
```python
# Just run all cells - that's it!
```

## Key Statistics

- **Total DSL Functions**: 184
- **Pre-built Solvers**: 400
- **Training Tasks**: 1,000
- **Evaluation Tasks**: 120
- **Pre-built Coverage**: 39.1%
- **Tasks Need LLM**: 609

## Model Options

| Model | Memory | Speed | Accuracy |
|-------|--------|-------|----------|
| Phi-3-mini (default) | 7.5GB | Medium | Good |
| Mistral-7B | 14GB | Slow | Better |
| TinyLlama | 2.5GB | Fast | Lower |

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Out of Memory | Use TinyLlama or MAX_NEW_TOKENS=256 |
| Module Not Found | Check DSL_MODULE_PATH |
| Slow Execution | Reduce max_tasks or use smaller model |
| LLM Errors | Check internet for model download |

## Expected Runtime (P100)

- Model download: 5-10 min (first time)
- 10 tasks: ~5-10 min
- 100 tasks: ~30-60 min
- Full dataset: ~5-10 hours

## Files Overview

```
llm_dsl_solver.ipynb    - Main notebook (30 cells)
NOTEBOOK_README.md      - Full documentation
KAGGLE_SETUP.md         - Step-by-step setup
SUMMARY.md              - Implementation details
demo_notebook_usage.py  - Test without LLM
```

## Common Modifications

### Use Different Model
```python
LLM_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

### Process Fewer Tasks
```python
batch_solve_tasks(tasks, max_tasks=20)
```

### Lower Temperature (More Deterministic)
```python
TEMPERATURE = 0.05
```

### Process Only Evaluation Set
```python
eval_tasks = load_arc_tasks(EVALUATION_DATA_PATH)
results = batch_solve_tasks(eval_tasks)
```

## Notebook Sections

1. **Configuration** - Set paths and parameters
2. **Setup** - Load modules and initialize
3. **Data Loading** - Load ARC tasks
4. **LLM Init** - Initialize language model
5. **Analysis** - Generate solutions
6. **Execution** - Run and validate
7. **Batch** - Process multiple tasks
8. **Extensions** - Add custom functions

## Success Rate Formula

```
Total Accuracy = (Pre-built × 0.99) + (LLM-generated × 0.30)
Expected: ~50-60% on training set
```

## Next Steps After Setup

1. ✅ Run test on 3 sample tasks
2. ✅ Verify visualizations work
3. ✅ Process 10-20 tasks
4. ✅ Review accuracy
5. ✅ Adjust parameters if needed
6. ✅ Run full batch
7. ✅ Generate submission

## Support Resources

- **Full docs**: NOTEBOOK_README.md
- **Setup help**: KAGGLE_SETUP.md
- **Technical details**: SUMMARY.md
- **Test script**: demo_notebook_usage.py

## Output Files

- `submission.json` - Predictions for submission
- Notebook cells contain intermediate results

## Performance Tips

**Speed up**:
- Use TinyLlama model
- Reduce MAX_NEW_TOKENS
- Process in smaller batches

**Improve accuracy**:
- Use larger model (Mistral-7B)
- Increase MAX_NEW_TOKENS
- Lower temperature

**Save memory**:
- Use smaller model
- Reduce batch size
- Enable CPU mode if needed

---

**Ready to start?** Open `llm_dsl_solver.ipynb` and run all cells! 🚀
