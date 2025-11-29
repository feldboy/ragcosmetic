import asyncio
from agent import beauty_advisor_agent, BeautyAdvisorDependencies

async def main():
    deps = BeautyAdvisorDependencies()
    
    print("--- Test 1: Lead Warming ---")
    # User expresses a vague concern, agent should ask qualifying questions
    response1 = await beauty_advisor_agent.run("I want to look better for my wedding.", deps=deps)
    print(f"User: I want to look better for my wedding.\nAgent: {response1.output}\n")
    
    print("--- Test 2: Appointment Trigger ---")
    # User asks for a consultation
    history = response1.new_messages()
    response2 = await beauty_advisor_agent.run("I'm overwhelmed. Can I talk to someone?", deps=deps, message_history=history)
    print(f"User: I'm overwhelmed. Can I talk to someone?\nAgent: {response2.output}\n")
    
    print("--- Test 3: Check Availability ---")
    # User asks for availability
    history.extend(response2.new_messages())
    response3 = await beauty_advisor_agent.run("Yes, what times do you have tomorrow?", deps=deps, message_history=history)
    print(f"User: Yes, what times do you have tomorrow?\nAgent: {response3.output}\n")
    
    print("--- Test 4: Book Appointment ---")
    # User books a slot
    history.extend(response3.new_messages())
    response4 = await beauty_advisor_agent.run("Book me for 10:00. My name is Jane, phone 555-0199.", deps=deps, message_history=history)
    print(f"User: Book me for 10:00. My name is Jane, phone 555-0199.\nAgent: {response4.output}\n")

if __name__ == "__main__":
    asyncio.run(main())
