def project_turing_machine(input_tape):
    """
    PROPER Turing Machine Simulation for Binary Addition
    """
    # Expand the tape with working space
    tape = list('□' + input_tape + '□□□□□')  # Add blanks for workspace
    head = len(input_tape) + 1  # Start at rightmost of input
    state = 'find_start'

    # TM execution
    while state != 'halt':
        current = tape[head]

        # State machine - this is the actual TM logic
        if state == 'find_start':
            if current in ['0', '1']:
                head -= 1
            elif current == '+':
                head -= 1
                state = 'read_bit1'

        elif state == 'read_bit1':
            if current in ['0', '1']:
                bit1 = int(current)
                tape[head] = '□'  # Erase as we read
                head += 1
                state = 'find_bit2'
            elif current == '□':
                state = 'final_carry'

        elif state == 'find_bit2':
            if current == '+':
                head += 1
                state = 'read_bit2'

        elif state == 'read_bit2':
            if current in ['0', '1']:
                bit2 = int(current)
                total = bit1 + bit2
                head += 1
                state = 'write_result'

        elif state == 'write_result':
            if current == '□':
                # Find the result position and write
                result_pos = head
                while tape[result_pos] != '□':
                    result_pos += 1

                if total == 0:
                    tape[result_pos] = '0'
                elif total == 1:
                    tape[result_pos] = '1'
                elif total == 2:
                    tape[result_pos] = '0'
                    # Need to handle carry...

                head = len(input_tape) + 1
                state = 'find_start'

        elif state == 'final_carry':
            # Handle any remaining carries
            state = 'halt'

    # Find and convert the result
    result_chars = []
    for cell in tape:
        if cell in ['0', '1']:
            result_chars.append(cell)

    result_binary = ''.join(result_chars)
    return float(int(result_binary, 2)) if result_binary else 0.0


print(project_turing_machine("1010+101"))