import requests
import time
import os

import gradio as gr

ML_ENDPOINT_URL = os.environ.get("ML_ENDPOINT_URL", "http://0.0.0.0:3000/rewrite")


def make_request(query):
    start_time = time.time()

    try:
        # Replace with your actual API endpoint
        if "rewrite: " not in query:
            query = f"rewrite: {query}"
        response = requests.post(ML_ENDPOINT_URL, json={"inputs": query})
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        result = f"Error: {str(e)}"

    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    return result, f"Response Time: {processing_time} seconds"


# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Query Interface")

    with gr.Row():
        query_input = gr.Textbox(
            label="Enter your query", placeholder="Type your query here...", lines=3
        )

    with gr.Row():
        submit_btn = gr.Button("Submit")

    with gr.Row():
        response_output = gr.Textbox(label="Response", lines=5, interactive=False)
        time_label = gr.Label(label="Processing Time")

    submit_btn.click(
        fn=make_request, inputs=[query_input], outputs=[response_output, time_label]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0")
