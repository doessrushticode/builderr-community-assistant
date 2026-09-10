import os
import json
import pandas as pd
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="Builderr Community Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("Builderr Community Assistant")
st.markdown(
    "**Draft-only tool.** Nothing is published automatically. Human review is required."
)

gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key) if gemini_key else None

@st.cache_data
def load_posts():
    return pd.read_csv("sample_posts.csv")

df = load_posts()

SYSTEM_INSTRUCTION = """
You are Builderr's community-engagement drafting assistant.

Builderr is an open platform for AI-agent challenges. A person or company posts a real, measurable automation problem. Builderr helps turn that into a well-defined challenge with clear evaluation criteria. Builders submit working solutions; solutions are scored; only solutions that meet the agreed bar can win.

Decide whether Builderr should respond to the post.

Return JSON with exactly these fields:
{
  "should_respond": "Yes" or "No",
  "confidence": integer from 0 to 100,
  "why": "A concise explanation directly tied to the post.",
  "draft_response": "A useful, natural response if Yes. Empty string if No.",
  "tags": ["tag1", "tag2"]
}

Rules:
- Respond only when there is a genuine opportunity for Builderr to add value.
- If the post criticizes AI slop/bots/promotion, usually say No.
- Generic showcase threads should usually be No.
- Good fits: real automation problems, practical AI project requests, growth challenges, builder searches, relevant hiring threads.
- Drafts must be helpful even if the author never uses Builderr.
- No spammy or salesy language.
"""

def analyse_post(row):
    if client is None:
        return {"post_id": int(row["post_id"]), "error": "Missing GEMINI_API_KEY"}

    user_prompt = f"""
Community: {row['community']}
Context: {row['community_context']}
Summary: {row['post_summary']}
URL: {row['source_url']}

Return JSON with exactly:
{{
  "should_respond": "Yes" or "No",
  "confidence": 0-100,
  "why": "short reason",
  "draft_response": "draft if Yes else empty string",
  "tags": ["tag1","tag2"]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        result = json.loads(response.text.strip())
        result["post_id"] = int(row["post_id"])
        return result
    except Exception as e:
        return {"post_id": int(row["post_id"]), "error": str(e)}

st.subheader("Analyse a community post")
selected_id = st.selectbox("Select a post", options=df["post_id"].tolist(), format_func=lambda x: f"Post {x}")
row = df[df["post_id"] == selected_id].iloc[0]

st.markdown(f"**Community:** {row['community']}")
st.markdown(f"**Context:** {row['community_context']}")
st.markdown(f"**Summary:** {row['post_summary']}")
st.markdown(f"**Source:** [Open original post]({row['source_url']})")

if st.button("Analyse this post", type="primary"):
    if client is None:
        st.error("Gemini API key not found. Check your .env file.")
    else:
        with st.spinner("Analysing..."):
            result = analyse_post(row)
        if "error" in result and len(result) == 2:
            st.error(f"Error: {result['error']}")
        else:
            st.write(f"**Should respond:** {result.get('should_respond')}")
            st.write(f"**Confidence:** {result.get('confidence')}%")
            st.write(f"**Why:** {result.get('why')}")
            if result.get("should_respond") == "Yes":
                st.info(result.get("draft_response", ""))

st.divider()
st.subheader("Batch analysis")

if st.button("Analyse all eight posts"):
    if client is None:
        st.error("Gemini API key not found.")
    else:
        results = []
        progress = st.progress(0)
        status = st.empty()

        for index, (_, r) in enumerate(df.iterrows(), start=1):
            status.write(f"Analysing post {index} of {len(df)}...")
            results.append(analyse_post(r))
            progress.progress(index / len(df))

            # Gemini free tier allows limited requests per minute.
            # Wait between calls so the batch does not exceed the limit.
            if index < len(df):
                time.sleep(13)

        status.success("All posts analysed.")

        results_df = pd.DataFrame(results)

        # Keep exactly the columns requested in the assignment.
        output_df = results_df[
            ["post_id", "should_respond", "why", "draft_response"]
        ]

        st.dataframe(output_df, use_container_width=True)

        csv_data = output_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download example_output.csv",
            data=csv_data,
            file_name="example_output.csv",
            mime="text/csv",
        )

        # Save the results in the GitHub project as well.
        results_df.to_csv("results/example_output.csv", index=False)

        st.success(
            "Results saved in results/example_output.csv. "
            "You can also download the file above."
        )