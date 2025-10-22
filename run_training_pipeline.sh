#!/bin/bash
# Full training and testing pipeline for ARC-AGI-2
# This script runs the complete workflow from training to submission

set -e  # Exit on error

echo "=========================================="
echo "ARC-AGI-2 DSL Training Pipeline"
echo "=========================================="
echo ""

# Configuration
DATA_PATH="${1:-ARC-AGI-2-main/data}"
TRAINED_PROGRAMS="trained_programs_full.json"
TRAIN_SUBMISSION="train_submission.json"
EVAL_SUBMISSION="evaluation_submission.json"

# Check if data exists
if [ ! -d "$DATA_PATH" ]; then
    echo "Error: Data directory not found: $DATA_PATH"
    echo "Usage: $0 [data_path]"
    exit 1
fi

echo "Using data path: $DATA_PATH"
echo ""

# Step 1: Train on all training tasks
echo "Step 1: Training on all 1000 training tasks..."
echo "This may take 10-30 minutes depending on your machine."
echo ""

python3 train_dsl_model.py \
    --data-path "$DATA_PATH" \
    --output "$TRAINED_PROGRAMS" \
    --submission "$TRAIN_SUBMISSION"

echo ""
echo "✓ Training complete!"
echo ""

# Step 2: Test on training data (validation)
echo "Step 2: Validating on training data..."
echo ""

python3 test_dsl_model.py \
    --data-path "$DATA_PATH" \
    --trained-programs "$TRAINED_PROGRAMS" \
    --split training \
    --output train_validation.json

echo ""
echo "✓ Validation complete!"
echo ""

# Step 3: Generate predictions for evaluation data
echo "Step 3: Generating predictions for evaluation data..."
echo ""

python3 test_dsl_model.py \
    --data-path "$DATA_PATH" \
    --trained-programs "$TRAINED_PROGRAMS" \
    --split evaluation \
    --output "$EVAL_SUBMISSION"

echo ""
echo "✓ Evaluation predictions complete!"
echo ""

# Summary
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  1. $TRAINED_PROGRAMS - All trained DSL programs"
echo "  2. $TRAIN_SUBMISSION - Training data predictions"
echo "  3. $EVAL_SUBMISSION - Evaluation data predictions (for Kaggle)"
echo ""
echo "Next steps:"
echo "  1. Review training statistics in output above"
echo "  2. Submit $EVAL_SUBMISSION to Kaggle ARC-AGI competition"
echo "  3. (Optional) Analyze failed tasks and improve synthesis"
echo ""
