#!/usr/bin/env python3
"""
Setup script for Neon PostgreSQL database
"""

import os

def setup_neon():
    print("🚀 Setting up Neon PostgreSQL Database")
    print("=" * 50)
    
    print("\n📋 Steps to set up Neon database:")
    print("1. Go to https://neon.tech and create an account")
    print("2. Create a new project")
    print("3. Get your connection string from the dashboard")
    print("4. Copy the connection string")
    
    print("\n🔧 Configuration:")
    print("Create a .env file in the backend directory with:")
    print("DATABASE_URL=postgresql://username:password@host:port/database")
    
    print("\n💡 Example .env file content:")
    print("DATABASE_URL=postgresql://john:mypassword@ep-cool-name-123456.us-east-2.aws.neon.tech/todo_db")
    print("FLASK_ENV=development")
    print("FLASK_DEBUG=True")
    
    print("\n✅ After setting up .env file, run:")
    print("python migrate.py")
    print("python app.py")
    
    print("\n🔍 To check if your connection works:")
    print("python test_connection.py")

if __name__ == "__main__":
    setup_neon()

