"""
EVBot Chatbot - Intelligent EV Battery Advisor powered by hosted LLM APIs.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled at runtime
    OpenAI = None  # type: ignore[assignment]

try:
    from huggingface_hub import InferenceClient
except ImportError:  # pragma: no cover - handled at runtime
    InferenceClient = None  # type: ignore[assignment]

from ml_model import predict_from_payload


SYSTEM_PROMPT = """You are EVBot, a virtual assistant that provides electric vehicle battery advice.
Focus on EV charging strategies, battery health, efficiency, thermal management, and maintenance best practices.
Give concise, actionable answers tailored to everyday EV owners.
If you are uncertain or the user asks for something outside EV battery guidance, acknowledge the limitation clearly."""


class EVBotChatbot:
    """Chatbot that delegates responses to OpenAI or Hugging Face models using API keys."""

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        openai_model: Optional[str] = None,
        hf_api_key: Optional[str] = None,
        hf_model: Optional[str] = None,
    ) -> None:
        self._provider: Optional[str] = None
        self._client: Optional[object] = None

        self._openai_model = openai_model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._hf_model = hf_model or os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")

        openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        hf_key = hf_api_key or os.getenv("HF_API_KEY")

        # Prefer OpenAI if both keys are supplied.
        if openai_key:
            self.set_openai_key(openai_key)
        elif hf_key:
            self.set_hf_key(hf_key)
        else:
            print("EVBotChatbot: No API key detected for OpenAI or Hugging Face.")

    # --------------------------------------------------------------------- #
    # Provider configuration helpers
    # --------------------------------------------------------------------- #
    def set_openai_key(self, api_key: Optional[str]) -> None:
        """Configure the OpenAI client."""
        if api_key and OpenAI is not None:
            self._client = OpenAI(api_key=api_key)
            self._provider = "openai"
            self._openai_key = api_key
        else:
            self._openai_key = None
            if self._provider == "openai":
                self._provider = None
            if OpenAI is None and api_key:
                # Library missing; keep provider unset so we can surface message later.
                self._client = None

        # If we lost OpenAI configuration but have HF available, fall back.
        if self._provider is None and os.getenv("HF_API_KEY"):
            self.set_hf_key(os.getenv("HF_API_KEY"))

    def set_hf_key(self, api_key: Optional[str]) -> None:
        """Configure the Hugging Face Inference client."""
        if api_key:
            os.environ["HF_API_KEY"] = api_key
        if api_key and InferenceClient is not None:
            self._client = InferenceClient(model=self._hf_model, token=api_key)
            self._provider = "huggingface"
            self._hf_key = api_key
        else:
            self._hf_key = None
            if self._provider == "huggingface":
                self._provider = None
            if InferenceClient is None and api_key:
                self._client = None

        # If we lost HF configuration but have OpenAI available, fall back.
        if self._provider is None and os.getenv("OPENAI_API_KEY"):
            self.set_openai_key(os.getenv("OPENAI_API_KEY"))

    # --------------------------------------------------------------------- #
    # Response generation
    # --------------------------------------------------------------------- #
    def _format_model_summary(self, payload: Dict[str, Any]) -> str:
        prediction = predict_from_payload(payload)
        inputs = prediction["inputs"]

        key_metrics = (
            f"SOC {inputs['SOC (%)']}%, Voltage {inputs['Voltage (V)']} V, "
            f"Current {inputs['Current (A)']} A, Duration {inputs['Charging Duration (min)']} min, "
            f"Efficiency {inputs['Efficiency (%)']}%"
        )

        return (
            "EV model prediction:\n"
            f"- Outcome: {prediction['message']}\n"
            f"- Result type: {prediction['result_type']}\n"
            f"- Key metrics: {key_metrics}\n"
            f"- Battery: {inputs['Battery Type']} / {inputs['EV Model']} / Mode {inputs['Charging Mode']}"
        )

    def get_response(
        self,
        user_input: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Process user input and return a response from the configured provider."""
        if not user_input:
            return "Please ask me a question about EV battery maintenance or charging!"

        if self._provider == "openai":
            if OpenAI is None:
                return (
                    "The chatbot service is unavailable because the OpenAI client library "
                    "is not installed. Please install the 'openai' package."
                )
            if not getattr(self, "_openai_key", None):
                return (
                    "The chatbot is not configured yet. Please set the OPENAI_API_KEY "
                    "environment variable and restart the application."
                )

            supplemental_context = []
            if payload:
                try:
                    supplemental_context.append(self._format_model_summary(payload))
                except Exception as exc:  # pragma: no cover - validation errors
                    supplemental_context.append(
                        "EV model assistance is unavailable for this request."
                    )
                    supplemental_context.append(f"Model error: {exc}")

            try:
                response = self._client.responses.create(
                    model=self._openai_model,
                    input=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *({"role": "system", "content": ctx} for ctx in supplemental_context),
                        {"role": "user", "content": user_input.strip()},
                    ],
                    max_output_tokens=400,
                )
            except Exception as exc:  # pragma: no cover - network/runtime errors
                return f"Sorry, I couldn't reach the EV assistant service: {exc}"

            output_text = getattr(response, "output_text", "").strip()
            if not output_text:
                return (
                    "I’m sorry, I couldn’t generate a response right now. "
                    "Please try asking your EV question again."
                )

            return output_text

        if self._provider == "huggingface":
            if InferenceClient is None:
                return (
                    "The chatbot service is unavailable because the Hugging Face client "
                    "library is not installed. Please install 'huggingface_hub'."
                )
            if not getattr(self, "_hf_key", None):
                return (
                    "The chatbot is not configured yet. Please set the HF_API_KEY "
                    "environment variable and restart the application."
                )

            supplemental_context = []
            if payload:
                try:
                    supplemental_context.append(
                        self._format_model_summary(payload)
                    )
                except Exception as exc:  # pragma: no cover - validation errors
                    supplemental_context.append(
                        "EV model assistance is unavailable for this request."
                    )
                    supplemental_context.append(f"Model error: {exc}")

            try:
                response = self._client.chat.completions.create(
                    model=self._hf_model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *({"role": "system", "content": ctx} for ctx in supplemental_context),
                        {"role": "user", "content": user_input.strip()},
                    ],
                    max_tokens=400,
                    temperature=0.4,
                )
            except Exception as exc:  # pragma: no cover - network/runtime errors
                return f"Sorry, I couldn't reach the EV assistant service: {exc}"

            choices = getattr(response, "choices", None)
            if not choices:
                return (
                    "I’m sorry, I couldn’t generate a response right now. "
                    "Please try asking your EV question again."
                )

            message = choices[0].message
            # message may be dict or object depending on library version
            content = getattr(message, "content", None) or message.get("content")  # type: ignore[index]
            if isinstance(content, list):
                content = " ".join(part.get("text", "") for part in content)

            content = (content or "").strip()
            if not content:
                return (
                    "I’m sorry, I couldn’t generate a response right now. "
                    "Please try asking your EV question again."
                )

            return content

        # If no provider is configured, instruct user.
        return (
            "The chatbot is not configured yet. Please set either OPENAI_API_KEY or "
            "HF_API_KEY as an environment variable and restart the application."
        )

    def provider(self) -> Optional[str]:
        """Return the active provider."""
        return self._provider


# Global chatbot instance
chatbot = EVBotChatbot()
if chatbot.provider():
    print(f"EVBotChatbot: Using provider '{chatbot.provider()}' with model "
          f"{'OPENAI_MODEL' if chatbot.provider() == 'openai' else 'HF_MODEL'}.")
