
from transformers import pipeline, Conversation, ConversationalPipeline

modelpath = "TheBloke/Guanaco-3B-Uncensored-v2-GPTQ"
converse : ConversationalPipeline = pipeline("conversational", model=modelpath)

conversation_1 = Conversation("Going to the movies tonight - any suggestions?")
conversation_2 = Conversation("What's the last book you have read?")

output = converse([conversation_1, conversation_2])
print(output)
