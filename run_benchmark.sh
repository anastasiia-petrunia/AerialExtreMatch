#!/bin/bash
# ==============================================================================
# run_benchmark.sh — Run AerialExtreMatch benchmark
# Usage: bash run_benchmark.sh
# Edit the variables below to match your setup before running.
# ==============================================================================

# Model name: must match a file in configs/<MODEL>.yml
MODEL="gim_roma"

# Root directory of benchmark data (must contain class_0/, class_1/, ...)
DATA_DIR="/media/guan/ZX1/ExeBenchmark/Benchmark"

# Root directory to save results (subdirs per model will be created automatically)
RESULTS_DIR="/media/guan/ZX1/ExeBenchmark/results"

# Number of class folders to evaluate (class_0 to class_{NUM_CLASSES-1})
NUM_CLASSES=32

# ==============================================================================
# Run benchmark (no need to edit below this line)
# ==============================================================================
python run_extrebenchmark.py \
    --model        "$MODEL"       \
    --data_dir     "$DATA_DIR"    \
    --results_dir  "$RESULTS_DIR" \
    --num_classes  "$NUM_CLASSES"
