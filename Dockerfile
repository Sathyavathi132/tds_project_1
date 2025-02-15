FROM python:3.12-slim-bookworm

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install `uv`
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install dependencies inside `uv` virtual environment
RUN uv venv && .venv/bin/python -m ensurepip && .venv/bin/python -m pip install -r requirements.txt


# Command to run the FastAPI app
CMD [".venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
