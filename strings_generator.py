class rules():
    rules = dict()
    def add_rule(self, key, value):
        self.rules[key] = value
    def apply_rules(self, char):
        return self.rules[char]

def generate_sequence(rules, string, accum):
    if(len(string) == 0):
        return accum
    return generate_sequence(rules, string[1:], accum + rules.apply_rules(string[0]))

def generate_pattern(rules, string, n):
    if(n <= 0):
        return string
    return generate_pattern(rules, generate_sequence(rules, string, ""), n-1)

rules = rules()
rules.add_rule("A", "ABC")
rules.add_rule("B", "BB")
rules.add_rule("C", "A")
print(generate_pattern(rules, "AAA", 3))


