#import object files

import llm
from conf import *


def summarize(summ_prompt, conversation_txt_file, summ_output_file):


    # begins a new conversation with the user
    conversation = []
    convo = open(summ_prompt, "r").read()
    starting_msg = open(conversation_txt_file, "r").read()
    full_convo = starting_msg + "\n"  + ("-"*5)  + "\n" +  convo + "\n" + "\n"
    conversation.append({"role": "system", "content": full_convo})

    ai_msg = llm.get_msg(conversation=conversation, mt=500)
    print(ai_msg)

    # write respose to file
    with open(summ_output_file, "w") as f:
        f.write(ai_msg)
        f.close()