import os


def get_cpu_count():
    try:
        with open("/sys/fs/cgroup/cpu.max") as f:
            quota_str, period_str = f.read().strip().split()
            if quota_str != "max":
                quota = int(quota_str)
                period = int(period_str)
                if period > 0:
                    return max(1, quota // period)
    except (FileNotFoundError, ValueError):
        pass

    try:
        with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us") as f:
            quota = int(f.read().strip())
        with open("/sys/fs/cgroup/cpu/cpu.cfs_period_us") as f:
            period = int(f.read().strip())
        if quota > 0 and period > 0:
            return max(1, quota // period)
    except (FileNotFoundError, ValueError):
        pass

    return os.cpu_count() or 1


def main():
    cpus = get_cpu_count()
    workers = cpus * 2 + 1
    os.execvp("uv", [
        "uv", "run", "uvicorn", "app.main:app",
        "--host", "0.0.0.0", "--port", "5000",
        "--workers", str(workers),
    ])


if __name__ == "__main__":
    main()
