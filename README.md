# Energy AI Agents Simulation & Coordination

This project implements a decentralized AI-driven system to optimize token economics in an energy simulation. Multiple independent agents monitor various aspects (such as grid trading, storage, demand, and peer-to-peer opportunities) and send their recommendations as JSON messages to a central AI Manager server. The AI Manager aggregates these messages and makes a coordinated decision that can be used to dynamically adjust simulation parameters to improve token savings.

## Overview

### Architecture

- **AI Manager API Server**  
  A Flask-based API server that receives JSON messages from all agents. It provides:
  - **`/receive` Endpoint:** Accepts POST requests from agents.
  - **`/messages` Endpoint:** Returns all received messages.
  - **`/aggregate` Endpoint:** Aggregates agent recommendations into a single coordinated decision.

- **Agents**  
  Implemented using Fetch.ai's agent framework (uagents), each agent monitors a specific aspect:
  - **Token Economist Agent:** Monitors demand and suggests adjustments to token burn rates.
  - **Storage Optimizer Agent:** Checks storage levels and recommends charging/discharging actions.
  - **Grid Trading Agent:** Observes grid prices and advises on buying or selling energy.
  - **Demand Forecasting Agent:** Forecasts consumption vs. production and recommends procurement adjustments.
  - **Peer-to-Peer Trading Agent:** Looks for profitable trade opportunities among community members.

- **AI Manager Launcher**  
  A Python script that uses multiprocessing to run all agents concurrently, so they can send their recommendations to the AI Manager server.

### Communication Flow

1. **Agents → Server:**  
   Each agent periodically sends a JSON payload with its recommendation (e.g., “High demand detected: Increasing token burn rate.”) to `http://localhost:9000/receive`.

2. **Server Aggregation:**  
   The server collects these messages, which you can view at `http://localhost:9000/messages`.  
   It also processes these messages using simple aggregation logic (e.g., counting key terms) to produce a final decision. You can view this aggregated decision at `http://localhost:9000/aggregate`.

3. **Impact on Simulation:**  
   The coordinated decision (e.g., “Increase token burn rate and adjust procurement.”) is intended to be used by your simulation to optimize operations and ultimately save tokens.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd energy-ai-agents-simulation
    ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
   Ensure `Flask` and the Fetch.ai `uagents` library are listed in your `requirements.txt`.

## Running the System

### 1. Start the AI Manager API Server

- Open a terminal and run:
  ```bash
  python ai_manager_server.py
  ```
- The server will start on port 9000.
- In your browser, navigate to [http://localhost:9000/](http://localhost:9000/). You should see:
  ```
  Welcome to the AI Manager API server. Use POST /receive to send messages.
  ```
- To view all messages, go to: [http://localhost:9000/messages](http://localhost:9000/messages).  
- To view the aggregated decision, visit: [http://localhost:9000/aggregate](http://localhost:9000/aggregate).

### 2. Launch the Agents

- Open a second terminal and run:
  ```bash
  python ai_manager.py
  ```
- This script starts all agents concurrently using multiprocessing.
- Each agent will send its recommendation to the server every 5 seconds.

### 3. Monitor the Outputs

- **Agent Messages:**  
  Check [http://localhost:9000/messages](http://localhost:9000/messages) to see a JSON array of all recommendations.  
  Example output:
  ```json
  [
    {"agent_name": "grid_trader", "message": "Low purchase price detected (0.33 CT/kWh). Recommend buying energy to cover deficits.", "timestamp": "2025-03-22 19:39:10"},
    {"agent_name": "token_economist", "message": "High demand detected: Increasing token burn rate.", "timestamp": "2025-03-22 19:39:10"},
    {"agent_name": "storage_optimizer", "message": "storage_A optimal (65.35%). No action needed. | storage_B undercharged (29.39%). Recommend increasing charging.", "timestamp": "2025-03-22 19:39:10"},
    {"agent_name": "demand_forecaster", "message": "Forecast indicates a deficit (consumption: 0.48 kWh, production: 0.34 kWh). Recommend adjusting procurement.", "timestamp": "2025-03-22 19:39:10"},
    {"agent_name": "p2p_trader", "message": "No profitable P2P trade available at the moment.", "timestamp": "2025-03-22 19:39:10"}
  ]
  ```

- **Aggregated Decision:**  
  Check [http://localhost:9000/aggregate](http://localhost:9000/aggregate) to see the consolidated decision.  
  Example output:
  ```json
  {
    "action": "Increase token burn rate and adjust procurement.",
    "details": {
      "high_demand_count": 5,
      "deficit_count": 6,
      "surplus_count": 9,
      "undercharged_count": 5,
      "optimal_count": 8
    },
    "timestamp": "2025-03-22 19:47:17"
  }
  ```

## How It Works

- **Agents:**  
  Each agent monitors a specific aspect of the simulation (e.g., grid prices, storage levels) and sends its recommendation as a JSON message to the AI Manager server at regular intervals.

- **AI Manager Server:**  
  The server collects these messages and stores them in an in-memory list. It provides endpoints to view all messages (`/messages`) and to view an aggregated decision (`/aggregate`), which applies simple rules (e.g., counting keywords) to generate a consolidated action.

- **Aggregated Decision Usage:**  
  The final decision is intended to guide the simulation in adjusting parameters—such as increasing the token burn rate or modifying procurement strategies—to optimize token savings. This decision can later be integrated directly into your simulation.

## Future Enhancements

- **Refine Decision Logic:**  
  Develop more sophisticated aggregation rules or use machine learning to weigh recommendations.
- **Integrate with Simulation:**  
  Use the aggregated decision to dynamically update simulation parameters in real-time.
- **Build a Dashboard:**  
  Create a monitoring dashboard to visualize agent messages, aggregated decisions, and simulation performance.
