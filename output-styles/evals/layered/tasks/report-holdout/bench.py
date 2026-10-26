"""Benchmark an ETL loader that inserts rows in batches.

    python3 bench.py --batch-size 100 --seed 1

Simulates loading 200,000 rows and prints total time and peak memory.
"""
import argparse
import random

ROWS = 200_000
ROW_BYTES = 2_048
MEMORY_LIMIT_MB = 512
PER_BATCH_OVERHEAD_S = 0.004
PER_ROW_S = 0.00003


def run(batch_size, seed):
    rng = random.Random(seed)
    buffered_mb = batch_size * ROW_BYTES * 6 / 1_000_000
    peak_mb = 180 + buffered_mb * rng.uniform(40, 48)
    total = 0.0
    for _ in range(ROWS // batch_size):
        t = PER_BATCH_OVERHEAD_S + batch_size * PER_ROW_S * rng.uniform(0.9, 1.1)
        if peak_mb > MEMORY_LIMIT_MB:
            t *= 1 + (peak_mb - MEMORY_LIMIT_MB) / 40
        total += t
    return total, peak_mb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    total, peak = run(args.batch_size, args.seed)
    print(f"batch_size={args.batch_size} seed={args.seed} rows={ROWS} "
          f"total_s={total:.1f} peak_mem_mb={peak:.0f}")


if __name__ == "__main__":
    main()
