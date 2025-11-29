import asyncio
import os
from agent import beauty_advisor_agent, BeautyAdvisorDependencies
from pydantic_ai import Agent

# Set API key if not already set (for testing purposes, assume user has it in env or we prompt)
if "OPENROUTER_API_KEY" not in os.environ:
    # os.environ["OPENROUTER_API_KEY"] = "..." # User needs to provide this
    pass

async def main():
    print("✨ Welcome to your Digital Beauty Advisor! ✨")
    print("(Type 'quit' to exit)")
    
    deps = BeautyAdvisorDependencies()
    
    # Start the conversation
    # We maintain history implicitly via the agent's run method if we were using a persistent conversation,
    # but for a simple CLI loop with Pydantic AI, we might need to manage messages if we want context.
    # Pydantic AI agents are stateless by default unless we pass history.
    
    history = []
    
    # Initial greeting from the agent? 
    # The prompt says "Start with positive energy", but usually the user initiates or the system triggers.
    # Let's have the agent start.
    
    # Actually, the prompt examples show the User speaking first or the Agent reacting.
    # Let's simulate the Agent starting the conversation as per "Step 1: Connect & Discover".
    # We can prompt the agent to start.
    
    try:
        # Initial trigger to get the agent to say hello
        result = await beauty_advisor_agent.run(
            "The user has just arrived. Start the conversation according to your instructions.", 
            deps=deps
        )
        print(f"\nAdvisor: {result.output}\n")
        history.extend(result.new_messages())

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            result = await beauty_advisor_agent.run(
                user_input, 
                deps=deps, 
                message_history=history
            )
            print(f"\nAdvisor: {result.output}\n")
            history.extend(result.new_messages())
            
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have set the OPENROUTER_API_KEY environment variable.")

if __name__ == "__main__":
    asyncio.run(main())
