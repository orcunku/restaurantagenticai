from __future__ import annotations

from datetime import datetime, timedelta

RESTAURANTS = {
    "vienna-table": {
        "name": "Vienna Table",
        "concept": "Modern Austrian",
        "city": "Vienna",
        "address": "Opernring 18, 1010 Wien",
        "phone": "+43 1 555 0188",
        "language": "de-AT",
        "status": "Live demo",
        "hours": "Mon–Sat 11:30–23:00 · Kitchen until 22:00 · Sun closed",
        "hero": "A busy city-centre restaurant using one AI front desk across calls, WhatsApp and web.",
        "menu": [
            {"name": "Wiener Schnitzel", "price": 24, "diet": "", "allergens": "A, C, G"},
            {"name": "Pumpkin Risotto", "price": 19, "diet": "Vegan", "allergens": "L"},
            {"name": "Alpine Trout", "price": 27, "diet": "", "allergens": "D, G"},
            {"name": "Gluten-free Pasta", "price": 21, "diet": "GF on request", "allergens": "Varies"},
        ],
        "policies": ["Terrace subject to availability", "Dogs welcome", "High chairs available", "Groups of 8+ are handed to staff", "Severe allergy requests always require human confirmation"],
        "integrations": ["Reservation system", "POS", "WhatsApp", "Phone", "Website"],
    },
    "alpine-stube": {
        "name": "Alpine Stube",
        "concept": "Tyrolean dining",
        "city": "Innsbruck",
        "address": "Maria-Theresien-Straße 31, 6020 Innsbruck",
        "phone": "+43 512 555 221",
        "language": "de-AT",
        "status": "Live demo",
        "hours": "Daily 12:00–22:30 · Kitchen until 21:45",
        "hero": "Tourism-heavy restaurant with multilingual guest requests and strong evening call volume.",
        "menu": [
            {"name": "Käsespätzle", "price": 18, "diet": "Vegetarian", "allergens": "A, C, G"},
            {"name": "Tiroler Gröstl", "price": 22, "diet": "", "allergens": "C"},
            {"name": "Mountain Salad", "price": 16, "diet": "Vegan", "allergens": "H"},
        ],
        "policies": ["Terrace closes at 21:00", "Walk-ins welcome", "Groups of 10+ require a deposit", "Allergy questions can be escalated to the kitchen"],
        "integrations": ["Reservation system", "Hotel PMS", "Phone", "Website"],
    },
    "porto-bistro": {
        "name": "Porto Bistro",
        "concept": "Mediterranean casual",
        "city": "Lisbon",
        "address": "Rua do Comércio 42, Lisboa",
        "phone": "+351 21 555 0192",
        "language": "pt-PT",
        "status": "Live demo",
        "hours": "Tue–Sun 12:00–00:00 · Mon closed",
        "hero": "A synthetic EU expansion example showing the same system localised outside DACH.",
        "menu": [
            {"name": "Grilled Sea Bass", "price": 25, "diet": "", "allergens": "Fish"},
            {"name": "Roasted Pepper Rice", "price": 17, "diet": "Vegan", "allergens": "None declared"},
            {"name": "Octopus Salad", "price": 19, "diet": "", "allergens": "Molluscs"},
        ],
        "policies": ["Outdoor seating subject to weather", "Large groups handled by staff", "English, Portuguese and Spanish supported"],
        "integrations": ["Reservation system", "POS", "WhatsApp", "Phone", "Website"],
    },
}

CHANNELS = [
    {"name": "Phone", "share": 44, "handled": 384, "resolution": 91},
    {"name": "WhatsApp", "share": 31, "handled": 271, "resolution": 94},
    {"name": "Web", "share": 25, "handled": 219, "resolution": 96},
]

KPI = {
    "conversations": 874,
    "reservations": 126,
    "guests": 318,
    "after_hours": 182,
    "hours_saved": 23.4,
    "estimated_value": 14310,
    "resolution_rate": 92,
    "handoffs": 29,
    "missed_calls_prevented": 146,
}

