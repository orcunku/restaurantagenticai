import httpx


class POSAdapter:
    async def menu(self, restaurant):
        cfg=restaurant.pos_config or {}
        if restaurant.pos_provider != "webhook" or not cfg.get("base_url"):
            return None
        headers={"Authorization":f"Bearer {cfg['token']}"} if cfg.get("token") else {}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(cfg["base_url"].rstrip("/")+"/menu",headers=headers); r.raise_for_status(); return r.json()
