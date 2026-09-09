from abc import ABC, abstractmethod
from datetime import UTC, datetime

import httpx


class ReservationAdapter(ABC):
    @abstractmethod
    async def check(self, restaurant, start_at: datetime, party_size: int, seating: str | None): ...
    @abstractmethod
    async def create(self, restaurant, payload: dict): ...
    @abstractmethod
    async def cancel(self, restaurant, provider_id: str): ...

class MockReservationAdapter(ReservationAdapter):
    async def check(self, restaurant, start_at, party_size, seating):
        if party_size > 8:
            return {"available": False, "reason": "groups_over_8_require_handoff", "alternatives": []}
        return {"available": True, "start_at": start_at.isoformat(), "seating": seating or "any"}
    async def create(self, restaurant, payload):
        return {"ok": True, "provider_id": f"mock-{int(datetime.now(UTC).timestamp())}", **payload}
    async def cancel(self, restaurant, provider_id):
        return {"ok": True, "provider_id": provider_id, "status": "cancelled"}

class WebhookReservationAdapter(ReservationAdapter):
    def _cfg(self, restaurant): return restaurant.reservation_config or {}
    async def _post(self, restaurant, path, body):
        cfg=self._cfg(restaurant); base=cfg.get("base_url"); token=cfg.get("token")
        if not base: raise RuntimeError("reservation_config.base_url missing")
        headers={"Authorization":f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.post(base.rstrip("/")+path, json=body, headers=headers); r.raise_for_status(); return r.json()
    async def check(self, restaurant, start_at, party_size, seating):
        return await self._post(restaurant,"/availability",{"start_at":start_at.isoformat(),"party_size":party_size,"seating":seating})
    async def create(self, restaurant, payload): return await self._post(restaurant,"/reservations",payload)
    async def cancel(self, restaurant, provider_id): return await self._post(restaurant,f"/reservations/{provider_id}/cancel",{})

def get_reservation_adapter(restaurant):
    return WebhookReservationAdapter() if restaurant.reservation_provider=="webhook" else MockReservationAdapter()
