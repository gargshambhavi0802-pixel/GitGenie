import os
import copy
from typing import Any

import litellm
from dotenv import load_dotenv

from crewai.llms.base_llm import BaseLLM

load_dotenv()


class GeminiGroqFallbackLLM(BaseLLM):
    """
    CrewAI BaseLLM implementation

    Gemini first
    ↓
    if fails
    ↓
    Groq
    """

    def __init__(self):
        super().__init__(
            model="gemini/gemini-2.0-flash",
            temperature=0.3,
            provider="gemini"
        )

        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        self.groq_model = "groq/llama-3.3-70b-versatile"

    def _clean_messages(self, messages):

        cleaned = []

        for msg in messages:

            m = copy.deepcopy(msg)

            if isinstance(m, dict):

                # Gemini-only fields
                m.pop("cache_breakpoint", None)
                m.pop("cached_content", None)
                m.pop("cache_control", None)

                # Anthropic fields
                m.pop("thinking", None)

                # OpenAI beta fields
                m.pop("reasoning", None)

                # provider metadata
                m.pop("provider_options", None)

            cleaned.append(m)

        return cleaned

    def _clean_kwargs(self, kwargs):

        kwargs = dict(kwargs)

        remove = [
            "cache_breakpoint",
            "cached_content",
            "cache_control",
            "provider_options",
            "thinking",
            "reasoning",
            "response_model",
            "callbacks",
            "from_task",
            "from_agent",
            "available_functions"
        ]

        for k in remove:
            kwargs.pop(k, None)

        return kwargs

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):

        if isinstance(messages, str):
            messages = [
                {
                    "role": "user",
                    "content": messages
                }
            ]

        messages = self._clean_messages(messages)

        try:

            print("\n✨ Trying Gemini...\n")

            response = litellm.completion(
                model="gemini/gemini-2.0-flash",
                api_key=self.gemini_key,
                messages=messages,
                temperature=self.temperature,
                tools=tools,
            )

        except Exception as gemini_error:

            print("\n⚠ Gemini Failed")
            print(gemini_error)

            print("\n🔥 Switching to Groq...\n")

            messages = self._clean_messages(messages)

            try:

                response = litellm.completion(
                    model=self.groq_model,
                    api_key=self.groq_key,
                    base_url="https://api.groq.com/openai/v1",
                    messages=messages,
                    temperature=self.temperature,
                    tools=tools,
                )

                return response.choices[0].message.content

            except Exception as groq_error:

                print("\n❌ Groq also failed\n")
                print(groq_error)

                raise RuntimeError(
                    f"""
Gemini Error:
{gemini_error}

-------------------------------------

Groq Error:
{groq_error}
"""
                )     

              
              
                

    async def acall(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):
        return self.call(
            messages=messages,
            tools=tools,
            callbacks=callbacks,
            available_functions=available_functions,
            from_task=from_task,
            from_agent=from_agent,
            response_model=response_model,
        )

    def supports_function_calling(self) -> bool:
        return True

    def supports_stop_words(self) -> bool:
        return True

    def get_context_window_size(self) -> int:
        return 128000