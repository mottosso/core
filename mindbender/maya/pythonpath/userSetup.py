"""Maya initialisation for Mindbender pipeline"""

from maya import cmds

import os


def setup():
    assert __import__("pyblish_maya").is_setup(), (
        "mindbender-core depends on pyblish_maya which has not "
        "yet been setup. Run pyblish_maya.setup()")

    from mindbender import api, maya
    api.install(maya)

    FPS = {
        "12": "12fps",
        "15": "game",
        "16": "16fps",
        "24": "film",
        "25": "pal",
        "30": "ntsc",
        "48": "show",
        "50": "palf",
        "60": "ntscf"
    }.get(os.getenv("MINDBENDER_FPS"), "pal")  # Default to "pal"

    # Load dependencies
    cmds.loadPlugin("AbcExport.mll", quiet=True)
    cmds.loadPlugin("AbcImport.mll", quiet=True)

    EDIT_IN = getenv("MINDBENDER_EDIT_IN", int) or 101
    EDIT_OUT = getenv("MINDBENDER_EDIT_OUT", int) or 201
    RESOLUTION_WIDTH = getenv("MINDBENDER_RESOLUTION_WIDTH", int) or 1920
    RESOLUTION_HEIGHT = getenv("MINDBENDER_RESOLUTION_HEIGHT", int) or 1080

    cmds.setAttr("defaultResolution.width", RESOLUTION_WIDTH)
    cmds.setAttr("defaultResolution.height", RESOLUTION_HEIGHT)
    cmds.currentUnit(time=FPS)
    cmds.playbackOptions(minTime=EDIT_IN)
    cmds.playbackOptions(maxTime=EDIT_OUT)
    cmds.playbackOptions(animationStartTime=EDIT_IN)
    cmds.playbackOptions(animationEndTime=EDIT_OUT)
    cmds.playbackOptions(minTime=EDIT_IN)
    cmds.playbackOptions(maxTime=EDIT_OUT)


def getenv(var, typ):
    """Return `var` from environment as `typ`"""
    try:
        return typ(os.getenv(var))
    except TypeError:
        return None


# Allow time for dependencies (e.g. pyblish-maya)
# to be installed first.
cmds.evalDeferred(setup)
