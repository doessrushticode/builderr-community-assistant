import os
import json
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Streamlit configuration MUST come before other Streamlit commands
st.set_page_config(
    page_title="Builderr Community Assistant",
    page_icon="🤖",
    layout="centered"
)