#!/usr/bin/env python3
"""
Database migration script to recreate tables with new schema.
Run this when you add new columns to the models.
"""

from database import recreate_tables

if __name__ == "__main__":
    print("Recreating database tables...")
    recreate_tables()
    print("Database tables recreated successfully!")