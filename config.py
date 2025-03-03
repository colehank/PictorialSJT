#%%
import os
import os.path as op
import requests
from dotenv import load_dotenv
from wasabi import msg
from typing import ClassVar
from openai import OpenAI

load_dotenv()

SEED = 464365
VNG_ANA_PATH: str = "assets/prompts/VNGAnalyser.txt"
VNG_GEN_PATH: str = "assets/prompts/VNGGenerator.txt"
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE: float = 1
LLM_TOP_P: float = 0.95
LLM_MAX_TOKENS: int = 4096
LLM_FREQUENCY_PENALTY: float = 0
LLM_PRESENCE_PENALTY: float = 0
LLM_STOP: bool = None


class V3Config:
    url = "https://api.gpt.ge"
    api_key = os.getenv("openai_api")


class MJConfig:
    seed = SEED
    api_key = V3Config.api_key
    root_url = V3Config.url
    gen_url = f"{root_url}/mj/submit/imagine"
    status_url = f"{root_url}/mj/task/{{}}/fetch"
    img_url = f"{root_url}/mj/image/{{}}"
    img_upload_url = f"{root_url}/mj/submit/upload-discord-images"
    img_change_url = f"{root_url}/mj/submit/change"


def query_credits(url=V3Config.url, api_key=V3Config.api_key):
    credits_used = (
        requests.get(
            f"{url}/v1/dashboard/billing/usage",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()["total_usage"]
        / 100
    )

    all_credits = requests.get(
        f"{url}/v1/dashboard/billing/subscription",
        headers={"Authorization": f"Bearer {api_key}"},
    ).json()["soft_limit_usd"]
    remaining_credits = all_credits - credits_used
    msg.info(f"Total credits: {all_credits:.2f}")
    msg.info(f"Used credits: {credits_used:.2f}")
    msg.info(f"Remaining credits: {remaining_credits:.2f}")


class LLMConfig:
    model: str = LLM_MODEL
    api_key: str = os.getenv("openai_api")
    base_url: str = os.getenv("openai_url")
    response_format: ClassVar[dict] = {"type": "json_object"}
    VNGAnalyser_prompt: ClassVar[str] = open(VNG_ANA_PATH, "r").read()
    VNGGenerator_prompt: ClassVar[str] = open(VNG_GEN_PATH, "r").read()
    temperature: float = LLM_TEMPERATURE
    top_p: float = LLM_TOP_P
    max_tokens: int = LLM_MAX_TOKENS
    frequency_penalty: float = LLM_FREQUENCY_PENALTY
    presence_penalty: float = LLM_PRESENCE_PENALTY
    stop: str = LLM_STOP


#%%
