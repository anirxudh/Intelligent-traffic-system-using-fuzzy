import streamlit as st
from typing import List, Tuple

# Constants for fuzzy sets
WAITING_TRAFFIC = ['minimal', 'light', 'average', 'heavy', 'standstill']
INCOMING_TRAFFIC = ['minimal', 'light', 'average', 'heavy', 'excess']
DURATION = ['short', 'medium', 'long']

# Traffic light timing constants (in seconds)
LIGHT_TIMING = {
    'short': 50,
    'medium': 90,
    'long': 125,
    'default_min': 45,
    'default_max': 150
}

# Fuzzy rules for traffic control
FUZZY_RULES = [
    [['minimal', 'minimal'], 'short'],
    [['minimal', 'light'], 'short'],
    [['minimal', 'average'], 'medium'],
    [['minimal', 'heavy'], 'long'],
    [['minimal', 'excess'], 'long'],
    [['light', 'minimal'], 'short'],
    [['light', 'light'], 'short'],
    [['light', 'average'], 'medium'],
    [['light', 'heavy'], 'medium'],
    [['light', 'excess'], 'long'],
    [['average', 'minimal'], 'short'],
    [['average', 'light'], 'medium'],
    [['average', 'average'], 'medium'],
    [['average', 'heavy'], 'long'],
    [['average', 'excess'], 'long'],
    [['heavy', 'minimal'], 'medium'],
    [['heavy', 'light'], 'medium'],
    [['heavy', 'average'], 'long'],
    [['heavy', 'heavy'], 'long'],
    [['heavy', 'excess'], 'long'],
    [['standstill', 'minimal'], 'medium'],
    [['standstill', 'light'], 'long'],
    [['standstill', 'average'], 'long'],
    [['standstill', 'heavy'], 'long'],
    [['standstill', 'excess'], 'long']
]

def calculate_traffic_state(cars: int, is_waiting: bool) -> List[Tuple[str, float]]:
    # (Keep the existing function implementation unchanged)
    traffic_set = WAITING_TRAFFIC if is_waiting else INCOMING_TRAFFIC

    states = []
    if 0 <= cars <= 15:
        states.append(traffic_set[0])
    if 10 <= cars <= 25:
        states.append(traffic_set[1])
    if 20 <= cars <= 35:
        states.append(traffic_set[2])
    if 30 <= cars <= 45:
        states.append(traffic_set[3])
    if cars >= 40:
        states.append(traffic_set[4])

    if len(states) <= 1:
        return [(states[0], 1.0)]

    if cars <= 15:
        return [
            (states[0], -(cars - 15) / 5),
            (states[1], -(cars - 25) / 5)
        ]
    elif cars <= 25:
        return [
            (states[0], -(cars - 25) / 5),
            (states[1], (cars - 20) / 5)
        ]
    elif cars <= 35:
        return [
            (states[0], -(cars - 35) / 5),
            (states[1], (cars - 30) / 5)
        ]
    else:
        return [
            (states[0], -(cars - 45) / 5),
            (states[1], (cars - 40) / 5)
        ]

def apply_fuzzy_rules(waiting: List[Tuple[str, float]],
                     incoming: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    # (Keep the existing function implementation unchanged)
    durations = []
    for w_state, w_value in waiting:
        for i_state, i_value in incoming:
            for rule in FUZZY_RULES:
                if rule[0][0] == w_state and rule[0][1] == i_state:
                    durations.append((rule[1], min(w_value, i_value)))
    return durations

def calculate_duration(duration_states: List[Tuple[str, float]]) -> int:
    # (Keep the existing function implementation unchanged)
    if not duration_states:
        return LIGHT_TIMING['default_min']

    total_weight = sum(weight for _, weight in duration_states)
    if total_weight == 0:
        return LIGHT_TIMING['default_min']

    weighted_sum = sum(
        LIGHT_TIMING[state] * weight
        for state, weight in duration_states
    )

    duration = weighted_sum / total_weight

    return min(max(int(duration), LIGHT_TIMING['default_min']),
              LIGHT_TIMING['default_max'])

def process_traffic(waiting_cars: int, incoming_cars: int) -> int:
    # (Keep the existing function implementation unchanged)
    waiting_state = calculate_traffic_state(waiting_cars, True)
    incoming_state = calculate_traffic_state(incoming_cars, False)

    duration_states = apply_fuzzy_rules(waiting_state, incoming_state)
    return calculate_duration(duration_states)

# Streamlit UI
st.title("Intelligent Traffic Light System")

col1, col2 = st.columns(2)
with col1:
    waiting_cars = st.number_input("Cars waiting at light", 
                                  min_value=0, 
                                  value=10,
                                  step=1)
with col2:
    incoming_cars = st.number_input("Cars approaching intersection", 
                                   min_value=0, 
                                   value=33,
                                   step=1)

if st.button("Calculate Green Light Duration"):
    st.markdown("---")
    st.subheader("Current Traffic Situation")
    st.markdown(f"- Cars waiting at light: `{waiting_cars}`")
    st.markdown(f"- Cars approaching intersection: `{incoming_cars}`")
    
    waiting_state = calculate_traffic_state(waiting_cars, True)
    incoming_state = calculate_traffic_state(incoming_cars, False)
    
    st.markdown("---")
    st.subheader("Analysis Results")
    st.markdown(f"- Waiting traffic state: `{waiting_state}`")
    st.markdown(f"- Incoming traffic state: `{incoming_state}`")
    
    duration = process_traffic(waiting_cars, incoming_cars)
    
    st.markdown("---")
    st.subheader("Recommended Action")
    st.success(f"→ Set traffic light to GREEN for {duration} seconds")