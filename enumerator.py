import sys

# DSL components
TERMINALS = ["x", "y", "0", "1", "2"]
OPERATORS = ["+", "-", "*"]


def evaluate_polish(tokens, env):
    """
    Evaluates a Polish notation token list given an environment dict
    (e.g., {'x': 1, 'y': 2}). Evaluates right-to-left using a stack.
    """
    stack = []

    for token in reversed(tokens):
        if token == "x":
            stack.append(env["x"])
        elif token == "y":
            stack.append(env["y"])
        elif token in ("0", "1", "2"):
            stack.append(int(token))
        elif token in OPERATORS:
            if len(stack) < 2:
                return None  # Invalid expression

            a = stack.pop()
            b = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)

    return stack[0] if len(stack) == 1 else None


class EnumerativeSynthesizer:
    def __init__(self):
        self.memo = {}

    def get_programs_of_size(self, size):
        """Generates all valid token lists"""
        if size in self.memo:
            return self.memo[size]

        if size < 1:
            return []

        # Base case: Size 1 programs are atomic terminals
        if size == 1:
            res = [[t] for t in TERMINALS]
            self.memo[1] = res
            return res

        # Recursive case
        programs = []

        for s1 in range(1, size - 1):
            s2 = size - 1 - s1
            left_exprs = self.get_programs_of_size(s1)
            right_exprs = self.get_programs_of_size(s2)

            for op in OPERATORS:
                for e1 in left_exprs:
                    for e2 in right_exprs:
                        programs.append([op] + e1 + e2)

        self.memo[size] = programs
        return programs

    def synthesize(self, examples):
        """
        Enumerates programs by size and returns first valid program
        examples: list of tuples [(i1, i2, o1), ...]
        """
        size = 1

        while True:
            candidates = self.get_programs_of_size(size)

            for prog in candidates:
                # Check whether the candidate satisfies all examples
                match = True

                for i1, i2, expected_o1 in examples:
                    env = {"x": i1, "y": i2}
                    res = evaluate_polish(prog, env)

                    if res != expected_o1:
                        match = False
                        break

                if match:
                    return " ".join(prog)

            size += 1
