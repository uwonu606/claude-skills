"""Simulate a job queue drained by N workers that share one database.

    python3 sim.py --workers 8 --seed 1

Prints throughput and p95 job latency for one run.
"""
import argparse
import heapq
import random

DB_CONNECTIONS = 10
LOCK_WAIT_COST = 0.012


def simulate(workers, seed, duration, arrival_rate):
    rng = random.Random(seed)
    t = 0.0
    arrivals = []
    while t < duration:
        t += rng.expovariate(arrival_rate)
        arrivals.append(t)
    free_at = [0.0] * workers
    heapq.heapify(free_at)
    db_free_at = [0.0] * DB_CONNECTIONS
    heapq.heapify(db_free_at)
    latencies = []
    done = 0
    for arrived in arrivals:
        worker_free = heapq.heappop(free_at)
        start = max(arrived, worker_free)
        db_free = heapq.heappop(db_free_at)
        busy = sum(1 for f in db_free_at if f > start) + 1
        contention = max(0, workers - DB_CONNECTIONS) * LOCK_WAIT_COST * busy
        service = rng.uniform(0.04, 0.08) * (1 + contention)
        db_start = max(start, db_free)
        finish = db_start + service
        heapq.heappush(db_free_at, finish)
        heapq.heappush(free_at, finish)
        if finish <= duration:
            done += 1
            latencies.append(finish - arrived)
    latencies.sort()
    p95 = latencies[int(0.95 * len(latencies)) - 1] if latencies else float("nan")
    return done / duration, p95


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--arrival-rate", type=float, default=150.0)
    args = parser.parse_args()
    throughput, p95 = simulate(args.workers, args.seed, args.duration, args.arrival_rate)
    print(f"workers={args.workers} seed={args.seed} duration_s={args.duration:.0f} "
          f"throughput_jobs_per_s={throughput:.1f} p95_latency_s={p95:.2f}")


if __name__ == "__main__":
    main()
