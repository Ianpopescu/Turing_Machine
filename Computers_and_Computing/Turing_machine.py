"""
M3L110: Computers and Computing
Project 1 – Binary Addition Turing Machine
Author: Ian Popescu
Date: October 2025

This Python program simulates a single-tape Turing Machine
that performs binary addition of two numbers written in
little-endian form (least significant bit on the right),
separated by a '+' symbol. Example: "1010+101"
represents (0101 + 101) in standard binary notation.
"""

class TuringMachine:
    def __init__(self, tape, blank='+', start_state='q0', halt_state='qhalt'):
        """
        Initialize the Turing Machine.

        Parameters:
        - tape: the input string, e.g. "1010+101"
        - blank: the blank symbol used for padding (default '+')
        - start_state: initial state (default 'q0')
        - halt_state: halting state (default 'qhalt')
        """
        self.tape = [blank] * 10 + list(tape) + [blank] * 10
        self.blank = blank
        self.head = 10            # Head starts on the first symbol of the input
        self.state = start_state  # Current state
        self.halt_state = halt_state

    def step(self, transitions):
        """
        Execute one transition step based on the current state and symbol.
        """
        key = (self.state, self.tape[self.head])

        # If no transition is defined for (state, symbol), halt the machine and tell what transition is missing
        if key not in transitions:
            print(f"No transition for {key}, halting.")
            self.state = self.halt_state
            return

        # Fetch next state, symbol to write, and movement direction
        next_state, write, move = transitions[key]

        # Write the new symbol on the tape
        self.tape[self.head] = write

        # Move the head left or right
        if move == 'R':
            self.head += 1
        elif move == 'L':
            self.head -= 1

        # Update the current state
        self.state = next_state

    def run(self, transitions):
        """
        Run the Turing Machine until it reaches the halt state.
        Returns the final tape content as a string (without blanks).
        """
        while self.state != self.halt_state:
            self.step(transitions)
        else:
            # Return the resulting tape without blank padding
            return ''.join(self.tape).strip(self.blank)


# --- Transition rules ---
# Each key is (state, symbol_read)
# Each value is (next_state, symbol_to_write, move_direction)
# Movement direction: 'L' = left, 'R' = right

transitions = {
    # q0: move right through the first binary number until reaching '+'
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '+'): ('q1', '+', 'R'),

    # q1: move through the second number until the end (blank)
    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '+'): ('q2', '+', 'L'),

    # q2: perform addition (no carry / carry handling begins)
    ('q2', '0'): ('q2', '1', 'L'),   # write 1 if 0+1 or carry
    ('q2', '1'): ('q3', '0', 'L'),   # carry generated
    ('q2', '+'): ('q5', '+', 'R'),   # reached separator, go to cleanup

    # q3: propagate carry to the left
    ('q3', '0'): ('q3', '0', 'L'),
    ('q3', '1'): ('q3', '1', 'L'),
    ('q3', '+'): ('q4', '+', 'L'),

    # q4: handle final carry back into first number
    ('q4', '0'): ('q0', '1', 'R'),   # write carry 1
    ('q4', '1'): ('q4', '0', 'L'),   # continue carry
    ('q4', '+'): ('q0', '1', 'R'),   # add carry at left boundary

    # q5: cleanup phase, replace 1s with 0s as part of final output
    ('q5', '1'): ('q5', '0', 'R'),
    ('q5', '+'): ('qclean', '+', 'L'),

    # qclean: remove extra '+' symbols and finalize
    ('qclean', '0'): ('qclean', '+', 'L'),
    ('qclean', '+'): ('qhalt', '+', 'L')
}


# --- Run the machine ---
tm = TuringMachine("1010+101")
result = tm.run(transitions)
print("Result:", result)
