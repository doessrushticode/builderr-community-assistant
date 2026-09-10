# Builderr Community Assistant

A draft-only assistant that reviews community posts and helps Builderr decide:

1. Should Builderr respond?
2. Why?
3. What should the response say?

The tool never publishes content automatically. Every suggested response requires human review before use.

## What it does

- Loads eight sample community posts from `sample_posts.csv`
- Lets a reviewer analyse one post at a time
- Generates a recommendation: `Yes` or `No`
- Explains the reasoning behind the recommendation
- Produces a tailored draft only when responding would add genuine value
- Supports batch analysis of all eight posts
- Exports the required results as `example_output.csv`

## Decision framework

The assistant recommends a response only when Builderr has a relevant, constructive reason to engage.

It prioritises posts involving:

- Real automation or AI-agent problems
- Requests for practical AI project ideas based on real use cases
- Founders facing measurable growth, activation, or community challenges
- Requests for builders or developers where a clear, testable brief would help
- Relevant hiring or cofounder opportunities

It avoids engagement when a response would be irrelevant, promotional, spam-like, or inappropriate for the community. For example, it does not respond to posts that criticise automated promotional comments or to broad showcase threads without a specific problem.

## Tech stack

- Python
- Streamlit
- Google Gemini API
- Pandas

## Run locally

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/builderr-community-assistant.git](https://github.com/YOUR_GITHUB_USERNAME/builderr-community-assistant.git)
cd builderr-community-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a file named `.env` in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit this file. It is already excluded through `.gitignore`.

### 4. Run the application

```bash
streamlit run app.py
```

Open the local address shown in the terminal.

## Results

The final reviewed outputs for all eight sample posts are available here:

```text
results/example_output.csv
```

The results file uses the required schema:

```text
post_id, should_respond, why, draft_response
```

## Safety and limitations

- This prototype generates drafts only; it has no capability to publish or interact with external community platforms.
- Human review is required before using any suggested response.
- LLM output can vary and may be overly conservative or insufficiently aware of community nuance.
- The submitted CSV is a reviewed final output, because community engagement is brand-sensitive and should not rely on an unreviewed automated decision.

## Future improvements

- Add structured-output validation with a JSON schema
- Add rate-limit retries and exponential backoff for batch processing
- Allow reviewers to edit, approve, reject, and save drafts in the interface
- Add community-specific policies and tone controls
- Evaluate recommendations against historical engagement outcomes
