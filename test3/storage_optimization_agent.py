from uagents import Agent, Context
import random
import requests
import datetime

# URL for the AI Manager API server
manager_url = "http://localhost:9000/receive"

# Create the storage optimizer agent
storage_agent = Agent(name="storage_optimizer", seed="YOUR_SECURE_SEED_2", port=8002, endpoint=["http://localhost:8002/submit"])

@storage_agent.on_interval(period=5.0)
async def optimize_storage(ctx: Context):
    # Simulate storage metrics (in a real system, these would come from actual data)
    storage_levels = {
        "storage_A": {"current_level": random.uniform(0, 100), "capacity": 100},
        "storage_B": {"current_level": random.uniform(0, 200), "capacity": 200}
    }
    
    recommendations = []
    for name, data in storage_levels.items():
        current_level = data["current_level"]
        capacity = data["capacity"]
        charge_ratio = current_level / capacity
        
        if charge_ratio < 0.3:
            rec = f"{name} undercharged ({charge_ratio:.2%}). Recommend increasing charging."
        elif charge_ratio > 0.8:
            rec = f"{name} nearly full ({charge_ratio:.2%}). Recommend discharging to utilize surplus."
        else:
            rec = f"{name} optimal ({charge_ratio:.2%}). No action needed."
        
        recommendations.append(rec)
    
    # Build message payload
    payload = {
        "agent_name": storage_agent.name,
        "message": " | ".join(recommendations),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send the payload to the AI Manager server
    try:
        response = requests.post(manager_url, json=payload)
        if response.status_code == 200:
            ctx.logger.info("Storage optimizer: Message sent successfully.")
        else:
            ctx.logger.error("Storage optimizer: Failed to send message.")
    except Exception as e:
        ctx.logger.error(f"Storage optimizer: Error sending message: {e}")

if __name__ == "__main__":
    storage_agent.run()
