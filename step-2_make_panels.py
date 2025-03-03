# %%
import config
from vng import VNGGenerator
from mj import ImageGenerator
import json
import utils

# %%
items = json.load(open("results/itemsVNG/situ_VNG_DimN.json", "rb"))
# %%
c_ref = "assets/characters/image/female_0.jpg"

test_prompt = {
    "1": "a young adult with medium-length black hair, wearing a dark hoodie and jeans, sitting in the middle of a crowded movie theater, surrounded by people of various ages, popcorn and drinks in hand, dimly lit environment with a large screen at the front, excited chatter filling the air, wide shot capturing the bustling atmosphere",
    "2": "you, looking around with anticipation, medium-length black hair, dark hoodie and jeans, slightly leaning forward in your seat, film credits rolling on the screen, ambient light from the screen illuminating your face, medium shot focusing on your expression of excitement, soft glow enhancing the cinematic experience",
    "3": "you, suddenly realizing your mistake, eyes wide with shock, medium-length black hair falling over your forehead, dark hoodie, surrounded by bewildered audience members, the film scene on the screen depicting an entirely different genre than expected, bright screen casting eerie shadows, close-up shot of your concerned expression, tension rising in the air",
}

gen = ImageGenerator()
imgs1, idx1 = gen.generate_image(test_prompt["1"], c_ref=c_ref, cw=100)
# %%
imgs2, idx2 = gen.generate_image(test_prompt["2"], c_ref=c_ref, cw=100)
# %%
imgs3, idx3 = gen.generate_image(test_prompt["3"], c_ref=c_ref, cw=100)
# %%
panel1 = gen.action(idx, "UPSCALE", 2)[0]
panel2 = gen.action(idx2, "UPSCALE", 4)[0]
panel3 = gen.action(idx3, "UPSCALE", 3)[0]
# %%
comic = utils.make_sequence([panel1, panel2, panel3])
comic.save("results/comic_test.tif")
