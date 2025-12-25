# Docker Environment

This will process the Dockerfile.in templates and generate Dockerfiles for each target.

## 1. Initialize Python Virtual Environment

> [!NOTE]
> Python is installed. >3.13.9

Open a terminal in this directory and run:

```sh
python -m venv .venv
```

Activate the virtual environment:

- On **Windows**:
  ```sh
  .venv\Scripts\activate
  ```
- On **Linux/macOS**:
  ```sh
  source .venv/bin/activate
  ```

## 2. Install Dependencies

```sh
pip install -r requirements.txt
```

## 3. Install pre-commit hooks (for contributors)

```sh
pre-commit install
```

## 4. Run the Dockerfile Generator

To generate Dockerfiles, run:

- On **Windows**:
    ```sh
    python .\make-dockerfiles
    ```
- On **Linux/macOS**:
    ```sh
    python ./make-dockerfiles
    ```