ACTIVITY = [
    {"time": "14:42", "channel": "Phone", "event": "Reservation created", "detail": "4 guests · 19:30 · Anna Berger", "value": "€180"},
    {"time": "14:38", "channel": "WhatsApp", "event": "Menu question resolved", "detail": "Vegan options · English", "value": "Auto"},
    {"time": "14:31", "channel": "Web", "event": "Reservation modified", "detail": "2 → 3 guests · terrace", "value": "Auto"},
    {"time": "14:19", "channel": "Phone", "event": "Human handoff", "detail": "Severe nut allergy confirmation", "value": "Safe"},
    {"time": "14:06", "channel": "Phone", "event": "Reservation created", "detail": "6 guests · 20:00 · Michael S.", "value": "€270"},
    {"time": "13:55", "channel": "WhatsApp", "event": "Hours answered", "detail": "Kitchen open until 22:00", "value": "Auto"},
]

CONVERSATIONS = [
    {"id": "C-2048", "channel": "Phone", "guest": "Anna Berger", "lang": "DE", "intent": "Reservation", "status": "Resolved", "summary": "Booked 4 guests for Friday 19:30. Terrace unavailable; guest accepted indoor table.", "duration": "1m 44s"},
    {"id": "C-2047", "channel": "WhatsApp", "guest": "Guest 7F21", "lang": "EN", "intent": "Dietary", "status": "Resolved", "summary": "Answered vegan menu question from verified menu knowledge.", "duration": "2m 08s"},
    {"id": "C-2046", "channel": "Phone", "guest": "Guest 91C2", "lang": "DE", "intent": "Allergy", "status": "Handoff", "summary": "Nut allergy request escalated to staff; no safety guarantee given by AI.", "duration": "0m 56s"},
    {"id": "C-2045", "channel": "Web", "guest": "Guest 3A11", "lang": "IT", "intent": "Location", "status": "Resolved", "summary": "Provided address and public-transport directions in Italian.", "duration": "1m 12s"},
]

WEEKLY = [
    {"day": "Mon", "conversations": 104, "reservations": 15},
    {"day": "Tue", "conversations": 118, "reservations": 17},
    {"day": "Wed", "conversations": 123, "reservations": 18},
    {"day": "Thu", "conversations": 131, "reservations": 20},
    {"day": "Fri", "conversations": 154, "reservations": 23},
    {"day": "Sat", "conversations": 168, "reservations": 25},
    {"day": "Sun", "conversations": 76, "reservations": 8},
]

RESERVATIONS = [
    {"time": "18:30", "name": "Lukas M.", "party": 2, "seating": "Indoor", "source": "Web", "status": "Confirmed", "value": 90},
    {"time": "19:00", "name": "Sofia R.", "party": 3, "seating": "Terrace", "source": "WhatsApp", "status": "Confirmed", "value": 135},
    {"time": "19:30", "name": "Anna Berger", "party": 4, "seating": "Indoor", "source": "Phone", "status": "Confirmed", "value": 180},
    {"time": "20:00", "name": "Michael S.", "party": 6, "seating": "Indoor", "source": "Phone", "status": "Confirmed", "value": 270},
    {"time": "20:30", "name": "Emily K.", "party": 2, "seating": "Terrace", "source": "Web", "status": "Confirmed", "value": 90},
]

DEMO_SCENARIOS = [
    {"label": "Book a table", "message": "I need a table for 4 this Friday at 19:30. My name is Anna Berger."},
    {"label": "Dietary question", "message": "Do you have a vegan main course?"},
    {"label": "Allergy safety", "message": "I have a severe nut allergy. Can you guarantee my meal is safe?"},
    {"label": "Opening hours", "message": "How late is the kitchen open tonight?"},
    {"label": "German request", "message": "Habt ihr Freitag um 20 Uhr einen Tisch für zwei auf der Terrasse?"},
]


