import streamlit as st
import time

st.set_page_config(page_title="AI Traffic Signal Control", layout="wide")
st.title("🚦 AI-Based Intelligent Traffic Signal Control System")
st.markdown("Smart traffic management using AI logic, vehicle density, and emergency detection.")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("📊 Real-Time Traffic Input")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🛣️ Road A")
    road_a = st.number_input("Number of Vehicles", min_value=0, step=1, key="road_a")
    emergency_a = st.checkbox("🚑 Emergency Vehicle", key="emergency_a")

with col2:
    st.subheader("🛣️ Road B")
    road_b = st.number_input("Number of Vehicles", min_value=0, step=1, key="road_b")
    emergency_b = st.checkbox("🚑 Emergency Vehicle", key="emergency_b")

with col3:
    st.subheader("🛣️ Road C")
    road_c = st.number_input("Number of Vehicles", min_value=0, step=1, key="road_c")
    emergency_c = st.checkbox("🚑 Emergency Vehicle", key="emergency_c")

# -----------------------------
# PROCESSING FUNCTIONS
# -----------------------------

def get_signal_duration(vehicle_count):
    """Determine signal duration based on vehicle count"""
    if vehicle_count > 120:
        return 60, "HIGH"
    elif 60 <= vehicle_count <= 120:
        return 40, "MEDIUM"
    else:
        return 20, "LOW"

def get_alert_message(congestion_level, road_name, signal_duration):
    """Generate alert message based on congestion level"""
    if congestion_level == "HIGH":
        alert_type = "⚠️ WARNING"
        alert_message = f"Heavy traffic detected on {road_name}. Expect delays."
        suggested_action = "Consider alternate routes if possible."
    elif congestion_level == "MEDIUM":
        alert_type = "⚠️ CAUTION"
        alert_message = f"Moderate traffic flow on {road_name}."
        suggested_action = "Drive carefully and maintain safe distance."
    else:
        alert_type = "✅ INFO"
        alert_message = f"Traffic is smooth on {road_name}."
        suggested_action = "Normal driving conditions."
    
    return alert_type, alert_message, suggested_action

# -----------------------------
# ANALYZE BUTTON
# -----------------------------

