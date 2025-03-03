#%%
import src
#%%
ImageGenerator = src.ImageGenerator
prompt = (
"A human is giving a presentation to the colleagues in a meeting room, "
"with a bunch of people sitting in the conference room listening to his speech,"
"wide shot.")

generator = ImageGenerator(c_ref="assets/characters/image/female_0.png")
task_id, image = generator.generate_image(prompt, c_ref=True, cw=100)
picked_task, picked_img = generator.action(task_id, "UPSCALE", 1)