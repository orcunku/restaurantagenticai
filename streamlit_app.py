import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="HostAI | Restaurant Front Desk",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --bg: #F5F3EE;
        --panel: #FFFFFF;
        --ink: #18201D;
        --muted: #69716D;
        --line: #E4E2DC;
        --accent: #173D32;
        --sidebar: #10261F;
        --soft: #E7EEE9;
        --warm: #F3ECE0;
        --danger: #8B3F37;
    }

    .stApp {
        background: var(--bg);
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: var(--sidebar);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.15);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .eyebrow {
        color: #69716D;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero {
        background: #173D32;
        color: white;
        border-radius: 18px;
        padding: 38px 42px;
        margin: 22px 0 28px 0;
    }

    .hero-pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 42px;
        line-height: 1.08;
        margin: 0 0 15px 0;
        max-width: 700px;
    }

    .hero p {
        color: rgba(255,255,255,.78);
        font-size: 17px;
        max-width: 700px;
    }

    .card {
        background: white;
        border: 1px solid #E4E2DC;
        border-radius: 14px;
        padding: 22px;
        min-height: 130px;
        box-shadow: 0 5px 18px rgba(16,38,31,.04);
    }

    .metric-label {
        color: #69716D;
        font-size: 13px;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #18201D;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .metric-detail {
        color: #69716D;
        font-size: 13px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #18201D;
        margin-bottom: 4px;
    }

    .soft-card {
        background: #E7EEE9;
        border-radius: 14px;
        padding: 22px;
    }

    .warm-card {
        background: #F3ECE0;
        border-radius: 14px;
        padding: 22px;
    }

    .status {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 999px;
        background: #E7EEE9;
        color: #173D32;
        font-size: 12px;
        font-weight: 700;
    }

    .synthetic {
        font-size: 12px;
        color: rgba(255,255,255,.65);
        line-height: 1.5;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: #173D32;
        border-color: #173D32;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SYNTHETIC DEMO DATA
# ---------------------------------------------------------

restaurants = {
    "Vienna Table · Vienna": {
        "name": "Vienna Table",
        "concept": "Modern Austrian",
        "city": "Vienna",
        "description": (
            "A busy city-centre restaurant using one AI front desk "
            "across calls, WhatsApp and web."
        ),
    },
    "Alpine Stube · Innsbruck": {
        "name": "Alpine Stube",
        "concept": "Tyrolean dining",
        "city": "Innsbruck",
        "description": (
            "A high-volume Alpine restaurant handling guest questions "
            "and reservations across multiple channels."
        ),
    },
    "Porto Bistro · Lisbon": {
        "name": "Porto Bistro",
        "concept": "Mediterranean casual",
        "city": "Lisbon",
        "description": (
            "A busy Mediterranean restaurant using HostAI to support "
            "international guests and reservations."
        ),
    },
}

kpis = [
    ("Conversations", "874", "Across all channels"),
    ("Reservations created", "126", "318 guests booked"),
    ("After-hours handled", "182", "No staff needed"),
    ("Missed calls prevented", "146", "Estimated"),
    ("Resolution rate", "92%", "29 safe handoffs"),
    ("Staff time saved", "23.4 h", "Estimated"),
    ("Booking value", "€14.3k", "AI-assisted estimate"),
    ("Active channels", "3", "Phone · WhatsApp · Web"),
]

weekly = pd.DataFrame(
    {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Conversations": [94, 106, 112, 119, 143, 171, 129],
    }
)

reservations = pd.DataFrame(
    [
        ["18:30", "Anna M.", 2, "Dining room", "Phone", "Confirmed", "€90"],
        ["19:00", "David K.", 4, "Dining room", "WhatsApp", "Confirmed", "€180"],
        ["19:30", "Sophie L.", 3, "Terrace", "Web", "Confirmed", "€135"],
        ["20:00", "Marco R.", 5, "Dining room", "Phone", "Confirmed", "€225"],
        ["20:30", "Julia S.", 2, "Dining room", "Web", "Confirmed", "€90"],
    ],
    columns=["Time", "Guest", "Party", "Seating", "Source", "Status", "Est. value"],
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Overview"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello — I'm the digital assistant for Vienna Table. "
                "I can help with reservations, menu questions, opening "
                "hours and guest requests."
            ),
        }
    ]

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("## H  HostAI")
    st.caption("Restaurant Front Desk")

    st.markdown("---")

    pages = [
        "Overview",
        "Live Agent",
        "Reservations",
        "Conversations",
        "Knowledge",
        "Integrations",
    ]

    for page in pages:
        if st.button(page, use_container_width=True, key=f"nav_{page}"):
            st.session_state.page = page
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <div class="synthetic">
        ● Synthetic demo data<br><br>
        No real guest or restaurant data is used.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------

