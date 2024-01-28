import openai
client = openai.OpenAI(api_key="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")
thread_id = "thread_LOA4eknVmFwSDGky3CE8I2HP"
def create_thread():
    thread = client.beta.threads.create(messages=[{"role": "user", "content": "Hi"}])
    thread_id = thread.id
    return thread_id
print(create_thread())