
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Find project root and load configuration
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")

if not all([MONGODB_URI, DATABASE_NAME, COLLECTION_NAME]):
    raise ValueError("Check MongoDB settings in the root .env file.")

client = None

try:
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )
    client.admin.command("ping")
    print("MongoDB connection successful!")

    collection = client[DATABASE_NAME][COLLECTION_NAME]
    total = collection.count_documents({})

    print(f"Database: {DATABASE_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Total documents: {total}")

    if total == 0:
        raise ValueError(
            "No documents found. Check the collection name."
        )

    # Read existing records only
    records = list(collection.find({}))
    for record in records:
        record["_id"] = str(record["_id"])

    df = pd.DataFrame(records)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nDataset shape:", df.shape)
    print("\nMissing values per column:")
    print(df.isnull().sum().to_string())

    # Export local working copy
    raw_dir = PROJECT_DIR / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_file = raw_dir / "healthcare_claims_export.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"\nExport completed: {output_file}")
    print(f"Rows exported: {len(df)}")

except Exception as error:
    print(f"\nError: {error}")
    raise

finally:
    if client is not None:
        client.close()
        print("MongoDB connection closed.")
        