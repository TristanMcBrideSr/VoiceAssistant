
import json
import re
import inspect
import os
import threading
import logging
from dotenv import load_dotenv
from pathlib import Path

from SkillLink import SkillLink # Dont for get to pip install SkillLink

load_dotenv()

logger = logging.getLogger(__name__)


class SkillGraph:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SkillGraph, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.skillLink         = SkillLink()
        self.baseSkillsDir     = self.getDir('Skills')
        self.printCapabilities = os.getenv('SHOW_CAPABILITIES', 'False') == 'True'
        self.printMetaData     = os.getenv('SHOW_METADATA', 'False') == 'True'
        self.loadAllComponents()

    def getDir(self, *paths):
        return self.skillLink.getDir(*paths)

    def loadAllComponents(self):
        """
        Load all components from the specified directories.
        This method loads skills and tools from the 'Skills' directory.
        It also loads custom tools for the agent.
        """
        self.userSkills  = []
        self.agentSkills = []

        self.skillLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User')],
                [self.getDir(self.baseSkillsDir, 'Agent')],
            ],
            components=[
                self.userSkills,
                self.agentSkills,
            ],
            reloadable=[
                False,
                False,
            ]
        )

    def getUserActions(self, content):
        """
        Get user actions based on the provided content.
        This method combines dynamic, static, and restricted user skills to return the available actions.
        Use only if you want to get user actions based on the content provided.
        """
        skills = (
            self.userSkills
        )
        return self.skillLink.getComponents(skills, content)

    def getAgentActions(self):
        """
        Get self actions based on the skills available.
        This method combines dynamic, static, and restricted self skills.
        """
        skills = (
            self.agentSkills
        )
        return self.skillLink.getComponents(skills)

    def reloadSkills(self):
        """
        Reload all skills and print any new skills added.
        """
        original = self.getMetaData()
        self.skillLink.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} That {skill['description']}.\n")

    def getMetaData(self):
        """Get metadata for all skills."""
        metaData = (
                self.agentSkills
        )
        return self.skillLink.getMetaData(metaData, self.printMetaData)

    # ----- Skills -----
    def getAgentCapabilities(self):
        """
        Get the capabilities of the agent based on its skills.
        This method retrieves the capabilities of the agent's skills and returns them in a structured format.
        """
        description = False
        capabitites = (
            self.agentSkills
        )
        return self.skillLink.getCapabilities(capabitites, self.printCapabilities, description)

    def checkActions(self, action: str) -> str:
        """
        Check if the given action is valid based on the agent's skills.
        Returns a string indicating whether the action is valid or not.
        """
        return self.skillLink.actionParser.checkActions(action)

    def getActions(self, action: str) -> list:
        """
        Get a list of actions based on the given action string.
        This method uses the skills manager's action parser to retrieve actions that match the given string.
        If the action is not found, it returns an empty list.
        """
        return self.skillLink.actionParser.getActions(action)

    def executeAction(self, actions, action):
        """
        Execute a single action based on the provided actions and action string.
        You must create your own for loop if you want to execute multiple actions.
        """
        return self.skillLink.actionParser.executeAction(actions, action)

    def executeActions(self, actions, action):
        """
        Execute both single and multiple actions based on the provided actions and action string.
        The for loop is handled internally, so you can pass a single action or a list of actions.
        """
        return self.skillLink.actionParser.executeActions(actions, action)

    def skillInstructions(self):
        """
        Get skill instructions for the ava based on its capabilities.
        """
        # If you want to use the default skill instructions without examples, uncomment the next line
        # and comment the line below it.
        #return self.skillLink.skillInstructions(self.getAvaCapabilities())
        return self.skillLink.skillInstructions(self.getAvaCapabilities(), self.skillExamples())

    def skillExamples(self):
        """
        Get examples of how to use skills from your naming conventions.
        This should be customized to match your skill naming conventions.
        """
        return (
            "Single Action Examples:\n" # Don't change this line
            "- ['getDate()']\n" # Change to match your skill naming conventions
            "- ['getTime()']\n" # Change to match your skill naming conventions
            "- ['getDate()', 'getTime()']\n"
            "Skill With Sub-Action Examples:\n" # Don't change this line
            "- ['appSkill(\"open\", \"Notepad\")']\n" # Change to match your skill naming conventions
            "- ['appSkill(\"open\", \"Notepad\")', 'appSkill(\"open\", \"Word\")']\n"
            "- ['weatherSkill(\"get-weather\", 47.6588, -117.4260)']\n" # Change to match your skill naming conventions
        )


    # ----- Can be used with both skills and tools -----
    def isStructured(self, *args):
        """
        Check if any of the arguments is a list of dictionaries.
        This indicates structured input (multi-message format).
        """
        return self.skillLink.isStructured(*args)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        """
        Format content for Google GenAI APIs.
        """
        return self.skillLink.handleTypedFormat(role, content)

    def handleJsonFormat(self, role: str = "user", content: str = ""):
        """
        Format content for OpenAI APIs and similar JSON-based APIs.
        """
        return self.skillLink.handleJsonFormat(role, content)

    def formatTypedExamples(self, items):
        """
        Handle roles for Google GenAI APIs, converting items to Gemini Content/Part types.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleTypedFormat
            - dict: wrapped as Content with role, value as text
            - list of dicts: each dict converted to Content with role, dict as text
        Returns a flat list of Content objects.
        """
        return self.skillLink.formatTypedExamples(items)

    def formatJsonExamples(self, items):
        """
        Handle roles for OpenAI APIs, converting items to JSON message format.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleJsonFormat
            - dict: added as-is
            - list of dicts: each dict is added individually
        Returns a flat list of message dicts.
        """
        return self.skillLink.formatJsonExamples(items)

    def formatExamples(self, items, formatFunc):
        """
        Ultra-robust handler for message formatting.
        Accepts string, dict, list of any mix, any nested depth.
        Silently ignores None. Converts numbers and bools to strings.
        """
        return self.skillLink.formatExamples(items, formatFunc)

    def handleTypedExamples(self, items):
        """
        Handle roles for Google GenAI APIs, converting items to Gemini Content/Part types.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleTypedFormat
            - dict: wrapped as Content with role, value as text
            - list of dicts: each dict converted to Content with role, dict as text
        Returns a flat list of Content objects.
        """
        return self.skillLink.handleTypedExamples(items)

    def handleJsonExamples(self, items):
        """
        Handle roles for OpenAI APIs, converting items to JSON message format.
        Accepts a list of (role, value) tuples, where value can be:
            - str: will be wrapped using handleJsonFormat
            - dict: added as-is
            - list of dicts: each dict is added individually
        Returns a flat list of message dicts.
        """
        return self.skillLink.handleJsonExamples(items)

    def handleExamples(self, items, formatFunc):
        """
        Ultra-robust handler for message formatting.
        Accepts string, dict, list of any mix, any nested depth.
        Silently ignores None. Converts numbers and bools to strings.
        """
        return self.skillLink.handleExamples(items, formatFunc)

    def buildGoogleSafetySettings(self, harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
        """
        Construct a list of Google GenAI SafetySetting objects.
        """
        return self.skillLink.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)

