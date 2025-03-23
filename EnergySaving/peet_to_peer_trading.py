from uagents import Agent, Context
import random
import requests
import datetime

manager_url = "http://localhost:9000/receive"

# Create the P2P trading agent
p2p_trading_agent = Agent(name="p2p_trader", seed="YOUR_SECURE_SEED_5", port=8005, endpoint=["http://localhost:8005/submit"])

@p2p_trading_agent.on_interval(period=5.0)
async def p2p_trading(ctx: Context):
    # Simulate offers from a seller and a buyer
    seller_offer_price = random.uniform(0.4, 0.6)  # Seller's asking price
    buyer_offer_price = random.uniform(0.3, 0.5)   # Buyer's offer price
    
    if seller_offer_price < buyer_offer_price:
        profit_margin = buyer_offer_price - seller_offer_price
        action_message = f"Profitable trade detected: Profit margin of {profit_margin:.2f} CT/kWh. Recommend initiating negotiation."
    else:
        action_message = "No profitable P2P trade available at the moment."
    
    # Build payload
    payload = {
        "agent_name": p2p_trading_agent.name,
        "message": action_message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(manager_url, json=payload)
        if response.status_code == 200:
            ctx.logger.info("P2P trader: Message sent successfully.")
        else:
            ctx.logger.error("P2P trader: Failed to send message.")
    except Exception as e:
        ctx.logger.error(f"P2P trader: Error sending message: {e}")

if __name__ == "__main__":
    p2p_trading_agent.run()
