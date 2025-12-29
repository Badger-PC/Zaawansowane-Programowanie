# Animal Detection API Management

This guide explains how to start, stop, and restart the Animal Detection API server.

### Start the Server
To start the server with auto-reload enabled (useful for development):
```bash
python run.py
```

### Stop the Server
To stop the running server:
```bash
kill <PID>
```

### Restart the Server
To restart the server (stop execution and start again):
```bash
kill <PID>
python run.py
```

### Stop the Server
If the server is running in your current terminal, simply press **Ctrl+C**.

If the server is running in the background or another terminal you want to kill:
1.  Find the process ID (PID):
    ```bash
    ps aux | grep uvicorn
    ```
2.  Kill the process using the PID found above:
    ```bash
    kill <PID>
    ```
    Or use `pkill` to kill by name:
    ```bash
    pkill -f "uvicorn src.main:app"
    ```
