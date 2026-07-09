from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from bot.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

engine = None
_session_maker = None


def _make_url():
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is not set. "
            "Check your .env file or Railway environment variables."
        )
    db_url = DATABASE_URL
    if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    connect_args = {}
    if "supabase" in db_url:
        connect_args["ssl"] = "require"
    return db_url, connect_args


async def init_engine():
    global engine, _session_maker
    db_url, connect_args = _make_url()
    engine = create_async_engine(db_url, echo=False, connect_args=connect_args)
    _session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    logger.info("Database engine initialized")


@asynccontextmanager
async def get_db():
    global _session_maker
    if _session_maker is None:
        await init_engine()
    async with _session_maker() as session:
        yield session


async def column_exists(conn, table: str, column: str) -> bool:
    try:
        result = await conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = :column"
        ), {"table": table, "column": column})
        return result.scalar() is not None
    except Exception:
        return False


async def table_exists(conn, table: str) -> bool:
    try:
        result = await conn.execute(text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_name = :table"
        ), {"table": table})
        return result.scalar() is not None
    except Exception:
        return False


async def migrate_schema():
    if not engine:
        await init_engine()
    # Bu migratsiya Postgres'ga xos (information_schema, ALTER TABLE).
    # SQLite (lokal test) uchun create_all allaqachon to'g'ri sxemani yaratadi — o'tkazib yuboramiz.
    if engine.dialect.name != "postgresql":
        logger.info(f"Skipping Postgres-specific migration for dialect: {engine.dialect.name}")
        return
    async with engine.begin() as conn:
        if not await column_exists(conn, "users", "household_size"):
            await conn.execute(text("ALTER TABLE users ADD COLUMN household_size INTEGER NOT NULL DEFAULT 1"))
            logger.info("Added column: users.household_size")
        else:
            logger.info("Column users.household_size already exists")
        
        if not await column_exists(conn, "users", "language"):
            await conn.execute(text("ALTER TABLE users ADD COLUMN language VARCHAR(2) NOT NULL DEFAULT 'uz'"))
            logger.info("Added column: users.language")
        else:
            logger.info("Column users.language already exists")

        for col in ["telegram_username", "approved_at", "approved_by", "status"]:
            if await column_exists(conn, "users", col):
                await conn.execute(text(f"ALTER TABLE users DROP COLUMN {col}"))
                logger.info(f"Dropped column: users.{col}")

        for col in ["location_lat", "location_lng"]:
            if not await column_exists(conn, "orders", col):
                await conn.execute(text(f"ALTER TABLE orders ADD COLUMN {col} DOUBLE PRECISION"))
                logger.info(f"Added column: orders.{col}")
            else:
                logger.info(f"Column orders.{col} already exists")

        # Saqlangan manzil ustunlari (users)
        if not await column_exists(conn, "users", "saved_address"):
            await conn.execute(text("ALTER TABLE users ADD COLUMN saved_address TEXT"))
            logger.info("Added column: users.saved_address")
        if not await column_exists(conn, "users", "saved_lat"):
            await conn.execute(text("ALTER TABLE users ADD COLUMN saved_lat DOUBLE PRECISION"))
            logger.info("Added column: users.saved_lat")
        if not await column_exists(conn, "users", "saved_lng"):
            await conn.execute(text("ALTER TABLE users ADD COLUMN saved_lng DOUBLE PRECISION"))
            logger.info("Added column: users.saved_lng")

        # Bir nechta mahsulot uchun ustunlar (orders)
        if not await column_exists(conn, "orders", "items"):
            await conn.execute(text("ALTER TABLE orders ADD COLUMN items TEXT"))
            logger.info("Added column: orders.items")
        if not await column_exists(conn, "orders", "total_price"):
            await conn.execute(text("ALTER TABLE orders ADD COLUMN total_price INTEGER"))
            logger.info("Added column: orders.total_price")

        for col in ["product_type", "delivery_date", "delivered_at", "delivered_by"]:
            if await column_exists(conn, "orders", col):
                await conn.execute(text(f"ALTER TABLE orders DROP COLUMN {col}"))
                logger.info(f"Dropped column: orders.{col}")

        for tbl in ["operators", "delivery_staff", "blacklist"]:
            if await table_exists(conn, tbl):
                await conn.execute(text(f"DROP TABLE IF EXISTS {tbl} CASCADE"))
                logger.info(f"Dropped table: {tbl}")


async def init_db():
    if not engine:
        await init_engine()
    from bot.database.models import Base
    import asyncio
    for attempt in range(5):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except OSError as e:
            if attempt < 4:
                wait = (attempt + 1) * 5
                logger.warning(f"Database connection failed (attempt {attempt+1}/5): {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                raise
    await migrate_schema()
    logger.info("Database migration completed")
