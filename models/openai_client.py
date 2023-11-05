import models.openai_client as openai_client

class OpenAIClient():   
    def __init__(self, config):
        self.client_secret = config["openai"]["client_secret"]