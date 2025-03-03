import streamlit as st

st.set_page_config(layout="wide")
st.title("Socio-Economic Data Visualization Tool")
st.divider()

st.markdown("""
    <style>
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #003366;
            margin-top: 20px;
        }
        .content {
            font-size: 18px;
            # color: #333;
        }
        .icon {
            font-size: 24px;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Vision Section
st.markdown('<h3 class="section-title">Our Vision</h3>', unsafe_allow_html=True)
st.markdown('<p class="content">We aim to harness socio-economic data to drive impactful decisions in key sectors like education, healthcare, and agriculture. Our goal is to provide stakeholders with actionable insights to foster economic growth and social progress.</p>', unsafe_allow_html=True)

# Problem Statement Section
st.markdown('<h3 class="section-title">Problem Statement</h3>', unsafe_allow_html=True)
st.markdown('<p class="content">Understanding socio-economic patterns across regions is challenging due to fragmented data sources. There is a lack of an integrated, interactive, and visually engaging tool to help policymakers, researchers, and analysts make data-driven decisions efficiently.</p>', unsafe_allow_html=True)

# Solution Section
st.markdown('<h3 class="section-title">Our Solution</h3>', unsafe_allow_html=True)
st.markdown("""
<p class="content">
Our platform is designed to bridge this gap by offering:
<ul>
    <li>Interactive Dashboards – Explore trends and patterns with dynamic charts and graphs.</li>
    <li>State-wise & National Comparisons – Compare key indicators across different regions over time.</li>
    <li>Real-time Data Integration – Access up-to-date socio-economic insights from reliable sources.</li>
    <li>AI-Powered Insights – Get automated trend analysis and predictive analytics for future planning.</li>
</ul>
</p>
""", unsafe_allow_html=True)

st.divider()

st.markdown("### 🔍 Explore the Data & Gain Insights")
st.write("Use the navigation sidebar to explore various features of our socio-economic data visualization tool.")
