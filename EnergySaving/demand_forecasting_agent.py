from uagents import Agent, Context
import random
import requests
import datetime

manager_url = "http://localhost:9000/receive"

# Create the demand forecasting agent
demand_forecaster = Agent(name="demand_forecaster", seed="YOUR_SECURE_SEED_4", port=8004, endpoint=["http://localhost:8004/submit"])

@demand_forecaster.on_interval(period=5.0)
async def forecast_demand(ctx: Context):
    # Simulate forecast values for consumption and production
    predicted_consumption = random.uniform(0.3, 0.7)  # in kWh
    predicted_production = random.uniform(0.0, 1.0)     # in kWh
    
    if predicted_consumption > predicted_production:
        action_message = f"Forecast indicates a deficit (consumption: {predicted_consumption:.2f} kWh, production: {predicted_production:.2f} kWh). Recommend adjusting procurement."
    else:
        action_message = f"Forecast indicates surplus (consumption: {predicted_consumption:.2f} kWh, production: {predicted_production:.2f} kWh). Recommend charging storage or selling surplus."
    
    # Build payload
    payload = {
        "agent_name": demand_forecaster.name,
        "message": action_message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(manager_url, json=payload)
        if response.status_code == 200:
            ctx.logger.info("Demand forecaster: Message sent successfully.")
        else:
            ctx.logger.error("Demand forecaster: Failed to send message.")
    except Exception as e:
        ctx.logger.error(f"Demand forecaster: Error sending message: {e}")

if __name__ == "__main__":
    demand_forecaster.run()
