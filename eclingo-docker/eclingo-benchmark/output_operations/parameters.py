# solver name to command mapping
solver_commands = {
    "eclingo-old": "eclingo",
    "ezsmt-z3-idl": "ezsmt -V 0 -s z3 -l 3",
    "ezsmt-yices-idl": "ezsmt -V 0 -s yices -l 3",
    "ezsmt-cvc5-idl": "ezsmt -V 0 -s cvc5 -l 3",
}

# line index for answer set on output file
answer_line_indices = {
    "eclingo-old": 3,
    "ezsmt": 1,
    "clingcon": 4,
    "clingo": 4,
    "clingo-dl": 4,
    "ezsmt-z3-idl": 1,
    "ezsmt-yices-idl": 1,
    "ezsmt-cvc5-idl": 1,
}

# separator for atoms in answer set
delimiters = {
    "eclingo-old": "&",
}

# prefix for answer set
answer_line_prefixes = {
    "ezsmt": "Answer 1:"
}

# index for given word and its relative position from answer set
relative_indices = {
    "eclingo": ("World view", 1)
}