# Fitness Server

This is a FastAPI application for counting exercise repetitions from accelerometer data.

## Running the application

### With Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t fitness-server .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 12001:8000 fitness-server
    ```

### Locally

1.  **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    python run.py
    ```

## Testing

To run the tests, including the stress test, use the following command:

```bash
pytest
```
