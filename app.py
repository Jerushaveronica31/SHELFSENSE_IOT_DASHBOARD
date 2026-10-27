import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# பக்கத்தின் அமைப்பு (Wide Mode)
st.set_page_config(page_title="ShelfSense Pro Analytics", page_icon="📦", layout="wide")

# கஸ்டம் CSS ஸ்டைலிங்
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    </style>
""", unsafe_allow_html=True)

# ஹெட்டர் பகுதி
st.title("📦 ShelfSense - Advanced IoT Analytics Dashboard")
st.markdown("### Real-time Monitoring with Bar, Line & Pie Charts")
st.markdown("---")

# ஃபைர்பேஸ் URL
firebase_url = "https://shelfsense-d9cde-default-rtdb.firebaseio.com/shelf_logs.json"

# சைட் பார் கண்ட்ரோல்ஸ்
st.sidebar.header("⚙️ Control Panel")
refresh_btn = st.sidebar.button("🔄 Refresh Dashboard")

# டேட்டாவை பெறுதல்
response = requests.get(firebase_url)

if response.status_code == 200:
    data = response.json()
    
    if data:
        # டேட்டாவை DataFrame-ஆக மாற்றுதல்
        df = pd.DataFrame(list(data.values()))
        
        # 1. டாப் மெட்ரிக்ஸ் (4 பிரிவுகள்)
        total_logs = len(df)
        unique_products = df['product_id'].nunique() if 'product_id' in df.columns else 0
        sensors_used = df['sensor'].nunique() if 'sensor' in df.columns else 0
        latest_status = df['action'].iloc[-1] if 'action' in df.columns else "Active"
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Total Activity Logs", total_logs)
        col2.metric("🏷️ Unique Products", unique_products)
        col3.metric("🔌 Active Sensors", sensors_used)
        col4.metric("⚡ Current Status", latest_status)
        
        st.markdown("---")
        
        # 2. பார் சார்ட் மற்றும் லைன் சார்ட் பகுதி
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("📊 Product Activity (Bar Chart)")
            if 'product_id' in df.columns:
                product_counts = df['product_id'].value_counts()
                st.bar_chart(product_counts)
            else:
                st.info("No product data for bar chart.")
                
        with chart_col2:
            st.subheader("📈 Activity Trends (Line Chart)")
            if len(df) > 0:
                st.line_chart(df.index)
            else:
                st.info("No data for line chart.")
                
        st.markdown("---")

        # 3. பை சார்ட் (Pie Chart) பகுதி
        st.subheader("🥧 Product Distribution (Pie Chart)")
        if 'product_id' in df.columns:
            fig = px.pie(df, names='product_id', title='Share of Products Picked', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data for pie chart.")
            
        st.markdown("---")

        # 4. பிரதான டேபிள் பகுதி
        st.subheader("📋 Detailed Shelf Logs Table")
        st.dataframe(df, use_container_width=True, height=350)
        
        # 5. டவுன்லோட் ஆப்ஷன்
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name='shelfsense_detailed_logs.csv',
            mime='text/csv'
        )
            
    else:
        st.warning("No records found in Firebase yet! Trigger your Wokwi sensor.")
else:
    st.error("Failed to connect with Firebase database.")