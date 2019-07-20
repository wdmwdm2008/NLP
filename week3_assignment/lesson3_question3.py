def parse_edit_solution(string1, string2):
    if string1 == "" and string2 == "":
        return []
    if len(solution[(string1, string2)]) == 0 or solution[(string1, string2)].startswith("SUB"):
        return [solution[(string1, string2)]] + parse_edit_solution(string1[:-1], string2[:-1])
    elif solution[(string1, string2)].startswith("ADD"):
        return [solution[(string1, string2)]] + parse_edit_solution(string1, string2[:-1])
    elif solution[(string1, string2)].startswith("DEL"):
        return [solution[(string1, string2)]] + parse_edit_solution(string1[:-1], string2)