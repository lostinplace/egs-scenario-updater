from lib.simple_rule import SimpleRule


def capitalize_struct_bool(node:dict):
    value = node.get("Struct")
    if isinstance(value, bool):
        out = "True" if value else "False"
    else:
        out = value.capitalize()

    node["Struct"] = out
    return node


def generate_struct_capitalization_rule():
    conditions = [lambda node: isinstance(node, dict) and "Struct" in node]
    effects = [capitalize_struct_bool]
    return SimpleRule(conditions, effects)

