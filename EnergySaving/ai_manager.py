import multiprocessing
import time

def run_token_economist():
    from token_agent import token_agent
    token_agent.run()

def run_storage_optimizer():
    from storage_optimization_agent import storage_agent
    storage_agent.run()

def run_grid_trader():
    from grid_trading_agent import grid_trading_agent
    grid_trading_agent.run()

def run_demand_forecaster():
    from demand_forecasting_agent import demand_forecaster
    demand_forecaster.run()

def run_p2p_trader():
    from peet_to_peer_trading import p2p_trading_agent
    p2p_trading_agent.run()

if __name__ == '__main__':
    # Create processes for each agent
    agents = [
        multiprocessing.Process(target=run_token_economist),
        multiprocessing.Process(target=run_storage_optimizer),
        multiprocessing.Process(target=run_grid_trader),
        multiprocessing.Process(target=run_demand_forecaster),
        multiprocessing.Process(target=run_p2p_trader)
    ]
    
    # Start all agents
    for agent in agents:
        agent.start()
    
    print("All agents are running. Press Ctrl+C to terminate.")
    
    try:
        # Keep the main process alive while agents run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating agents...")
        for agent in agents:
            agent.terminate()
        print("All agents terminated.")