top_left, top_right = st.columns([2, 1])

with top_left:
    st.markdown('<div class="eyebrow">CLIENT DEMO ENVIRONMENT</div>',
                unsafe_allow_html=True)

with top_right:
    restaurant_choice = st.selectbox(
        "Restaurant",
        list(restaurants.keys()),
        label_visibility="collapsed",
    )

restaurant = restaurants[restaurant_choice]

st.title(restaurant["name"])

# ---------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------

if st.session_state.page == "Overview":

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-pill">
                AI FRONT DESK · PHONE + WHATSAPP + WEB
            </div>

            <h1>Every guest conversation,<br>
            handled intelligently.</h1>

            <p>{restaurant["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show the agent", type="primary",
                     use_container_width=True):
            st.session_state.page = "Live Agent"
            st.rerun()

    with col2:
        if st.button("See what it knows", use_container_width=True):
            st.session_state.page = "Knowledge"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">LAST 30 DAYS</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Business impact</div>',
        unsafe_allow_html=True,
    )
    st.caption("Synthetic performance scenario")

    for row_start in range(0, 8, 4):
        cols = st.columns(4)

        for col, metric in zip(cols, kpis[row_start:row_start + 4]):
            label, value, detail = metric

            with col:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-detail">{detail}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown('<div class="eyebrow">VOLUME</div>',
                    unsafe_allow_html=True)
        st.subheader("Conversations by day")
        st.bar_chart(
            weekly,
            x="Day",
            y="Conversations",
            use_container_width=True,
        )

    with right:
        st.markdown('<div class="eyebrow">CHANNELS</div>',
                    unsafe_allow_html=True)
        st.subheader("One agent, everywhere")

        st.write("**Phone** — 44%")
        st.progress(44)
        st.caption("384 handled · 91% AI resolution")

        st.write("**WhatsApp** — 31%")
        st.progress(31)
        st.caption("271 handled · 94% AI resolution")

        st.write("**Web** — 25%")
        st.progress(25)
        st.caption("219 handled · 96% AI resolution")

    st.markdown("---")
    st.markdown('<div class="eyebrow">LIVE OPERATIONS</div>',
                unsafe_allow_html=True)
    st.subheader("What the AI is doing")

    activity = pd.DataFrame(
        [
            ["20:41", "Phone", "Reservation created",
             "Table for 4 · 19:30", "€180"],
            ["20:36", "WhatsApp", "Opening hours answered",
             "Kitchen closes at 22:00", "Resolved"],
            ["20:28", "Web", "Allergy request",
             "Escalated safely to staff", "Handoff"],
            ["20:17", "Phone", "Reservation modified",
             "2 → 4 guests", "Updated"],
            ["20:09", "Web", "Menu question",
             "Vegan options explained", "Resolved"],
        ],
        columns=["Time", "Channel", "Event", "Detail", "Outcome"],
    )

    st.dataframe(activity, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# LIVE AGENT
# ---------------------------------------------------------

elif st.session_state.page == "Live Agent":

    st.markdown('<div class="eyebrow">INTERACTIVE DEMO</div>',
                unsafe_allow_html=True)
    st.header("Run a guest scenario")

    st.caption(
        "Synthetic restaurant knowledge and mock reservation actions. "
        "No external AI API is required."
    )

    chat_col, trace_col = st.columns([1.25, 1])

    with chat_col:
        st.subheader(f"{restaurant['name']} AI")
        st.caption("Digital front desk · online")

        scenario_cols = st.columns(4)

        scenario_messages = [
            "I'd like a table for 4 tonight at 19:30.",
            "Do you have vegan options?",
            "I have a severe nut allergy. Is everything safe?",
            "What time does the kitchen close?",
        ]

        scenario_names = [
            "Book a table",
            "Dietary",
            "Allergy",
            "Hours",
        ]

        for col, name, message in zip(
            scenario_cols,
            scenario_names,
            scenario_messages,
        ):
            with col:
                if st.button(name, use_container_width=True):
                    st.session_state.messages.append(
                        {"role": "user", "content": message}
                    )

                    if name == "Book a table":
                        reply = (
                            "Absolutely. I found availability for 4 guests "
                            "at 19:30. I've created the synthetic demo "
                            "reservation ✓"
                        )
                    elif name == "Dietary":
                        reply = (
                            "Yes. Our verified menu includes Pumpkin Risotto, "
                            "which is vegan. I can also explain documented "
                            "allergen information."
                        )
                    elif name == "Allergy":
                        reply = (
                            "For a severe allergy, I won't make a safety "
                            "guarantee. I'll escalate this request to the "
                            "restaurant team for confirmation."
                        )
                    else:
                        reply = (
                            "Vienna Table is open until 23:00 and the kitchen "
                            "closes at 22:00."
                        )

                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )
                    st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        guest_message = st.chat_input(
            "Try: table for 4 tonight at 19:30"
        )

        if guest_message:
            st.session_state.messages.append(
                {"role": "user", "content": guest_message}
            )

            text = guest_message.lower()

            if "allerg" in text:
                answer = (
                    "For severe allergies, I can explain documented "
                    "information but I need restaurant staff to confirm "
                    "safety. I'm escalating this request."
                )
            elif "table" in text or "reservation" in text or "book" in text:
                answer = (
                    "I can help with that. For this synthetic demo, "
                    "availability has been checked and a reservation "
                    "workflow would now be completed."
                )
            elif "vegan" in text:
                answer = (
                    "Yes — the verified demo menu includes Pumpkin Risotto, "
                    "which is vegan."
                )
            elif "hour" in text or "close" in text or "open" in text:
                answer = (
                    "The restaurant is open until 23:00 and the kitchen "
                    "closes at 22:00."
                )
            else:
                answer = (
                    "I can help with reservations, opening hours, menu "
                    "questions and guest requests."
                )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()

    with trace_col:
        st.markdown('<div class="eyebrow">AGENTIC WORKFLOW</div>',
                    unsafe_allow_html=True)
        st.subheader("What happens behind the answer")

        st.markdown(
            """
            <div class="soft-card">
            <b>1. Guest request received</b><br><br>
            ↓<br><br>
            <b>2. Intent classified</b><br><br>
            ↓<br><br>
            <b>3. Restaurant knowledge retrieved</b><br><br>
            ↓<br><br>
            <b>4. Availability / policy checked</b><br><br>
            ↓<br><br>
            <b>5. Action completed or escalated</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# RESERVATIONS
# ---------------------------------------------------------

elif st.session_state.page == "Reservations":

    st.markdown('<div class="eyebrow">TONIGHT</div>',
                unsafe_allow_html=True)
    st.header("AI-generated reservations")

    st.caption(
        "A synthetic reservation book showing how phone, WhatsApp "
        "and web converge into one workflow."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tonight", "5")
    c2.metric("Guests", "16")
    c3.metric("Booking value", "€720")
    c4.metric("Channels", "3")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(
        reservations,
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------
# CONVERSATIONS
# ---------------------------------------------------------

elif st.session_state.page == "Conversations":

    st.markdown('<div class="eyebrow">QUALITY & CONTROL</div>',
                unsafe_allow_html=True)
    st.header("Conversation review")

    st.caption(
        "Managers can inspect outcomes and see where the AI handed "
        "work to a human."
    )

    conversations = pd.DataFrame(
        [
            ["C-1042", "Phone", "DE", "Reservation",
             "Anna M.", "Table for two booked", "Resolved", "2m 14s"],
            ["C-1041", "WhatsApp", "EN", "Allergy",
             "David K.", "Severe allergy escalated", "Handoff", "3m 02s"],
            ["C-1040", "Web", "EN", "Menu",
             "Sophie L.", "Vegan options explained", "Resolved", "1m 08s"],
            ["C-1039", "Phone", "DE", "Hours",
             "Marco R.", "Opening hours answered", "Resolved", "0m 48s"],
        ],
        columns=[
            "ID", "Channel", "Language", "Intent",
            "Guest", "Summary", "Status", "Duration"
        ],
    )

    st.dataframe(
        conversations,
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------
# KNOWLEDGE
# ---------------------------------------------------------

elif st.session_state.page == "Knowledge":

    st.markdown('<div class="eyebrow">GROUNDING LAYER</div>',
                unsafe_allow_html=True)
    st.header("Restaurant knowledge")

    st.caption(
        "The AI answers from verified restaurant-specific "
        "information instead of guessing."
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Profile")
        st.markdown(
            f"""
            <div class="card">
            <b>Restaurant</b><br>{restaurant["name"]}<br><br>
            <b>Concept</b><br>{restaurant["concept"]}<br><br>
            <b>Location</b><br>{restaurant["city"]}<br><br>
            <b>Language</b><br>German / English
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("Policies")
        st.markdown(
            """
            <div class="card">
            Terrace seating depends on availability.<br><br>
            Dogs are welcome where operationally possible.<br><br>
            High chairs are available.<br><br>
            Groups of 8+ are handed to restaurant staff.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Verified dishes")

        menu = pd.DataFrame(
            [
                ["Wiener Schnitzel", "€24", "A, C, G"],
                ["Pumpkin Risotto", "€19 · Vegan", "L"],
                ["Alpine Trout", "€27", "D, G"],
                ["Gluten-free Pasta", "€21 · GF on request", "Varies"],
            ],
            columns=["Dish", "Price / status", "Allergens"],
        )

        st.dataframe(menu, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="warm-card">
            <b>Safe by design</b><br><br>
            The agent may explain documented allergen information,
            but severe allergy assurances are always escalated to staff.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# INTEGRATIONS
# ---------------------------------------------------------

elif st.session_state.page == "Integrations":

    st.markdown('<div class="eyebrow">SYSTEM LAYER</div>',
                unsafe_allow_html=True)
    st.header("Fits the restaurant's existing stack")

    st.caption(
        "Production deployments connect the same action layer to "
        "the client's existing systems."
    )

    st.markdown(
        """
        <div class="hero">
            <div style="font-size:20px;font-weight:700">
            Guests
            &nbsp; → &nbsp;
            HostAI Agent
            &nbsp; → &nbsp;
            Restaurant Tools
            </div>

            <p>
            Phone · WhatsApp · Web
            &nbsp;&nbsp; → &nbsp;&nbsp;
            Intent · Knowledge · Actions
            &nbsp;&nbsp; → &nbsp;&nbsp;
            Reservations · POS · CRM
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    integrations = [
        "Reservation system",
        "POS",
        "WhatsApp",
        "Phone",
        "Website",
        "Hotel PMS",
    ]

    cols = st.columns(3)

    for i, integration in enumerate(integrations):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">INTEGRATION</div>
                    <div style="font-size:19px;font-weight:700">
                        {integration}
                    </div>
                    <br>
                    <span class="status">Demo adapter ready</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Adapter-first architecture")

    st.info(
        "Each external provider sits behind a stable internal contract. "
        "The AI workflow therefore remains consistent when a restaurant "
        "uses a different reservation, POS or messaging system."
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.caption(
    "HostAI · Restaurant Front Desk · Synthetic client demonstration · "
    "No real guest or restaurant data is used."
)
