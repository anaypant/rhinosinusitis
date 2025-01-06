from together import Together
import random


def get_msg(conversation, mt=200):
    tai_key = "2e1a1e910693ae18c09ad0585a7645e0f4595e90ec35bb366b6f5520221b6ca7"
    client = Together(api_key=tai_key)

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=conversation,
        max_tokens=mt,
        temperature=1,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1.2,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=False
    )
    return response.choices[0].message.content