FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv pip install --system .

COPY src/ ./src/

EXPOSE 8080
CMD ["python", "-m", "src.mcp_server"]
