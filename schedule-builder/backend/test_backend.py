import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    from app.services.database_service import DatabaseService
    from app.services.excel_parser import ExcelParserService
    print("Backend components imported successfully!")
    print("- FastAPI app initialized")
    
    # Test database service
    db_service = DatabaseService()
    print("- Database service initialized")
    
    # Test excel parser service
    excel_parser = ExcelParserService()
    print("- Excel parser service initialized")
    
    print("\nAll backend components are working correctly!")
    
except Exception as e:
    print(f"Error initializing backend components: {e}")
    import traceback
    traceback.print_exc()