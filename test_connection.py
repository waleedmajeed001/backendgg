#!/usr/bin/env python3
"""
Test Neon PostgreSQL database connection
"""

import os
from dotenv import load_dotenv
from database import get_db_connection, DATABASE_URL

def test_connection():
    load_dotenv()
    
    print("🔍 Testing Neon PostgreSQL Connection")
    print("=" * 40)
    
    if not DATABASE_URL.startswith('postgresql://'):
        print("❌ DATABASE_URL is not configured for PostgreSQL")
        print("💡 Please set DATABASE_URL in .env file to your Neon connection string")
        return False
    
    try:
        print(f"🔗 Connecting to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connected successfully!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📋 Existing tables: {[table[0] for table in tables]}")
        else:
            print("📋 No tables found - run 'python migrate.py' to create tables")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your DATABASE_URL in .env file")
        print("2. Make sure your Neon database is running")
        print("3. Verify your credentials are correct")
        return False

if __name__ == "__main__":
    test_connection()

