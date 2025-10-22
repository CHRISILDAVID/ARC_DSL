# Quick Setup Guide for Kaggle

This guide will help you set up and run the LLM DSL Solver notebook on Kaggle with P100 GPU.

## Step 1: Prepare Datasets

### Option A: Upload as Datasets (Recommended)

1. **Create arc-dsl Dataset**:
   - Zip the `arc-dsl` folder
   - Go to Kaggle → Your Profile → Datasets → New Dataset
   - Upload `arc-dsl.zip`
   - Title: "ARC DSL Module"
   - Slug: `arc-dsl`

2. **Create ARC-AGI-2 Dataset** (if not already available):
   - Zip the `ARC-AGI-2-main` folder
   - Upload to Kaggle Datasets
   - Title: "ARC-AGI-2 Data"
   - Slug: `arc-agi-2`

### Option B: Direct Upload

1. Create a new Kaggle Notebook
2. Click "Add Data" → "Upload" → "Add Folder"
3. Upload both `arc-dsl` and `ARC-AGI-2-main` folders

## Step 2: Create New Notebook

1. Go to Kaggle → Code → New Notebook
2. Delete default cell
3. Click "File" → "Import Notebook"
4. Upload `llm_dsl_solver.ipynb`

## Step 3: Configure Paths

Edit the first code cell to match your setup:

### If using Kaggle Datasets:
```python
# ===== CONFIGURATION =====
DSL_MODULE_PATH = "/kaggle/input/arc-dsl/arc-dsl"
ARC_DATA_PATH = "/kaggle/input/arc-agi-2/ARC-AGI-2-main/data"
TRAINING_DATA_PATH = f"{ARC_DATA_PATH}/training"
EVALUATION_DATA_PATH = f"{ARC_DATA_PATH}/evaluation"

# LLM Configuration
LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
USE_GPU = True
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.1
```

### If using Direct Upload:
```python
# ===== CONFIGURATION =====
DSL_MODULE_PATH = "/kaggle/working/arc-dsl"
ARC_DATA_PATH = "/kaggle/working/ARC-AGI-2-main/data"
TRAINING_DATA_PATH = f"{ARC_DATA_PATH}/training"
EVALUATION_DATA_PATH = f"{ARC_DATA_PATH}/evaluation"

# LLM Configuration  
LLM_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
USE_GPU = True
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.1
```

## Step 4: Enable GPU

1. Click "Settings" on the right sidebar
2. Under "Accelerator", select **GPU P100**
3. Save settings

## Step 5: Install Dependencies

Uncomment and run the installation cell:

```python
# Install required packages
!pip install transformers torch accelerate matplotlib numpy
```

**Note**: Kaggle kernels already have many packages, but you may need to install/upgrade these specific ones.

## Step 6: Run the Notebook

1. Click "Run All" or run cells sequentially
2. Monitor progress in the output
3. First run will download the LLM model (~7.5GB for Phi-3-mini)

## Expected Runtime

- **Model Download**: 5-10 minutes (first time only)
- **Initialization**: 1-2 minutes
- **Per Task**: 10-30 seconds (depending on complexity)
- **10 Tasks**: ~5-10 minutes
- **100 Tasks**: ~30-60 minutes

## Troubleshooting

### "No module named 'transformers'"
- Make sure the pip install cell executed successfully
- Restart kernel and rerun from beginning

### "CUDA out of memory"
- Reduce `MAX_NEW_TOKENS` to 256
- Process fewer tasks at once
- Try smaller model: `"TinyLlama/TinyLlama-1.1B-Chat-v1.0"`

### "DSL module not found"
- Verify `DSL_MODULE_PATH` is correct
- Check data sources are properly added
- Use `!ls /kaggle/input/` to see available paths

### "Task file not found"
- Verify `ARC_DATA_PATH` is correct
- Check the folder structure matches expectations
- Use `!ls /kaggle/input/arc-agi-2/` to verify

### Model Download is Slow
- This is normal on first run
- Consider using cached models:
  ```python
  LLM_MODEL_NAME = "/kaggle/input/phi-3-mini-4k/transformers/default/1"
  ```
  (if model is pre-downloaded as a dataset)

## Optimization Tips

### For Faster Execution:
1. **Use Smaller Model**:
   ```python
   LLM_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
   ```

2. **Reduce Token Limit**:
   ```python
   MAX_NEW_TOKENS = 256
   ```

3. **Process in Batches**:
   ```python
   # In the batch processing cell
   all_results = batch_solve_tasks(all_training_tasks, max_tasks=20)
   ```

### For Better Accuracy:
1. **Use Larger Model** (if memory allows):
   ```python
   LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
   ```

2. **Increase Token Limit**:
   ```python
   MAX_NEW_TOKENS = 1024
   ```

3. **Lower Temperature**:
   ```python
   TEMPERATURE = 0.05  # More deterministic
   ```

## Saving Results

The notebook will generate:
- `submission.json`: Formatted predictions for evaluation tasks
- Intermediate results in notebook cells

To download:
1. Run the submission generation cell
2. Click the output file in the file browser
3. Download to your computer

## Alternative Models

If the default model doesn't work or you want to try others:

### Small & Fast (1-2GB):
- `"TinyLlama/TinyLlama-1.1B-Chat-v1.0"`
- Fastest, lowest accuracy

### Medium & Balanced (7-8GB):
- `"microsoft/Phi-3-mini-4k-instruct"` (default)
- `"microsoft/phi-2"`
- Good balance of speed and accuracy

### Large & Accurate (13-15GB):
- `"mistralai/Mistral-7B-Instruct-v0.2"`
- `"meta-llama/Llama-2-7b-chat-hf"` (requires HF token)
- Best accuracy, slower

## Next Steps

After successful setup:

1. **Test on Sample Tasks**: Run cells up to "Test on Sample Tasks"
2. **Visualize Results**: Check the visualization outputs
3. **Batch Process**: Uncomment and run the full pipeline
4. **Generate Submission**: Create submission file for evaluation
5. **Iterate**: Adjust prompts, models, or add DSL functions

## Support

If you encounter issues:
1. Check the NOTEBOOK_README.md for detailed documentation
2. Review error messages in notebook output
3. Verify all paths are correct for your setup
4. Ensure GPU is enabled and model fits in memory

## Example Output

```
Loading model: microsoft/Phi-3-mini-4k-instruct...
Using device: cuda
GPU: Tesla P100-PCIE-16GB
GPU Memory: 16.28 GB
✓ LLM initialized successfully

✓ Found 184 DSL functions
✓ Found 400 pre-built solvers

Loading training tasks...
✓ Loaded 10 training tasks

============================================================
Testing task: 00d62c1b
============================================================
Found pre-built solver for 00d62c1b
  Training example 1: ✓
  Training example 2: ✓
  Training example 3: ✓
Task 00d62c1b: SOLVED (5/5)
```

Happy solving! 🎯