def dashboard_payload(slug: str):
    restaurant = RESTAURANTS.get(slug, RESTAURANTS["vienna-table"])
    return {
        "restaurant": restaurant,
        "restaurants": [{"slug": s, "name": r["name"], "city": r["city"]} for s, r in RESTAURANTS.items()],
        "kpi": KPI,
        "channels": CHANNELS,
        "activity": ACTIVITY,
        "conversations": CONVERSATIONS,
        "weekly": WEEKLY,
        "reservations": RESERVATIONS,
        "scenarios": DEMO_SCENARIOS,
        "synthetic": True,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def demo_reply(slug: str, message: str):
    r = RESTAURANTS.get(slug, RESTAURANTS["vienna-table"])
    text = message.lower()
    trace = []
    if any(k in text for k in ["allergy", "allerg", "nut", "nuss", "nüsse"]):
        trace = ["Detected safety-sensitive dietary request", "Retrieved verified allergy policy", "Triggered human handoff"]
        return {
            "reply": f"I can share {r['name']}'s documented allergen information, but I can’t guarantee safety for a severe allergy. I’ve flagged this for the restaurant team so they can confirm directly with the kitchen.",
            "intent": "allergy",
            "action": "handoff_to_staff",
            "trace": trace,
            "synthetic": True,
        }
    if any(k in text for k in ["vegan", "vegetarian", "menu", "gericht", "essen"]):
        vegan = [m for m in r["menu"] if "Vegan" in m.get("diet", "")]
        item = vegan[0] if vegan else r["menu"][0]
        trace = ["Detected menu intent", "Searched restaurant knowledge", f"Matched menu item: {item['name']}"]
        return {
            "reply": f"Yes. One verified option is {item['name']} at €{item['price']}. If you have an allergy rather than a preference, I can hand that to the team for confirmation.",
            "intent": "menu",
            "action": "knowledge_answer",
            "trace": trace,
            "synthetic": True,
        }
    if any(k in text for k in ["open", "hours", "kitchen", "küche", "geöffnet", "uhr"]):
        trace = ["Detected opening-hours intent", "Retrieved current restaurant hours"]
        return {
            "reply": f"{r['name']}: {r['hours']}.",
            "intent": "hours",
            "action": "knowledge_answer",
            "trace": trace,
            "synthetic": True,
        }
    if any(k in text for k in ["table", "reservation", "reserv", "tisch", "book"]):
        terrace = any(k in text for k in ["terrace", "outside", "outdoor", "terrasse"])
        party = 4 if "4" in text or "four" in text else 2
        time = "19:30" if "19:30" in text else ("20:00" if "20" in text else "19:00")
        seating = "terrace" if terrace else "indoor"
        available = not (terrace and time == "20:00")
        if available:
            trace = ["Detected reservation intent", f"Checked availability: {party} guests · {time} · {seating}", "Created synthetic reservation", "Prepared confirmation"]
            return {
                "reply": f"Done — I’ve reserved a {seating} table for {party} at {time} in this synthetic demo. Confirmation reference: DEMO-{time.replace(':','')}-{party}.",
                "intent": "reservation",
                "action": "create_reservation",
                "trace": trace,
                "synthetic": True,
            }
        trace = ["Detected reservation intent", f"Checked availability: {party} guests · {time} · terrace", "Requested slot unavailable", "Generated alternatives"]
        return {
            "reply": f"The terrace is full at {time} in this demo. I can offer 19:00 on the terrace or {time} indoors. Which would you prefer?",
            "intent": "reservation",
            "action": "offer_alternative",
            "trace": trace,
            "synthetic": True,
        }
    trace = ["Classified general guest question", "Searched restaurant knowledge", "Generated grounded response"]
    return {
        "reply": f"I’m the synthetic AI front desk for {r['name']}. I can demonstrate reservations, opening hours, menu questions, dietary handling and staff handoff across phone, WhatsApp and web.",
        "intent": "general",
        "action": "knowledge_answer",
        "trace": trace,
        "synthetic": True,
    }
