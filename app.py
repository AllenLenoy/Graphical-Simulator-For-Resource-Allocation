import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize session state to store graph data  
if 'processes' not in st.session_state:
    st.session_state.processes = []
if 'resources' not in st.session_state:
    st.session_state.resources = []     ##created code for intiliazing resources
if 'request_edges' not in st.session_state:
    st.session_state.request_edges = []
if 'allocation_edges' not in st.session_state:
    st.session_state.allocation_edges = []

# Sidebar controls for interactivity
st.sidebar.header("Add Process")
process_name = st.sidebar.text_input("Process Name (e.g., P1)")
if st.sidebar.button("Add Process"):
    if process_name in st.session_state.processes:
        st.sidebar.error("Process already exists")
    elif process_name in st.session_state.resources:
        st.sidebar.error("Name conflicts with a resource")
    elif process_name:
        st.session_state.processes.append(process_name)

st.sidebar.header("Add Resource")
resource_name = st.sidebar.text_input("Resource Name (e.g., R1)")
if st.sidebar.button("Add Resource"):
    if resource_name in st.session_state.resources:
        st.sidebar.error("Resource already exists")
    elif resource_name in st.session_state.processes:
        st.sidebar.error("Name conflicts with a process")
    elif resource_name:
        st.session_state.resources.append(resource_name)

st.sidebar.header("Add Request Edge")
if st.session_state.processes and st.session_state.resources:
    process_select = st.sidebar.selectbox("Select Process", st.session_state.processes)
    resource_select = st.sidebar.selectbox("Select Resource", st.session_state.resources)
    if st.sidebar.button("Add Request Edge"):
        edge = (process_select, resource_select)
        if edge in st.session_state.request_edges:
            st.sidebar.error("Edge already exists")
        else:
            st.session_state.request_edges.append(edge)
else:
    st.sidebar.write("Add processes and resources first")

st.sidebar.header("Add Allocation Edge")
if st.session_state.resources and st.session_state.processes:
    resource_select_alloc = st.sidebar.selectbox("Select Resource", st.session_state.resources, key="alloc_resource")
    process_select_alloc = st.sidebar.selectbox("Select Process", st.session_state.processes, key="alloc_process")
    if st.sidebar.button("Add Allocation Edge"):
        edge = (resource_select_alloc, process_select_alloc)
        if edge in st.session_state.allocation_edges:
            st.sidebar.error("Edge already exists")
        else:
            st.session_state.allocation_edges.append(edge)
else:
    st.sidebar.write("Add resources and processes first")

st.sidebar.header("Remove Request Edges")
for edge in st.session_state.request_edges[:]:  # Use a copy to avoid modification issues
    col1, col2 = st.sidebar.columns([3, 1])
    col1.write(f"{edge[0]} → {edge[1]}")
    if col2.button("Remove", key=f"remove_request_{edge[0]}_{edge[1]}"):
        st.session_state.request_edges.remove(edge)

st.sidebar.header("Remove Allocation Edges")
for edge in st.session_state.allocation_edges[:]:  # Use a copy to avoid modification issues
    col1, col2 = st.sidebar.columns([3, 1])
    col1.write(f"{edge[0]} → {edge[1]}")
    if col2.button("Remove", key=f"remove_alloc_{edge[0]}_{edge[1]}"):
        st.session_state.allocation_edges.remove(edge)

st.sidebar.header("Remove Process")
if st.session_state.processes:
    process_to_remove = st.sidebar.selectbox("Select Process to Remove", st.session_state.processes)
    if st.sidebar.button("Remove Process"):
        st.session_state.processes.remove(process_to_remove)
        st.session_state.request_edges = [e for e in st.session_state.request_edges if e[0] != process_to_remove]
        st.session_state.allocation_edges = [e for e in st.session_state.allocation_edges if e[1] != process_to_remove]

st.sidebar.header("Remove Resource")
if st.session_state.resources:
    resource_to_remove = st.sidebar.selectbox("Select Resource to Remove", st.session_state.resources)
    if st.sidebar.button("Remove Resource"):
        st.session_state.resources.remove(resource_to_remove)
        st.session_state.request_edges = [e for e in st.session_state.request_edges if e[1] != resource_to_remove]
        st.session_state.allocation_edges = [e for e in st.session_state.allocation_edges if e[0] != resource_to_remove]

# Main area: Display the graph and check for deadlock
st.title("Resource Allocation Graph Simulator")
st.write("Blue circles = Processes, Red squares = Resources")

# Create the directed graph
G = nx.DiGraph()
for p in st.session_state.processes:
    G.add_node(p, type='process')
for r in st.session_state.resources:
    G.add_node(r, type='resource')
for edge in st.session_state.request_edges:
    G.add_edge(edge[0], edge[1])
for edge in st.session_state.allocation_edges:
    G.add_edge(edge[0], edge[1])

# Visualize the graph
if G.number_of_nodes() > 0:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist=st.session_state.processes, node_color='blue', node_shape='o', ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=st.session_state.resources, node_color='red', node_shape='s', ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    plt.title("Resource Allocation Graph")
    st.pyplot(fig)
else:
    st.write("Add processes and resources to see the graph.")

# Check for deadlock
if st.button("Check for Deadlock"):
    if G.number_of_nodes() == 0:
        st.write("Graph is empty.")
    elif not nx.is_directed_acyclic_graph(G):
        st.write("**Deadlock detected!** A cycle exists in the graph.")
    else:
        st.write("No deadlock. The graph is acyclic.")