"""
Module for parsing event XML files from Golden Treasure: the Great Green.
"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from typing import Optional, List, Dict


@dataclass
class EventOption:
    """Dataclass for event option.

    Fields:
        text: The displayed text of the event option.
        hidden_text: The hidden text of the event option.
            None if there is none.
        destinations: The list of all possible destinations.
            Variable substitutions are not handled.

    TODO: Handle pre-requirements
    TODO: Handle pre-requirements of destinations
    TODO: Handle variable changes of destinations
    """

    text: str
    hidden_text: Optional[str]
    destinations: List[str]


@dataclass
class Event:
    """Dataclass for event.

    Fields:
        name: name of the event
        texts: List of the text breaks of the event
        options: List of the options of the event

    TODO: Handle pre-requirements
    TODO: Handle variable changes
    """

    name: str
    texts: List[str]
    options: List[EventOption]


def parse_event_file(path: str) -> Dict[str, Event]:
    """Parse a event file given its path,
    and return a dict with event name as key and Event objects as items.

    Args:
        path (str): path of the event xml to be parsed

    Returns:
        Dict[str, Event]: the parsed events
    """
    events_tree = ET.parse(path)
    events_root = events_tree.getroot()

    events_all = {}
    for event_tag in events_root.findall("event"):
        event_name = event_tag.find("event_name").text

        event_body = event_tag.find("event_body")
        texts = []
        if event_body is not None:
            for text_break in event_body.findall("text_break"):
                if text_break.find("text") is None:
                    texts.append("")
                    continue
                texts.append(text_break.find("text").text or "")

        options = []
        event_options = event_tag.find("event_options")
        if event_options is not None:
            for event_option in event_options.findall("event_option"):
                option_text = event_option.find("option_text").text
                hidden_text_tag = event_option.find("hidden_message_text")
                hidden_text = (
                    hidden_text_tag.text
                    if hidden_text_tag is not None else None)
                destinations = []
                if event_option.find("destinations") is not None:
                    for destinations_node in event_option.find(
                            "destinations").findall("destination"):
                        if destinations_node.find(
                                "destination_id") is not None:
                            destinations.append(
                                destinations_node.find("destination_id").text
                                or "")
                options.append(EventOption(
                    text=option_text, hidden_text=hidden_text,
                    destinations=destinations,
                    ))

        events_all[event_name] = Event(
            name=event_name, texts=texts, options=options)

    return events_all
