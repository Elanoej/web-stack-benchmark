import os


def main():
    workers = int(os.getenv("WORKERS", "1"))
    os.execvp("python", [
        "python", "-m", "uvicorn", "app.main:app",
        "--host", "0.0.0.0", "--port", "5000",
        "--workers", str(workers),
    ])


if __name__ == "__main__":
    main()
