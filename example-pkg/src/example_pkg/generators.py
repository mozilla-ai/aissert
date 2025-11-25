"""LLM generator functions using litellm."""

from collections.abc import Callable
from typing import Any

from litellm import completion

# import litellm
# litellm._turn_on_debug()


def gen_use_local_llamafile() -> Callable[[], Any]:  # noqa: ANN401
    """Generate a function that uses local llamafile for LLM completion.

    Returns:
        Function that makes completion requests to local llamafile instance.
    """

    def use_local_llamafile() -> Any:  # noqa: ANN401
        """Make a completion request to local llamafile server.

        Returns:
            LLM completion response.
        """
        messages = [{"content": "Write a limerick about ClickHouse", "role": "user"}]
        response = completion(
            model="hosted_vllm/llamafile/mistral-7b-instruct-v0.2.Q4_K_M",  # pass the vllm model name
            messages=messages,
            api_base="http://localhost:8080/v1",
            temperature=0.2,
            max_tokens=80,
        )
        return response

    return use_local_llamafile
