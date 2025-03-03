#%%
from mj import ImageGenerator
from vng import VNGAnalyser
import os
import json
from tqdm.autonotebook import tqdm
import config

config.query_credits()
#%%
results_dir = "results/itemsVNG"
os.makedirs(results_dir, exist_ok=True)
with open("assets/SJT_item/SJTs.json", "r") as f:
    sjts = json.load(f)["items"]
#%%
analyser = VNGAnalyser()
situations = {}
situ_vng = {}

for dim, items in tqdm(sjts.items(), desc="Processing SJTs", position=0):
    if dim != "N":
        break
    for item_id, item in tqdm(
        items.items(), desc=f"Processing Dim.{dim}", position=1, leave=False
    ):
        # delete instruction
        this_sjt = ".".join(item.split(".")[:-1]) + "."
        res = analyser.call(this_sjt, json=True)

        situations[f"{dim}_{item_id}"] = this_sjt
        situ_vng[f"{dim}_{item_id}"] = res
        situ_vng[f"{dim}_{item_id}"].update({"situation": this_sjt})

with open(f"{results_dir}/situ_VNG_DimN.json", "w") as f:
    json.dump(situ_vng, f, indent=4)
#%%
