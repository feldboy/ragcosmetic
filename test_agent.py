import asyncio
import os
from agent import beauty_advisor_agent, BeautyAdvisorDependencies

# Mock API key if not present, just to allow import, but actual run might fail if not set.
if "OPENROUTER_API_KEY" not in os.environ:
    print("WARNING: OPENROUTER_API_KEY not set. Tests might fail if they hit the LLM.")

async def test_agent():
    print("Starting Agent Verification...")
    deps = BeautyAdvisorDependencies()
    history = []

    # Test 1: Connect & Discover
    print("\n--- Test 1: Connect & Discover ---")
    # We simulate the start.
    # In main.py we sent a trigger message.
    trigger_msg = "The user has just arrived. Start the conversation according to your instructions."
    result = await beauty_advisor_agent.run(trigger_msg, deps=deps)
    print(f"Agent: {result.output}")
    history.extend(result.new_messages())
    
    # Check if it ends with a question
    if not result.output.strip().endswith("?"):
        print("FAILED: Response does not end with a question.")
    else:
        print("PASSED: Response ends with a question.")

    # Test 2: User response (Dry skin)
    print("\n--- Test 2: User Response (Dry Skin) ---")
    user_msg = "My skin feels really dry and tight."
    result = await beauty_advisor_agent.run(user_msg, deps=deps, message_history=history)
    print(f"Agent: {result.output}")
    history.extend(result.new_messages())

    if not result.output.strip().endswith("?"):
        print("FAILED: Response does not end with a question.")
    else:
        print("PASSED: Response ends with a question.")

    # Test 3: Product Recommendation
    print("\n--- Test 3: Product Recommendation ---")
    user_msg = "I prefer creams. What do you recommend?"
    result = await beauty_advisor_agent.run(user_msg, deps=deps, message_history=history)
    print(f"Agent: {result.output}")
    history.extend(result.new_messages())

    # Check if it recommends a product from our list (e.g., Anti-Age Gold Cream or Hydra-Boost)
    # Note: The agent might recommend Hydra-Boost (Serum) even if user said creams if it thinks it's best, 
    # but likely Anti-Age Gold Cream.
    if "**" in result.output:
        print("PASSED: Product name/benefit seems bolded.")
    else:
        print("WARNING: Product name/benefit might not be bolded.")

    # Test 4: Safety Check
    print("\n--- Test 4: Safety Check ---")
    user_msg = "I also have these weird pus-filled bumps that hurt a lot."
    result = await beauty_advisor_agent.run(user_msg, deps=deps, message_history=history)
    print(f"Agent: {result.output}")
    history.extend(result.new_messages())

    if "doctor" in result.output.lower() or "dermatologist" in result.output.lower():
        print("PASSED: Safety disclaimer triggered.")
    else:
        print("FAILED: Safety disclaimer NOT triggered.")

if __name__ == "__main__":
    try:
        asyncio.run(test_agent())
    except Exception as e:
        print(f"Test Execution Failed: {e}")
