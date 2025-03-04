# %%
import json
import time
import io
import base64
import requests
from PIL import Image
from config import MJConfig
from wasabi import msg
import tqdm

GEN_URL = MJConfig.gen_url
STATUS_URL = MJConfig.status_url
IMG_URL = MJConfig.img_url
# %%


class ImageGenerator:
    def __init__(self, c_ref: str = None, s_ref: str = None):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MJConfig.api_key}",
        }
        if c_ref:
            self.c_ref = self.upload_image(c_ref)
            self.ref_character = Image.open(c_ref)
        if s_ref:
            self.s_ref = self.upload_image(s_ref)
            self.ref_style = Image.open(s_ref)
        self.generated = []

    def modify_ref(self, c_ref: str = None, s_ref: str = None):
        if c_ref:
            self.c_ref = self.upload_image(c_ref)
            self.ref_character = Image.open(c_ref)
        if s_ref:
            self.s_ref = self.upload_image(s_ref)
            self.ref_style = Image.open(s_ref)

    def generate_image(
        self,
        prompt: str,
        model: str = "6.1",
        ar: str = "1:1",
        stylize: int = 50,  # 0-1000
        seed: int = MJConfig.seed,  # 0-1000000
        c_ref: bool = False,
        s_ref: bool = False,
        cw: int = None,  # Optional weight for character reference
        sw: int = None,  # Optional weight for style reference
        no: list[str] = None,
        chaos: int = 0,
    ):
        prompt_input = (
            f"{prompt} --v {model} --s {stylize} --seed {seed} --chaos {chaos}"
        )
        if c_ref:
            prompt_input += f" --cref {self.c_ref}"
        if s_ref:
            prompt_input += f" --sref {self.s_ref}"
        if cw is not None:
            prompt_input += f" --cw {cw}"
        if sw is not None:
            prompt_input += f" --sw {sw}"
        if no:
            prompt_input += f" --no {', '.join(no)}"
        if ar:
            prompt_input += f" --ar {ar}"
        print(f"PROMPT: {prompt_input}")

        payload = json.dumps({"prompt": prompt_input})
        task_id = self._submit_request(payload)
        self._wait_for_result(task_id, action="Generation")
        image = self._get_img(task_id)
        self.generated.append({"id": task_id, "prompt": prompt_input})
        return task_id, image

    def action(self, task_id: str, action: str, img_id: int):
        if action not in ["UPSCALE", "VARIATION", "REROOL", "ZOOM"]:
            raise ValueError("Invalid action")

        img_index = int(img_id)
        payload = json.dumps(
            {
                "action": action,
                "index": img_index,
                "taskId": task_id,
            }
        )
        response = requests.post(
            MJConfig.img_change_url, headers=self.headers, data=payload
        )
        new_task_id = response.json()["result"]
        self._wait_for_result(new_task_id, action=action)
        image = self._get_img(new_task_id)
        self.generated.append({"id": new_task_id, "prompt": action})
        return new_task_id, image

    def _submit_request(self, payload: str) -> str:
        response = requests.post(GEN_URL, headers=self.headers, data=payload)
        try:
            return response.json()["result"]
        except KeyError:
            raise RuntimeError(response.json().get("description", "Unknown error"))

    def _check_status(self, task_id: str):
        response = requests.get(STATUS_URL.format(task_id), headers=self.headers)
        data = response.json()
        status = data["status"]
        progress_value = data.get("progress", "0%").split("%")[0]
        return status, int(progress_value) if progress_value.isdigit() else 0

    def _wait_for_result(self, task_id: str, action: str = "Gen"):
        with tqdm.tqdm(total=100, desc=f"{action} - Pending") as pbar:
            while True:
                time.sleep(1)
                status, progress = self._check_status(task_id)
                pbar.n = progress
                pbar.set_description(f"{action} - {status}")
                pbar.refresh()
                if status == "SUCCESS":
                    break
                if status == "FAILURE":
                    msg.fail(f"{action} failed. Please try again.")
                    response = requests.get(
                        STATUS_URL.format(task_id), headers=self.headers
                    )
                    raise ValueError(response.json()["failReason"])
        return task_id

    def _get_img(self, task_id: str) -> Image.Image:
        response = requests.get(IMG_URL.format(task_id), headers=self.headers)
        return Image.open(io.BytesIO(response.content))

    def upload_image(self, image: str | Image.Image) -> str:
        if isinstance(image, str):
            with open(image, "rb") as image_file:
                img_data = image_file.read()
        elif isinstance(image, Image.Image):
            with io.BytesIO() as buffer:
                image.save(buffer, format="JPEG")
                img_data = buffer.getvalue()
        else:
            raise ValueError("Image must be a path or a PIL Image object")

        encoded_image = base64.b64encode(img_data).decode("utf-8")
        payload = json.dumps({"base64Array": [encoded_image]})
        response = requests.post(
            MJConfig.img_upload_url, headers=self.headers, data=payload
        )
        resp_json = response.json()
        if resp_json.get("description") == "success":
            msg.good("Reference image uploaded successfully")
            return resp_json["result"][0]
        else:
            msg.fail(resp_json)
            raise ValueError("Reference image upload failed")


# %%
if __name__ == "__main__":
    prompt = (
        "A human is giving a presentation to the colleagues in a meeting room, "
        "with a bunch of people sitting in the conference room listening to his speech, wide shot."
    )
    generator = ImageGenerator(c_ref="assets/characters/image/female_0.jpg")
    task_id, image = generator.generate_image(prompt, c_ref=True, cw=100)
    picked_task, picked_img = generator.action(task_id, "UPSCALE", 1)
# %%
