from litellm import completion
# import litellm
# litellm._turn_on_debug()

def gen_use_local_llamafile():
    def use_local_llamafile():
        messages = [{"content": "Write a limerick about ClickHouse", "role": "user"}]
        response = completion(
                    model="hosted_vllm/llamafile/mistral-7b-instruct-v0.2.Q4_K_M", # pass the vllm model name
                    messages=messages,
                    api_base="http://localhost:8080/v1",
                    temperature=0.2,
                    max_tokens=80)
        return response
    return use_local_llamafile

