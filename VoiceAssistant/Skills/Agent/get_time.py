
from datetime import datetime
from SkillsManager import ArgumentParser

argParser = ArgumentParser()

def get_current_time():
    """
    Description: "Get the current time in HH:MM format."
    Additional Information: "This function returns the current time formatted as hour:minute."
    """
    argParser.printArgs(__name__, locals())
    return datetime.now().strftime('%H:%M')
