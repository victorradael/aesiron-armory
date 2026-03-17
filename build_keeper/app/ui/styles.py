import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        /* Base Colors & Typography */
        :root {
            --primary-bg:      #8b5cf6;
            --primary-hover:   #7c3aed;
            --success:         #10b981;
            --danger:          #f87171;
            --card-bg:         #242434;
            --card-border:     rgba(139, 92, 246, 0.2);
            --text-primary:    #e8e8f0;
            --text-secondary:  #9494b0;
            --border-radius:   12px;
            --glow:            rgba(139, 92, 246, 0.3);
        }

        /* Buttons Styling */
        .stButton>button {
            border-radius: var(--border-radius) !important;
            transition: all 0.2s ease-in-out !important;
            border: 1px solid var(--card-border) !important;
            color: var(--text-primary) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--glow);
            border-color: var(--primary-bg) !important;
            color: var(--primary-bg) !important;
        }

        /* Primary Buttons overrides */
        [data-testid="baseButton-primary"] {
            background-color: var(--primary-bg) !important;
            color: white !important;
            border: none !important;
        }
        [data-testid="baseButton-primary"]:hover {
            background-color: var(--primary-hover) !important;
            color: white !important;
            box-shadow: 0 4px 12px var(--glow) !important;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            border-radius: var(--border-radius) !important;
            background-color: var(--card-bg) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 10px 15px !important;
        }
        .streamlit-expanderContent {
            border: 1px solid var(--card-border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--border-radius) var(--border-radius) !important;
        }

        /* Text Inputs & Checkboxes */
        .stTextInput>div>div>input {
            border-radius: 8px !important;
        }

        /* Metric Cards for Progress */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            color: var(--primary-bg) !important;
        }

        /* Badges/Tags for complete sets */
        .completed-badge {
            background-color: var(--success);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }

        /* Progress Bar Override */
        .stProgress > div > div > div > div {
            background-color: var(--primary-bg) !important;
            border-radius: 10px !important;
        }

        /* Custom Header Styling */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            border-right: 1px solid var(--card-border) !important;
        }
        
        </style>
    """,
        unsafe_allow_html=True,
    )
