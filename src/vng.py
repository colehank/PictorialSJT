#%%
from openai import OpenAI
import os
import os.path as op
import re
import json
from config import LLMConfig
from . import utils


class VNGAnalyser:
    def __init__(self):
        self.client = OpenAI(
            base_url=LLMConfig.base_url,
            api_key=LLMConfig.api_key,
        )

    def call(
        self,
        situation: str,
        json: bool = True,
    ) -> str:
        msg = [
            {"role": "system", "content": LLMConfig.VNGAnalyser_prompt},
            {"role": "user", "content": situation},
        ]
        response = self.client.chat.completions.create(
            messages=msg,
            response_format=LLMConfig.response_format,
            model=LLMConfig.model,
            max_tokens=LLMConfig.max_tokens,
            temperature=LLMConfig.temperature,
            top_p=LLMConfig.top_p,
            frequency_penalty=LLMConfig.frequency_penalty,
            presence_penalty=LLMConfig.presence_penalty,
            stop=LLMConfig.stop,
        )
        content = response.choices[0].message.content.strip()

        if json:
            return utils.extract_json(content)
        else:
            return content


class VNGGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url=LLMConfig.base_url,
            api_key=LLMConfig.api_key,
        )

    def call(
        self,
        arc: str,
        json: bool = True,
    ) -> str:
        msg = [
            {"role": "system", "content": LLMConfig.VNGGenerator_prompt},
            {"role": "user", "content": arc},
        ]
        response = self.client.chat.completions.create(
            messages=msg,
            response_format=LLMConfig.response_format,
            model=LLMConfig.model,
            max_tokens=LLMConfig.max_tokens,
            temperature=LLMConfig.temperature,
            top_p=LLMConfig.top_p,
            frequency_penalty=LLMConfig.frequency_penalty,
            presence_penalty=LLMConfig.presence_penalty,
            stop=LLMConfig.stop,
        )
        content = response.choices[0].message.content.strip()

        if json:
            return utils.extract_json(content)
        else:
            return content


#%%
if __name__ == "__main__":
    situ = """
    You have taken your subordinate officer’s report at home to check and make corrections.
    Suddenly youremember that you have to attend the marriage of your friend.
    You are already late.
    """
    analyser = VNGAnalyser()
    generator = VNGGenerator()
    vng_comp = analyser.call(situ, json=True)
    with open("vng_output.json", "w") as f:
        json.dump(vng_comp, f, indent=4)
    # vng_prompt = generator.call(str(vng_comp))
    # print(vng_comp)
    # print(vng_prompt)
#
#%%
