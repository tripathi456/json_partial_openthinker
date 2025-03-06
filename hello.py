from json_partial_py import to_json_string
from rich.console import Console
from rich.table import Table
import json 

# Key not quoted, value not quoted
MALFORMED_JSON = """
{abhi: shek}
"""

# Key not quoted (valid JSON requires double quotes around keys)
MALFORMED_JSON2 = """
{abhi: "shek"}
"""

# Single quotes used instead of double quotes, trailing comma
MALFORMED_JSON3 = """
{'name': 'value',}
"""

# Missing closing brace, unclosed object
MALFORMED_JSON4 = """
{'name': 'value'
"""

# Mismatched quotes (double single-quote), trailing comma
MALFORMED_JSON5 = """
{'name': 'value'',}
"""

# Mismatched quotes, missing closing brace
MALFORMED_JSON6 = """
{'name': 'value''
"""

# Unquoted value, mismatched quotes
MALFORMED_JSON7 = """
{'name': value'}
"""

# Unquoted value, missing closing quote and brace
MALFORMED_JSON8 = """
{'name': value'
"""

# Valid JSON syntax but using single quotes for key, double quotes for the value
MALFORMED_JSON9 = """
{'name': "value"}
"""

# Mismatched quotes (double+single), unclosed value
MALFORMED_JSON10 = """
{'name': "value'
"""

# Unquoted value
MALFORMED_JSON11 = """
{'name': value}
"""

# Key not quoted (invalid identifier syntax)
MALFORMED_JSON12 = """
{name: "value"}
"""

MALFORMED_JSON13=r"""
{ rec_one: "and then i said \"hi\", and also \"bye\"", rec_two: "and then i said "hi", and also "bye"", "also_rec_one": ok }
"""



malformed_jsons = [
    MALFORMED_JSON,
    MALFORMED_JSON2,
    MALFORMED_JSON3,
    MALFORMED_JSON4,
    MALFORMED_JSON5,
    MALFORMED_JSON6,
    MALFORMED_JSON7,
    MALFORMED_JSON8,
    MALFORMED_JSON9,
    MALFORMED_JSON10,
    MALFORMED_JSON11,
    MALFORMED_JSON12,
    MALFORMED_JSON13
]

console = Console()
table = Table(
    title="JSON Parsing Test Results",
    show_header=True,
    header_style="bold magenta",
    show_lines=True  # Add lines between rows
)
table.add_column("Case #", justify="right", width=8)
table.add_column("Raw Input", style="cyan", no_wrap=False, max_width=40)
table.add_column("Structured Output", style="green", no_wrap=False, max_width=40)

for i, json_string in enumerate(malformed_jsons):
    raw_display = json_string.strip().replace('\n', ' ↵ ')
    structured_output_raw = to_json_string(json_string).strip()
      
    # Pretty-print the structured_output
    try:
        # Parse the JSON string and reformat it with indentation
        structured_output = json.dumps(json.loads(structured_output_raw), indent=2)
    except json.JSONDecodeError:
        # Fallback if the JSON is invalid
        structured_output = structured_output_raw
    
    table.add_row(
        str(i + 1),
        f"{raw_display}",
        f"{structured_output}"
    )

console.print(table)


# ❯ uv run hello.py
#                                     JSON Parsing Test Results                                     
# ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃   Case # ┃ Raw Input                                ┃ Structured Output                        ┃
# ┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │        1 │ {abhi: shek}                             │ {                                        │
# │          │                                          │   "abhi": "shek"                         │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        2 │ {abhi: "shek"}                           │ {                                        │
# │          │                                          │   "abhi": "shek"                         │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        3 │ {'name': 'value',}                       │ {                                        │
# │          │                                          │   "name": "value"                        │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        4 │ {'name': 'value'                         │ {                                        │
# │          │                                          │   "name": "value"                        │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        5 │ {'name': 'value'',}                      │ {                                        │
# │          │                                          │   "name": "value'"                       │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        6 │ {'name': 'value''                        │ {                                        │
# │          │                                          │   "name": "value'"                       │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        7 │ {'name': value'}                         │ {                                        │
# │          │                                          │   "name": "value'"                       │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        8 │ {'name': value'                          │ {                                        │
# │          │                                          │   "name": "value'"                       │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │        9 │ {'name': "value"}                        │ {                                        │
# │          │                                          │   "name": "value"                        │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │       10 │ {'name': "value'                         │ {                                        │
# │          │                                          │   "name": "value'\n"                     │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │       11 │ {'name': value}                          │ {                                        │
# │          │                                          │   "name": "value"                        │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │       12 │ {name: "value"}                          │ {                                        │
# │          │                                          │   "name": "value"                        │
# │          │                                          │ }                                        │
# ├──────────┼──────────────────────────────────────────┼──────────────────────────────────────────┤
# │       13 │ { rec_one: "and then i said \"hi\", and  │ {                                        │
# │          │ also \"bye\"", rec_two: "and then i said │   "also_rec_one": "ok",                  │
# │          │ "hi", and also "bye"", "also_rec_one":   │   "rec_one": "and then i said \"hi\",    │
# │          │ ok }                                     │ and also \"bye\"",                       │
# │          │                                          │   "rec_two": "and then i said \"hi\",    │
# │          │                                          │ and also \"bye\""                        │
# │          │                                          │ }                                        │
# └──────────┴──────────────────────────────────────────┴──────────────────────────────────────────┘