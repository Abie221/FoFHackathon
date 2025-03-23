from uagents import Agent, Context
import random
import requests
import datetime

# URL of the AI Manager API server
manager_url = "http://localhost:9000/receive"

# Create the token economist agent
token_agent = Agent(name="token_economist", seed="YOUR_SECURE_SEED", port=8000, endpoint=["http://localhost:8000/submit"])

@token_agent.on_interval(period=5.0)
async def adjust_token_economics(ctx: Context):
    # Simulate demand level (0 to 1)
    demand_level = random.random()
    ctx.logger.info(f"Current simulated demand level: {demand_level:.2f}")
    
    # Decide an action based on demand
    if demand_level > 0.7:
        action_message = "High demand detected: Increasing token burn rate."
    else:
        action_message = "Demand normal: Maintaining current token parameters."
    
    # Build message payload
    payload = {
        "agent_name": token_agent.name,
        "message": action_message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send message to the AI Manager API server
    try:
        response = requests.post(manager_url, json=payload)
        if response.status_code == 200:
            ctx.logger.info("Message sent to manager successfully.")
        else:
            ctx.logger.error("Failed to send message to manager.")
    except Exception as e:
        ctx.logger.error(f"Error sending message: {e}")

if __name__ == "__main__":
    token_agent.run()
