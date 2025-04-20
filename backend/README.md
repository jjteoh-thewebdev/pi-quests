# Quick Start

1. create `.env` from `.env.sample`

2. Start Redis
    ```bash
    docker compose up -d redis
    ```
3. (recommended) Run Python virtual environment
    ```bash
    source venv/bin/activate

    # to exit
    deactivate
    ```
4. Install dependencies
    ```bash
    # Install system dependencies for gmpy2
    # Ubuntu/Debian:
    sudo apt apt-get update
    sudo apt install libgmp-dev libmpfr-dev libmpc-dev

    # Install Python deps
    pip install -r requirements.txt
    ```
5. Start the FastAPI server
    ```bash
    uvicorn app.main:app --reload
    ```
6. (Optional) Run unit test
    ```bash
    pytest tests/unit
    ```
7. (Optional) Run e2e test
    ```bash
    pytest tests/e2e
    ```