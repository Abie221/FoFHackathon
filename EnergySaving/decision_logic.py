# decision_logic.py
from decision_models import DecisionInput, DecisionOutput

def make_decision(decision_input: DecisionInput) -> DecisionOutput:
    net_energy = decision_input.production - decision_input.consumption

    # Initialize output variables
    energy_added_to_storage = 0.0
    energy_sold_to_grid = 0.0
    energy_bought_from_storages = 0.0
    energy_bought_from_grid = 0.0

    if net_energy >= 0:
        # Surplus: Store half, sell the rest.
        energy_added_to_storage = net_energy * 0.5
        energy_sold_to_grid = net_energy - energy_added_to_storage
    else:
        # Deficit: First, use stored energy
        deficit = -net_energy  # absolute deficit
        total_storage_energy = sum(decision_input.storage_levels.values())
        energy_bought_from_storages = min(deficit, total_storage_energy)
        energy_bought_from_grid = max(0.0, deficit - energy_bought_from_storages)

    return DecisionOutput(
        energy_added_to_storage=energy_added_to_storage,
        energy_sold_to_grid=energy_sold_to_grid,
        energy_bought_from_storages=energy_bought_from_storages,
        energy_bought_from_grid=energy_bought_from_grid
    )
