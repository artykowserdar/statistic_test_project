from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import proxy, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (was previously in @app.on_event("startup"))
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)   # only if you want clean start for tests
        await conn.run_sync(Base.metadata.create_all)

    yield   # ← here the application runs

    # Shutdown code (was previously in @app.on_event("shutdown"))
    # await engine.dispose()   # usually not needed, but can be added


app = FastAPI(
    title="Statistic Test Project",
    description="Backend-прокси + пользовательская статистика для bot.e-replika.ru",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,           # ← important line
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy.router)
app.include_router(stats.router)


@app.get("/health")
def health():
    return {"status": "healthy", "project": "statistic_test_project"}