if st.button("🚥 Analyze Traffic & Control Signals", type="primary"):
    
    traffic_data = {
        "Road A": {"vehicles": road_a, "emergency": emergency_a},
        "Road B": {"vehicles": road_b, "emergency": emergency_b},
        "Road C": {"vehicles": road_c, "emergency": emergency_c}
    }
    
    # Check for emergency vehicles
    emergency_roads = [road for road, data in traffic_data.items() if data["emergency"]]
    
    st.markdown("---")
    
    # -----------------------------
    # EMERGENCY MODE
    # -----------------------------
    if emergency_roads:
        st.error("🚨 EMERGENCY MODE ACTIVATED")
        
        # Emergency vehicle gets priority
        priority_road = emergency_roads[0]  # First emergency vehicle detected
        
        st.warning(f"### 🚑 Emergency Vehicle Detected on {priority_road}")
        st.write(f"**Action:** Immediate green signal given to {priority_road}")
        st.write(f"**Duration:** Until emergency vehicle passes (estimated 90+ seconds)")
        
        st.markdown("### 🚦 Signal Status for All Roads")
        
        signal_col1, signal_col2, signal_col3 = st.columns(3)
        
        for idx, (road, data) in enumerate(traffic_data.items()):
            with [signal_col1, signal_col2, signal_col3][idx]:
                if road == priority_road:
                    st.success(f"**{road}**")
                    st.markdown("🟢 **GREEN** - 90+ seconds")
                    st.markdown("🟡 Yellow - 0 seconds")
                    st.markdown("🔴 Red - 0 seconds")
                    st.metric("Vehicles Waiting", data["vehicles"])
                else:
                    st.error(f"**{road}**")
                    st.markdown("🟢 Green - 0 seconds")
                    st.markdown("🟡 Yellow - 0 seconds")
                    st.markdown("🔴 **RED** - Until emergency clears")
                    st.metric("Vehicles Waiting", data["vehicles"])
        
        st.info("💡 **Emergency Protocol:** All other signals stopped. Normal operation will resume after emergency vehicle passes.")
    
    # -----------------------------
    # NORMAL MODE
    # -----------------------------
    else:
        st.success("✅ NORMAL TRAFFIC CONTROL MODE")
        
        # Determine priority based on vehicle count
        selected_road = max(traffic_data, key=lambda x: traffic_data[x]["vehicles"])
        selected_vehicles = traffic_data[selected_road]["vehicles"]
        
        # Get signal duration and congestion level
        green_duration, congestion_level = get_signal_duration(selected_vehicles)
        
        # Calculate yellow time (standard 3-5 seconds)
        yellow_duration = 5
        
        # Calculate red time for non-priority roads
        # Red time = green time of priority road + yellow time + buffer
        red_duration = green_duration + yellow_duration
        
        st.markdown("### 🎯 Traffic Signal Control Decision")
        
        decision_col1, decision_col2 = st.columns(2)
        
        with decision_col1:
            st.metric("Selected Road (Green Signal)", selected_road)
            st.metric("Vehicle Count", selected_vehicles)
            st.metric("Congestion Level", congestion_level)
        
        with decision_col2:
            st.metric("Green Signal Duration", f"{green_duration} seconds")
            st.metric("Yellow Signal Duration", f"{yellow_duration} seconds")
            st.metric("Emergency Status", "None")
        
        # Generate alert
        alert_type, alert_message, suggested_action = get_alert_message(
            congestion_level, selected_road, green_duration
        )
        
        st.markdown("### 📢 Alert & Notification")
        if congestion_level == "HIGH":
            st.warning(f"**{alert_type}**")
        elif congestion_level == "MEDIUM":
            st.info(f"**{alert_type}**")
        else:
            st.success(f"**{alert_type}**")
        
        st.write(f"**Message:** {alert_message}")
        st.write(f"**Suggested Action:** {suggested_action}")
        
        st.markdown("---")
        st.markdown("### 🚦 Signal Status for All Roads")
        
        signal_col1, signal_col2, signal_col3 = st.columns(3)
        
        for idx, (road, data) in enumerate(traffic_data.items()):
            with [signal_col1, signal_col2, signal_col3][idx]:
                if road == selected_road:
                    # Priority road - GREEN
                    st.success(f"**{road} (Priority)**")
                    st.markdown(f"🟢 **GREEN** - {green_duration} seconds")
                    st.markdown(f"🟡 Yellow - {yellow_duration} seconds")
                    st.markdown(f"🔴 Red - 0 seconds")
                    st.metric("Vehicles", data["vehicles"])
                    st.progress(1.0)
                else:
                    # Other roads - RED
                    st.error(f"**{road}**")
                    st.markdown("🟢 Green - 0 seconds")
                    st.markdown(f"🟡 Yellow - {yellow_duration} seconds")
                    st.markdown(f"🔴 **RED** - {red_duration} seconds")
                    st.metric("Vehicles Waiting", data["vehicles"])
                    st.progress(0.0)
        
        # Traffic optimization explanation
        st.markdown("### 🧠 AI Decision Explanation")
        st.info(f"""
        **Reasoning:**
        - {selected_road} has the highest vehicle density ({selected_vehicles} vehicles)
        - Congestion level: **{congestion_level}**
        - Allocated **{green_duration} seconds** green time to optimize traffic flow
        - Other roads will wait for **{red_duration} seconds** to ensure smooth flow
        - This prioritization minimizes overall waiting time and prevents gridlock
        """)

# -----------------------------
# SYSTEM INFORMATION
# -----------------------------
st.markdown("---")
st.markdown("### 📋 System Rules")

with st.expander("View Traffic Signal Control Rules"):
    st.markdown("""
    **Vehicle-Based Signal Timing:**
    - 🔴 HIGH traffic (>120 vehicles) → 60 seconds green
    - 🟡 MEDIUM traffic (60-120 vehicles) → 40 seconds green
    - 🟢 LOW traffic (<60 vehicles) → 20 seconds green
    
    **Emergency Vehicle Priority:**
    - ✅ Immediate green signal for road with emergency vehicle
    - ✅ Signal remains green until emergency vehicle passes
    - ✅ All other roads must wait (red signal)
    
    **Traffic Optimization:**
    - Roads with higher vehicle count get priority
    - Smooth traffic flow ensured
    - Dynamic adjustment based on real-time data
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("🤖 AI-Based Intelligent Traffic Signal Control System | Powered by Advanced Traffic Management Logic")