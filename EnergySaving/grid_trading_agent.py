from uagents import Agent, Context
import random
import requests
import datetime

manager_url = "http://localhost:9000/receive"

# Create the grid trading agent
grid_trading_agent = Agent(name="grid_trader", seed="YOUR_SECURE_SEED_3", port=8003, endpoint=["http://localhost:8003/submit"])

@grid_trading_agent.on_interval(period=5.0)
async def grid_trading(ctx: Context):
    # Simulate current grid prices
    current_purchase_price = random.uniform(0.3, 0.5)  # Price to buy energy
    current_sale_price = random.uniform(0.2, 0.4)      # Price to sell energy
    
    # Determine recommendation based on pricing thresholds
    if current_sale_price > 0.35:
        action_message = f"High sale price detected ({current_sale_price:.2f} CT/kWh). Recommend selling surplus energy."
    elif current_purchase_price < 0.35:
        action_message = f"Low purchase price detected ({current_purchase_price:.2f} CT/kWh). Recommend buying energy to cover deficits."
    else:
        action_message = "Grid prices are moderate. No grid trading adjustments recommended."
    
    # Build payload
    payload = {
        "agent_name": grid_trading_agent.name,
        "message": action_message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send the payload
    try:
        response = requests.post(manager_url, json=payload)
        if response.status_code == 200:
            ctx.logger.info("Grid trader: Message sent successfully.")
        else:
            ctx.logger.error("Grid trader: Failed to send message.")
    except Exception as e:
        ctx.logger.error(f"Grid trader: Error sending message: {e}")

if __name__ == "__main__":
    grid_trading_agent.run()
