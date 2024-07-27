import json

def load_game(json_file, scene_data, classes):
    objs_loaded = json.load(json_file)

    blocks = []
    for i in range(len(objs_loaded["Blocks"])):
        block_data = objs_loaded["Blocks"][i]
        new_block = classes["Block"](block_data["x"] * scene_data["block_size"],
                                     scene_data["screen_height"] - (block_data["y"] + 1) * scene_data["block_size"],
                                     scene_data["block_size"]
                                     )
        blocks.append(new_block)
    

    traps = []
    for i in range(len(objs_loaded["Traps"])):
        trap_data = objs_loaded["Traps"][i]
        new_trap = classes["Traps"][trap_data["type"]](trap_data["x"] * scene_data["block_size"],
                                                        scene_data["screen_height"] - (trap_data["y"] + 1) * scene_data["block_size"],
                                                        trap_data["width"],
                                                        trap_data["height"]
                                                        )
        traps.append(new_trap)
        print(trap_data)



    return [*blocks, *traps]