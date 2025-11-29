import os
try:
    from pydantic_ai.models.gemini import GeminiModel
    print("Import successful")
    model = GeminiModel('gemini-1.5-flash')
    print("Model instantiation successful")
except ImportError:
    print("Import failed")
except Exception as e:
    print(f"Error: {e}")
