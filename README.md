# A Benchark for Aerial Image Matching and Localization
In this repository, we provide 17 matching method for evaluation and localization.


#### 👉Refer to [ImatchToolbox](https://github.com/GrumpyZhou/image-matching-toolbox) for details about installation. (Thanks this codebase)

## Image Matching Evaluation

### Dataset Download

Download the benchmark dataset from Huggingface and organize it as follows:

```
ExeBenchmark/
└── Benchmark/
    ├── class_0/
    │   ├── class_0.npy       # metadata (poses, intrinsics, image pairs, overlap, pitch, scale)
    │   ├── rgb/              # 1581 aerial JPEG images
    │   │   ├── Berlin14@q137@17@-30@59@0@90.jpg   # query image
    │   │   ├── Berlin14@400@385@-60@-180@0@90.jpg  # reference image
    │   │   └── ...
    │   └── depth/            # 1581 EXR depth maps (paired with rgb/)
    │       ├── Berlin14@q137@17@-30@59@0@900001.exr
    │       └── ...
    ├── class_1/
    │   └── ...
    └── class_31/
        └── ...
```

#### Dataset Structure

The benchmark contains **32 difficulty classes** organized along three axes:

| Axis | Values |
|------|--------|
| **Scale** (GSD ratio between query and reference) | 1–2× (class 0–15) · 2–3× (class 16–31) |
| **Camera pitch** (degrees from nadir) | 55–59° · 60–64° · 65–69° · 70–74° |
| **Image overlap** | 60–80% · 40–60% · 20–40% · <20% |


Per class: **1581 images**, **1000 evaluation pairs**.

### Running the Benchmark

All paths are configured through variables at the top of `run_benchmark.sh`. Edit them to match your setup, then run:

```bash
bash run_benchmark.sh
```

#### Configuration (edit `run_benchmark.sh`)

| Variable | Description | Default |
|---|---|---|
| `MODEL` | Model name — must match `configs/<MODEL>.yml` | `gim_roma` |
| `DATA_DIR` | Root directory of benchmark data (contains `class_0/`, `class_1/`, ...) | `/media/guan/ZX1/ExeBenchmark/Benchmark` |
| `RESULTS_DIR` | Root directory to save results | `/media/guan/ZX1/ExeBenchmark/results` |
| `NUM_CLASSES` | Number of class folders to evaluate | `32` |

Results are saved to `$RESULTS_DIR/<MODEL>/` with three subdirectories:
- `pck/` — PCK scores per class
- `loc/` — per-pair localization errors
- `auc/` — pose AUC scores per class

#### Running directly with Python

You can also pass arguments directly without the shell script:

```bash
python run_extrebenchmark.py \
    --model       gim_roma \
    --data_dir    /path/to/Benchmark \
    --results_dir /path/to/results \
    --num_classes 32
```

