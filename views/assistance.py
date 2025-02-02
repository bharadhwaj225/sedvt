import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data for demo
states = ["Andhra Pradesh", "Maharashtra", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Rajasthan", "Gujarat", "Odisha", "West Bengal", "Kerala"]

locations = {
    "Andhra Pradesh": [(15.9129, 79.7400)],
    "Maharashtra": [(19.7515, 75.7139)],
    "Uttar Pradesh": [(26.8467, 80.9462)],
    "Karnataka": [(15.3173, 75.7139)],
    "Tamil Nadu": [(11.1271, 78.6569)],
    "Rajasthan": [(27.0238, 74.2179)],
    "Gujarat": [(22.2587, 71.1924)],
    "Odisha": [(20.9517, 85.0985)],
    "West Bengal": [(22.9868, 87.8550)],
    "Kerala": [(10.8505, 76.2711)]
}

resource_data = pd.DataFrame({
    'State': states,
    'Population Density': [303, 365, 828, 319, 555, 200, 308, 269, 1029, 859],
    'Literacy Rate': [67, 82, 67, 75, 80, 66, 78, 73, 77, 94],
    'Average Income': [140000, 180000, 57000, 150000, 160000, 82000, 150000, 73000, 88000, 135000],
    'Urbanization Rate': [35, 45, 28, 40, 48, 24, 42, 29, 31, 47],
    'Unemployment Rate': [5, 4, 6, 5, 4, 5, 4, 6, 5, 3]
})

# Main App
st.set_page_config(layout="wide")

st.title("Poverty Combat Assistance App")
# st.markdown("<br>", unsafe_allow_html=True)  # Adding space between title and content
st.divider()

# Create two columns
col1, col2 = st.columns([1, 3])

# Column 1: Dropdown Menu for Navigation
with col1:
    st.markdown("### Menu")
    menu = ["Home", "Resource Allocation", "Aid Coordination", "Volunteer Opportunities", "Unemployment Solutions"]
    choice = st.selectbox("Select an option from the menu", menu)

# Column 2: Content display based on menu selection
with col2:
    if choice == "Home":
        st.subheader("Welcome to the Poverty Combat Assistance App")
        st.write("Choose an option from the dropdown menu to get started.")

    elif choice == "Resource Allocation":
        st.subheader("Resource Allocation Strategies")

        # State selection
        selected_state = st.selectbox("Select a state:", states)

        # Additional inputs
        urbanization_rate = st.slider("Urbanization Rate (%)", 10, 100, 50)
        unemployment_rate = st.slider("Unemployment Rate (%)", 1, 20, 5)

        # Displaying map for selected state
        map_data = pd.DataFrame({
            'lat': [locations[selected_state][0][0]],
            'lon': [locations[selected_state][0][1]]
        })
        st.map(map_data)

        # Displaying dataframe for selected state
        st.dataframe(resource_data[resource_data['State'] == selected_state])

        # Bar chart for literacy rate and average income
        fig, ax = plt.subplots()
        resource_data.set_index('State')[['Literacy Rate', 'Average Income']].plot(kind='bar', ax=ax)
        st.pyplot(fig)

    elif choice == "Aid Coordination":
        st.subheader("Connect with Relevant Aid Organizations")

        aid_data = pd.DataFrame({
            'Organization': ['NGO A', 'Government Program B', 'Charity C', 'NGO D', 'Charity E', 'Government Program F'],
            'Contact': ['contact@ngoa.org', 'contact@govb.org', 'contact@charityc.org', 'contact@ngod.org', 'contact@charitye.org', 'contact@govf.org'],
            'Programs Offered': [2, 3, 1, 2, 3, 2]
        })

        # Search bar
        search_term = st.text_input("Search for an organization:")

        if search_term:
            st.dataframe(aid_data[aid_data['Organization'].str.contains(search_term, case=False)])
        else:
            st.dataframe(aid_data)

        # Pie chart for programs offered
        fig, ax = plt.subplots()
        aid_data.set_index('Organization')['Programs Offered'].plot(kind='pie', ax=ax)
        st.pyplot(fig)

    elif choice == "Volunteer Opportunities":
        st.subheader("Volunteer to Combat Poverty")

        volunteer_data = pd.DataFrame({
            'Opportunity': ['Teach children', 'Distribute food', 'Provide medical assistance', 'Clean-up drives', 'Skill development workshops', 'Agricultural assistance'],
            'Location': ['Andhra Pradesh', 'Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Tamil Nadu', 'Rajasthan'],
            'Details': ['Teach subjects like Math, Science', 'Distribute food packets', 'Provide basic medical checkups', 'Organize community clean-up', 'Provide vocational training', 'Help with farming techniques']
        })

        opportunity_type = st.selectbox("Filter by type:", ["All", "Teaching", "Medical", "Food Distribution"])
        if opportunity_type == "Teaching":
            st.dataframe(volunteer_data[volunteer_data['Opportunity'].str.contains("Teach")])
        elif opportunity_type == "Medical":
            st.dataframe(volunteer_data[volunteer_data['Opportunity'].str.contains("medical", case=False)])
        elif opportunity_type == "Food Distribution":
            st.dataframe(volunteer_data[volunteer_data['Opportunity'].str.contains("food", case=False)])
        else:
            st.dataframe(volunteer_data)

        # Bar chart for opportunities by state
        fig, ax = plt.subplots()
        volunteer_data['Location'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    elif choice == "Unemployment Solutions":
        st.subheader("Solutions to Combat Unemployment")

        # Provide insights based on current unemployment rate
        selected_state = st.selectbox("Select a state:", states)
        unemployment_rate = resource_data[resource_data['State'] == selected_state]['Unemployment Rate'].values[0]

        st.write(f"The current unemployment rate in {selected_state} is {unemployment_rate}%")

        # Suggesting strategies to reduce unemployment
        if unemployment_rate > 5:
            st.write("Recommendations to combat unemployment:")
            st.write("- **Increase Access to Skill Development**: Provide free online courses and local workshops.")
            st.write("- **Encourage Entrepreneurship**: Support startups and micro-enterprises with loans and grants.")
            st.write("- **Promote Agricultural Projects**: Invest in rural areas to create sustainable livelihoods.")
            st.write("- **Public Works Programs**: Launch government-funded programs for infrastructure development.")
        else:
            st.write("Unemployment rate is under control, continue existing support strategies.")

        # Visualization of unemployment vs literacy rate
        fig, ax = plt.subplots()
        x = resource_data['Literacy Rate']
        y = resource_data['Unemployment Rate']
        ax.scatter(x, y)
        ax.set_xlabel("Literacy Rate")
        ax.set_ylabel("Unemployment Rate")
        st.pyplot(fig)
