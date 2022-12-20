import uvicorn
from settings import settings

def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app:get_app",
        workers=settings.WORKERS_COUNT,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    main()