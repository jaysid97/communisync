import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from logic import analyze_community_report, generate_dispatch_message
import os
from PIL import Image

# Load environment variables
load_dotenv()

st.set_page_config(page_title="CommuniSync MVP", page_icon="🤝", layout="wide")

st.title("🤝 CommuniSync: Community Needs & Volunteer Matcher")
st.markdown("Transform scattered, unstructured field reports into actionable volunteer matching using Agentic AI.")

# Check for API Key
if not os.environ.get("GEMINI_API_KEY"):
    st.error("⚠️ GEMINI_API_KEY is missing. Please add it to your .env file to run the AI engine.")

# Mock Volunteer Database
volunteers = pd.DataFrame([
    {"Name": "Dr. Sarah Lee", "Skills": "Medical, First Aid, Triage", "Location": "Downtown", "Status": "Available"},
    {"Name": "Mark Johnson", "Skills": "Logistics, Driving, Heavy Lifting", "Location": "Northside", "Status": "Available"},
    {"Name": "Elena Rodriguez", "Skills": "Food Prep, Translation, Caregiving", "Location": "Eastville", "Status": "In Field"},
    {"Name": "James Chen", "Skills": "Construction, Carpentry, Repair", "Location": "West End", "Status": "Available"}
])

# Initialize session state for mock database to simulate dashboard analytics
if 'reports_db' not in st.session_state:
    st.session_state['reports_db'] = []

tab1, tab2 = st.tabs(["📥 Intake & Matching", "🗺️ Command Center Dashboard"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Submit Field Report")
        
        input_method = st.radio("Input Method:", ["Text / Notes", "Upload Paper Survey / Image"])
        
        report_input = None
        if input_method == "Text / Notes":
            report_text = st.text_area(
                "Paste unstructured notes or survey data here:",
                height=150,
                placeholder="e.g. Talked to folks at the Eastville community center. The roof is leaking badly after the storm..."
            )
            if report_text: report_input = report_text
        else:
            uploaded_file = st.file_uploader("Upload a handwritten note or photo", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Survey", use_column_width=True)
                report_input = image
        
        if st.button("Process with Context-Engine", type="primary", use_container_width=True):
            if not report_input:
                st.warning("Please enter text or upload an image to process.")
            else:
                with st.spinner("Gemini is reading and structuring the report..."):
                    result = analyze_community_report(report_input)
                    
                    if "error" in result:
                        st.error(f"Failed to process: {result['error']}")
                    else:
                        st.success("✅ Report Structured Successfully!")
                        st.session_state['last_result'] = result
                        # Add to mock DB for the dashboard
                        st.session_state['reports_db'].append(result)

    with col2:
        st.subheader("🎯 Actionable Insights & Dispatch")
        
        if 'last_result' in st.session_state:
            res = st.session_state['last_result']
            
            # Display extracted structured data elegantly
            st.markdown("### 📊 Extracted Data")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Urgency", res.get('urgency', 'Unknown'))
            metric_col2.metric("Category", res.get('primary_need', 'Unknown'))
            metric_col3.metric("Location", res.get('location', 'Unknown'))
            
            st.info(f"**Summary:** {res.get('summary', 'No summary provided.')}")
            
            skills = res.get('required_volunteer_skills', [])
            st.write(f"**Skills Required:** {', '.join(skills)}")
            
            st.divider()
            st.markdown("### 🧑‍🤝‍🧑 AI Recommended Volunteers")
            
            # Basic matching logic for the MVP
            matches = []
            for _, vol in volunteers.iterrows():
                vol_skills = vol['Skills'].lower()
                if any(skill.lower() in vol_skills for skill in skills) or (res.get('urgency') == 'High' and vol['Status'] == 'Available'):
                     matches.append(vol)
                     
            if matches:
                st.success(f"Found {len(matches)} suitable volunteers for this task!")
                st.dataframe(pd.DataFrame(matches), use_container_width=True)
                
                # Auto-dispatch feature
                st.markdown("#### ⚡ Automated Dispatch")
                top_match = matches[0]['Name']
                if st.button(f"Generate & Send Dispatch to {top_match}"):
                    with st.spinner("Agentic AI drafting SMS..."):
                        sms_draft = generate_dispatch_message(top_match, res.get('summary'), res.get('location'))
                        st.info(f"📱 **SMS Sent to {top_match}:**\n\n{sms_draft}")
                        st.toast(f"Dispatch alert sent to {top_match}!", icon="🚀")
            else:
                st.warning("No exact skill matches found. Showing all available volunteers:")
                st.dataframe(volunteers[volunteers['Status'] == 'Available'], use_container_width=True)
        else:
            st.info("Submit a report on the left to see the AI automatically extract data and recommend volunteers.")

with tab2:
    st.subheader("🗺️ Live Community Needs Dashboard")
    
    if not st.session_state['reports_db']:
        st.write("No reports processed yet. Process some reports to populate the dashboard!")
    else:
        db_df = pd.DataFrame(st.session_state['reports_db'])
        
        col_dash1, col_dash2 = st.columns(2)
        
        with col_dash1:
            st.markdown("#### Needs by Category")
            if 'primary_need' in db_df.columns:
                category_counts = db_df['primary_need'].value_counts()
                st.bar_chart(category_counts)
            
        with col_dash2:
            st.markdown("#### Urgency Levels")
            if 'urgency' in db_df.columns:
                urgency_counts = db_df['urgency'].value_counts()
                st.bar_chart(urgency_counts)
            
        st.markdown("#### Incident Map")
        map_data = []
        for index, row in db_df.iterrows():
            lat = row.get('latitude')
            lon = row.get('longitude')
            try:
                lat = float(lat)
                lon = float(lon)
            except:
                lat, lon = 0.0, 0.0
            
            if lat == 0.0 and lon == 0.0:
                # Fallback mock coordinates if missing or unparseable
                lat = 40.7128 + (index * 0.05)
                lon = -74.0060 + (index * 0.05)
            map_data.append({"lat": lat, "lon": lon})
            
        if map_data:
            st.map(pd.DataFrame(map_data))
