import json

jsonFile = open("settings.json")
jsonStr = jsonFile.read()
jsonFile.close()
settings = json.loads(jsonStr)


class Config:
    PATH = settings["path"]
    INTEGRATE_PRECISION = settings["integrate_precision"]
    CIRCLES_COLOR = settings["circles_color"]
    TRACK_COLOR = settings["track_color"]
    ORIGIN_COLOR = settings["origin_color"]
    X_AXIS_COLOR = settings["x_axis_color"]
    Y_AXIS_COLOR = settings["y_axis_color"]
    BACKGROUND_COLOR = settings["background_color"]
    WINDOW_SIZE = settings["window_size"]
    GRAPH_SCALE = settings["graph_scale"]
    ORDER = settings["order"]
    DELTA_T = settings["delta_t"]
    FPS = settings["fps"]
    WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE
    ORIGIN_POSITION = (
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
    )
