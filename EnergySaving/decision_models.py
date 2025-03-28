# decision_models.py
from pydantic import BaseModel
from typing import Dict

class DecisionInput(BaseModel):
    production: float
    consumption: float
    storage_levels: Dict[str, float]  # {storage_name: current_level}
    grid_purchase_price: float
    grid_sale_price: float
    p2p_base_price: float
    token_balance: float

class DecisionOutput(BaseModel):
    energy_added_to_storage: float
    energy_sold_to_grid: float
    energy_bought_from_storages: float
    energy_bought_from_grid: float
