#!/usr/bin/env python3
"""
run.py - Entry point to start the FastAPI application
Usage:
    python run.py              # development mode (reload=True)
    python run.py --prod       # production mode (no reload, more workers)
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import uvicorn

# Add project root to sys.path (useful when running from anywhere)
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from app.config import settings  # noqa: E402


def setup_logging():
    """Configure logging for both dev and prod"""
    log_level = "DEBUG" if os.getenv("DEBUG") else "INFO"

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Optional: add file handler in production
    if os.getenv("ENV") == "production":
        fh = logging.FileHandler("logs/app.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        ))
        logging.getLogger().addHandler(fh)


def main():
    parser = argparse.ArgumentParser(description="Run the Statistic Test Project API")
    parser.add_argument("--prod", action="store_true", help="Run in production mode")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=settings.app_port, help="Port to bind")
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    if args.prod:
        logger.info("Starting in PRODUCTION mode")
        reload = False
        workers = 4  # можно увеличить на сервере
        log_level = "info"
    else:
        logger.info("Starting in DEVELOPMENT mode (auto-reload enabled)")
        reload = True
        workers = 1  # reload работает только с 1 worker
        log_level = "debug"

    logger.info(f"API will be available at http://{args.host}:{args.port}/docs")

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=reload,
        workers=workers,
        log_level=log_level,
        factory=False,
        # timeout_keep_alive=65,      # полезно при nginx + gunicorn
        # limit_concurrency=1000,     # можно раскомментировать в проде
    )


if __name__ == "__main__":
    main()