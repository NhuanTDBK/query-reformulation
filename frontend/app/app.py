import requests
import time
import os

import gradio as gr

ML_ENDPOINT_URL = os.environ.get("ML_ENDPOINT_URL", "http://50.18.255.74:8040/rewrite")
client_session = requests.Session()
client_session.keep_alive = 5

# Example queries to help users understand the app
EXAMPLE_QUERIES = [
    [
        "In what year was the winner of the 44th edition of the Miss World competition born?"
    ],
    ["Who lived longer, Nikola Tesla or Milutin Milankovic?"],
    [
        "Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?"
    ],
    ["Create a table for top noise cancelling headphones that are not expensive"],
    ["what are some ways to do fast query reformulation?"],
]


def make_request(query):
    start_time = time.time()

    try:
        # Replace with your actual API endpoint
        if "rewrite: " not in query:
            query = f"rewrite: {query}"
        response = client_session.post(ML_ENDPOINT_URL, json={"inputs": query})
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        result = f"Error: {str(e)}"

    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    return result, f"Response Time: {processing_time} seconds"


# Create the Gradio interface
with gr.Blocks() as app:
    gr.Markdown(
        """
    # Query Reformulation Assistant

    This tool helps you rewrite text in different semantically style. Simply enter your text and it will be rewritten according to the prefix:
    The prefix "rewrite:" will be automatically added if not present.
    """
    )

    with gr.Row():
        query_input = gr.Textbox(
            label="Enter your text to rewrite",
            placeholder="Type your text here, or try one of the examples below...",
            lines=3,
        )

    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.Button("Clear")

    with gr.Row():
        response_output = gr.Textbox(label="Rewritten Text", lines=5, interactive=False)
        time_label = gr.Label(label="Processing Time")

    # Add examples section
    gr.Examples(
        examples=EXAMPLE_QUERIES,
        inputs=query_input,
        outputs=[response_output, time_label],
        fn=make_request,
        cache_examples=True,
        label="Example Queries",
    )

    # Clear button functionality
    clear_btn.click(
        lambda: ("", "", ""),  # Clear input  # Clear output  # Clear time label
        outputs=[query_input, response_output, time_label],
    )

    # Submit button click event
    submit_btn.click(
        fn=make_request, inputs=[query_input], outputs=[response_output, time_label]
    )

    # Add keyboard shortcut for submission
    query_input.submit(
        fn=make_request, inputs=[query_input], outputs=[response_output, time_label]
    )

# Launch the app
if __name__ == "__main__":
    app.launch()
