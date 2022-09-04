import re

import lavalink

to_camel_regex1 = re.compile("(.)([A-Z][a-z]+)")
to_camel_regex2 = re.compile("([a-z0-9])([A-Z])")


def to_camel(string: str) -> str:
    string = re.sub(to_camel_regex1, r"\1_\2", string)
    return re.sub(to_camel_regex2, r"\1_\2", string).lower()


def format_track(at: lavalink.AudioTrack, prefix: str = "- ") -> str:
    duration = lavalink.utils.format_time(at.duration)

    if duration.startswith("00:"):
        duration = duration[3:]

    return f"{prefix}[{at.title}](<{at.uri}>) ({duration})"
