# 🤝 CommuniSync: Community Needs & Volunteer Matcher

**CommuniSync** is an AI-powered platform designed to instantly translate messy, unstructured community field reports into structured, actionable insights, automatically matching local volunteers to the areas where they are needed most.

---

## 🚀 Hackathon Submission Requirements

### Problem Statement
Local social groups and NGOs collect a vast amount of critical information regarding community needs through paper surveys, handwritten notes, and unstructured field reports. Because this valuable data is often siloed and scattered across different formats and locations, it becomes incredibly difficult to identify the most urgent problems clearly. This fragmentation delays critical interventions and leaves willing volunteers sitting idle while local needs go unmet.

### Solution Overview
**CommuniSync** is a powerful, highly scalable Agentic AI system built to solve the local data fragmentation problem. Using the Google Gemini Context-Engine, our solution automatically reads and analyzes unstructured field reports in real-time. It extracts crucial structured data—such as specific needs, precise locations, urgency levels, and required skills. 

Once the data is structured, our smart matching engine instantly cross-references these urgent local needs against a centralized database of available volunteers, connecting the right people with the right skills to the specific tasks where they are needed the most.

### 🔗 Submission Links
*   **Prototype Link:** *[Insert Link to Live Streamlit MVP here]*
*   **Project Deck:** *[Insert Link to Presentation Deck here]*
*   **GitHub Repository:** [https://github.com/jaysid97/communisync](https://github.com/jaysid97/communisync)
*   **Demo Video:** *[Insert Link to Demo Video here]*

---

## 💻 Running the MVP Locally

Follow these steps to run the CommuniSync Context-Engine on your local machine:

1.  **Navigate to the project directory:**
    ```bash
    cd communisync
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    *   Duplicate `.env.template` and rename it to `.env`.
    *   Insert your valid Google Gemini API key: `GEMINI_API_KEY=your_actual_key_here`

4.  **Launch the Streamlit MVP:**
    ```bash
    python -m streamlit run app.py
    ```

### Example Input for Testing
Paste this into the application to see the Context-Engine in action:
> *"I was just at the Eastville community center. The roof is leaking really badly after last night's storm and they urgently need help fixing it before the weekend."*
