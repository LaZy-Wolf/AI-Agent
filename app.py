import streamlit as st
from workflow import graph
from models import WorkflowState

st.title("AI Agent Workflow")
query = st.text_input("Enter your query:", placeholder="e.g., Plan a trip")
if st.button("Run Workflow"):
    if query:
        with st.spinner("Processing..."):
            try:
                initial_state = WorkflowState(query=query)
                result = graph.invoke(initial_state, config={"recursion_limit": 10})
                # Coerce result to WorkflowState
                if isinstance(result, dict):
                    result = WorkflowState(**result)
                if not isinstance(result, WorkflowState):
                    st.error("Unexpected result type from workflow.")
                    st.stop()
                st.subheader("Tasks and Results")
                for task in result.tasks:
                    st.write(f"**Task {task.id}:** {task.description}")
                    st.write(f"Result: {task.result if task.result else 'No result yet'}")
                if result.final_output:
                    st.subheader("Final Output")
                    st.write(result.final_output)
                else:
                    st.warning("Workflow completed but no final output generated.")
            except Exception as e:
                st.error(f"Workflow error: {str(e)}")
    else:
        st.error("Please enter a query.")