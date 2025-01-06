#import object files

import llm
from conf import *



def recommend(recc_prompt, summarization_file, list_tests, output_file):


    # begins a new conversation with the user
    conversation = []
    starting_msg = open(recc_prompt, "r").read()
    summ = open(summarization_file, "r").read()
    tests = open(list_tests, "r").read()

    full_convo = starting_msg + "\n"  + ("-"*5)  + "\n" +  summ + "\n" + tests + "\n" + "\n"
    conversation.append({"role": "system", "content": full_convo})

    ai_msg = llm.get_msg(conversation=conversation)
    print(ai_msg)

    # write respose to file
    with open(output_file, "w") as f:
        f.write(ai_msg)
        f.close()