from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

from models import Base, Company, Dev, Freebie  # make sure your models.py or wherever Base/models are defined

# Set up database
engine = create_engine('sqlite:///freebies.db')  # or whatever your database is
Session = sessionmaker(bind=engine)
session = Session()

# Create tables (if not already created)
Base.metadata.create_all(engine)

# Initialize Faker
faker = Faker()

# Optional: Clear existing data
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()

# Create random companies
companies = []
for _ in range(5):
    company = Company(
        name=faker.company(),
        founding_year=random.randint(1900, 2024)
    )
    session.add(company)
    companies.append(company)

# Create random devs
devs = []
for _ in range(5):
    dev = Dev(
        name=faker.name()
    )
    session.add(dev)
    devs.append(dev)

session.commit()  # Commit so companies/devs have IDs

# Create random freebies linking devs + companies
for _ in range(10):
    freebie = Freebie(
        item_name=faker.word(),
        value=random.randint(1, 100),
        company=random.choice(companies),
        dev=random.choice(devs)
    )
    session.add(freebie)

session.commit()

print("✅ Database seeded with random data!")
