import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Attempting to import agent...")
    from src.core.agent import beauty_advisor_agent
    print("Agent imported successfully!")
except Exception as e:
    print(f"\n❌ Error importing agent: {e}")
    import traceback
    traceback.print_exc()
