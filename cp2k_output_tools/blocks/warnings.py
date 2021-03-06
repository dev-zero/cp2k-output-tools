import regex as re


WARNING_MESSAGE_RE = re.compile(
    r"""
^\ \*{3}\ WARNING\ in\ (?<filename>[^:]+):(?P<line>\d+)\ ::\ (?P<message>.+?) \*{3} \n
(\ \*{3}\ (?P<message>.+?) \*{3} \n)*
""",
    re.VERSION1 | re.VERBOSE | re.MULTILINE,
)

TOTAL_WARNING_COUNT_RE = re.compile(
    r"""
^\ The\ number\ of\ warnings\ for\ this\ run\ is\ :\s* (?P<value>\d+)
""",
    re.VERBOSE | re.MULTILINE,
)


def match_warnings(content):
    result = {"warnings": []}

    for wmatch in WARNING_MESSAGE_RE.finditer(content):
        result["warnings"] += [
            {"filename": wmatch["filename"], "line": int(wmatch["line"]), "message": "".join(wmatch.captures("message")).rstrip()}
        ]

    match = TOTAL_WARNING_COUNT_RE.search(content)
    if match:
        result["nwarnings"] = int(match["value"])

    return result
