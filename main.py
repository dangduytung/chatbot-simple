import gradio as gr
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from py_log import log

# Create a new chatbot
bot = ChatBot('Simple Chatbot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chatbot using the english greetings corpus
trainer.train('chatterbot.corpus.english')


def submit_chat(text, history):
    log.info(f'inp: {text}')
    history = history or []

    # Get response
    output = bot.get_response(text)
    output = str(output)
    log.info(f'bot: {output}')

    # Append to history
    history.append((text, output))
    return history, history


css = """
    #row_bot{width: 70%; height: var(--size-96); margin: 0 auto}
    #row_bot .block{background: var(--color-grey-100); height: 100%}
    #row_input{width: 70%; margin: 0 auto}
    #row_input .block{background: var(--color-grey-100)}

    @media screen and (max-width: 768px) {
        #row_bot{width: 100%; height: var(--size-96); margin: 0 auto}
        #row_bot .block{background: var(--color-grey-100); height: 100%}
        #row_input{width: 100%; margin: 0 auto}
        #row_input .block{background: var(--color-grey-100)}    
    }
    """
block = gr.Blocks(css=css, title="Simple Chatbot")

with block:
    gr.Markdown(
        """<p style="font-size:40px; text-align: center">&#128540;</p>""")
    with gr.Row(elem_id='row_bot'):
        chatbot = gr.Chatbot()
    with gr.Row(elem_id='row_input'):
        message = gr.Textbox(placeholder="Enter something")
        state = gr.State()

        message.submit(submit_chat, inputs=[
                       message, state], outputs=[chatbot, state])
        message.submit(lambda x: "", message, message)


# Params ex: debug=True, share=True, server_name="0.0.0.0", server_port=5050
block.launch()
