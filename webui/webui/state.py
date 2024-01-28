import os
import requests
import json
import openai
import reflex as rx

openai.api_key = os.getenv("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")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")



def get_access_token():
    """
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""
    question: str
    answer: str


DEFAULT_CHATS = {
    "Predictive Maintenance": [],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Predictive Maintenance"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    api_type: str = "baidu" if BAIDU_API_KEY else "openai"

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())
    
    def process_question(self, form_data: dict[str, str]):
        question = form_data["question"]
        if question == "":
            return

        # Append the question to the chat history
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        messages = [
            {"role": "system", "content": "You are a friendly chatbot named Reflex."}
        ]

        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})
        
        

        url = f"http://35.23.230.60:20100/sendMessage/{question}" # Assuming 'sendMessageee' is correct       
        try:
            response = requests.post(url)
            response_data =  response.json()["message"]
            self.chats[self.current_chat][-1].answer += response_data
            self.chats = self.chats


            # Rest of your processing code here
        except requests.RequestException as e:
            print(f"Request failed: {e}")
    '''
    def process_question(self, form_data: dict[str, str]
        question = form_data["question"]

        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)
        
        

        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Get the question from the form
      
        data={"message":question}
        url = "https://plankton-app-7tfzx.ondigitalocean.app/sendMessagee"
        data = {"message": "Your message here"}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)
        print(response.json())


        # Check if the question is empty
        if question == "":
            return

        try:
    # Sending a POST request to the API endpoint
            response = requests.post(url, json=data)

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Get the JSON response data
            response_data = response.json()
            return response_data["message"]
            print("Response from server:", response_data)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
    
        except Exception as err:
            print(f"An error occurred: {err}")
    '''
        
    async def openai_process_question(self, question: str):

        openai.api_key = "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"


        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are Elixr. You are suppose to give details of Patient B5, who is a bay "
                                          "in an NICU unit. The heart rate is 101, the o2 is at 90 and temperature is "
                                          "104 degrees farheiet. The patient is severe. Patient B14 has  heart rate of "
                                          "78 o2 is 100 and temprature is 96, the patient is improving. "
                                          "Keep the message conversational and breif. Do not say stuff like medical "
                                          "team is moniroing and stuff."}
        ]

        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = openai.ChatCompletion.create(

            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False

    async def baidu_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = json.dumps({"messages": messages[:-1]})
        # Start a new session to answer the question.
        session = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
            + get_access_token(),
            headers={"Content-Type": "application/json"},
            data=messages,
        )

        json_data = json.loads(session.text)
        if "result" in json_data.keys():
            answer_text = json_data["result"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        # Toggle the processing flag.
        self.processing = False
