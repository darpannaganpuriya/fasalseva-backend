from typing import Any

from app.services.ml_service import predict_price, predict_shelf_life


class DecisionService:
    def __init__(self) -> None:
        self.storage_cost_per_kg_per_day = 0.2
        self.transport_cost_per_kg = 1.5

    def generate_recommendation(self, crop: str, quantity_kg: float, current_price: float, temperature: float, humidity: float, days_stored: float, state: str, district: str, month: int, week: int) -> dict[str, Any]:
        shelf_life = predict_shelf_life(crop, temperature, humidity, days_stored)
        price = predict_price(crop, state, district, current_price, month, week)

        store_days = min(shelf_life["days_remaining"], 15)
        sell_now_revenue = quantity_kg * (current_price / 100)
        store_revenue = quantity_kg * (price["predicted_price"] / 100)
        storage_cost = quantity_kg * self.storage_cost_per_kg_per_day * store_days
        transport_cost = quantity_kg * self.transport_cost_per_kg

        sell_now_profit = sell_now_revenue - transport_cost
        store_profit = store_revenue - storage_cost - transport_cost
        process_profit = (quantity_kg * ((current_price / 100) * 0.85)) - (transport_cost * 0.7)

        options = {
            "sell_now": sell_now_profit,
            "store": store_profit,
            "process": process_profit,
        }
        best_action = max(options, key=options.get)

        action_map = {
            "sell_now": "Sell Today",
            "store": "Store Crop",
            "process": "Sell to Processing",
        }

        return {
            "recommended_action": action_map[best_action],
            "store_duration": store_days if best_action == "store" else 0,
            "expected_profit": round(options[best_action]),
            "recommendation": shelf_life["recommendation"],
            "shelf_life": shelf_life,
            "price": price,
        }


decision_service = DecisionService()
