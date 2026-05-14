"""Seed script for local development."""

import asyncio
import random
from datetime import datetime, timedelta
from uuid import uuid4

from app.infrastructure.db.models.sale import Sale
from app.infrastructure.db.models.user import User
from app.infrastructure.db.session import async_session_factory, engine
from app.infrastructure.db.models.base import Base
from app.core.security import hash_password


REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "EMEA"]
PRODUCTS = [
    ("PROD-001", "Enterprise CRM License"),
    ("PROD-002", "AI Forecasting Module"),
    ("PROD-003", "Data Integration Pack"),
    ("PROD-004", "Premium Support"),
    ("PROD-005", "Mobile App Add-on"),
    ("PROD-006", "Custom Reporting Suite"),
    ("PROD-007", "API Access Tier 1"),
    ("PROD-008", "Training & Onboarding"),
]
CUSTOMERS = [
    (str(uuid4()), "Acme Corp"),
    (str(uuid4()), "Globex Industries"),
    (str(uuid4()), "Soylent Solutions"),
    (str(uuid4()), "Initech LLC"),
    (str(uuid4()), "Umbrella Corp"),
    (str(uuid4()), "Stark Enterprises"),
    (str(uuid4()), "Wayne Industries"),
    (str(uuid4()), "Cyberdyne Systems"),
]


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Create test user
        user = User(
            id=str(uuid4()),
            email="demo@salespredict.ai",
            hashed_password=hash_password("demo123"),
            full_name="Demo User",
            is_active=True,
            is_superuser=False,
        )
        session.add(user)
        await session.flush()

        # Create sales for last 6 months
        now = datetime.utcnow()
        sales: list[Sale] = []
        for i in range(250):
            days_back = random.randint(0, 180)
            sale_date = now - timedelta(days=days_back)
            # Add some seasonality
            base_amount = random.uniform(500, 5000)
            if sale_date.month in [11, 12]:
                base_amount *= 1.4
            elif sale_date.month in [6, 7]:
                base_amount *= 0.9

            product_id, product_name = random.choice(PRODUCTS)
            customer_id, customer_name = random.choice(CUSTOMERS)
            region = random.choice(REGIONS)

            sale = Sale(
                id=str(uuid4()),
                amount=round(base_amount, 2),
                quantity=random.randint(1, 20),
                product_id=product_id,
                product_name=product_name,
                customer_id=customer_id,
                customer_name=customer_name,
                region=region,
                status=random.choice(
                    ["completed", "completed", "completed", "pending", "cancelled"]
                ),
                sale_date=sale_date,
            )
            sales.append(sale)

        session.add_all(sales)
        await session.commit()
        print(f"Seeded 1 user and {len(sales)} sales records.")


if __name__ == "__main__":
    asyncio.run(seed())
