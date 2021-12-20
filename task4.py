import sys
import secrets
import hashlib
import hmac


class HMACstep:
    def __init__(self, step):
        self.step = step
        self.key = secrets.token_hex(32)

    def hmac_step(self):
        hmac_hash = hmac.new(self.key.encode(), self.step.encode(), hashlib.sha3_256)
        return hmac_hash.hexdigest()


class Table:
    def __init__(self, list_steps):
        self.list_steps = list_steps

    def win_indexes_element(self, index_element):
        result = []
        for i in range(int((len(self.list_steps) - 1)/2)):
            i += 1
            if index_element + i <= len(self.list_steps) - 1:
                result.append(index_element + i)
            else:
                result.append(index_element + i - len(self.list_steps))
        return result

    def convert_index_to_string(self, list_steps, index):
        indexes = self.win_indexes_element(index)
        string_all_elements = ""
        for i in indexes:
            string_all_elements += "/" + list_steps[i]
        return string_all_elements[1:]

    def print_all_string_table_win(self):

        for index, value in enumerate(self.list_steps):
            print(f"{self.list_steps[index]} - {self.convert_index_to_string(self.list_steps, index)}")


class MenuUser:
    dict_elements = {}
    def __init__(self, list_steps):
        self.list_steps = list_steps
        self._dict_items()
        self.dict_elements[0] = 'exit'

    def _dict_items(self):
        list_items = list(self.list_steps)
        list_items.append('help')
        self.dict_elements = {key: value for key, value in zip(range(1,len(list_items) + 1), list_items)}

    def print_menu(self):
        elements = self.dict_elements
        print("Available moves:")
        for key, value in elements.items():
            print(f"{key} {value}")

    def input_user(self):
        try:
            integer = int(input('Enter your move:'))
        except ValueError:
            print("----Not a number entered, please enter a number from the list")
            self.input_user()
        list_key = list(self.dict_elements.keys())
        if integer in list_key:
            if integer == 0:
                exit()
            print("Your move:" + self.dict_elements[integer])
            return self.dict_elements[integer]
        else:
            self.print_menu()
            self.input_user()

class ValidatorWin:
    def __init__(self, index_step_user, index_step_pc, table_win):
        self.user = index_step_user
        self.pc = index_step_pc
        self.table = table_win

    def valid_win(self):
        list_index_win_user = self.table.win_indexes_element(self.user)
        if self.pc in list_index_win_user:
            print("You Win")
        elif self.pc == self.user:
            print("Draw")
        else:
            print("You lost")


def validator(steps_valid):
    set_number = len(set(steps_valid))
    number_of_steps = len(steps_valid)
    if number_of_steps < 3:
        print("""--The number of moves must be more than 3
        Example:
        python task4.py step1 step2 step3 step4 step5
        python task4.py step1 step2 step3""")
        return False
    elif number_of_steps % 2 == 0:
        print("""--The number of steps must be odd.
        Example:
        python task4.py step1 step2 step3 step4 step5
        python task4.py step1 step2 step3""")
        return False
    elif number_of_steps != set_number:
        print("--Step names must be unique")
        return False
    else:
        return True


def step_computer(steps_all):
    number_of_steps = len(steps_all) - 1
    random_class = secrets.SystemRandom()
    index = random_class.randint(0, number_of_steps)
    name_step = steps_all[index]
    return name_step


moves = list(sys.argv)[1:]
if validator(moves):
    step_pc = step_computer(moves)
    pc_hmac = HMACstep(step_pc)
    print("HMAC:\n" + pc_hmac.hmac_step())
    menu = MenuUser(moves)
    menu.print_menu()
    step_user = menu.input_user()
    table = Table(moves)
    if step_user == 'help':
        table.print_all_string_table_win()
        step_user = menu.input_user()
    elif step_user == 'exit':
        exit()
    win_result = ValidatorWin(moves.index(step_user), moves.index(step_pc), table)
    print("Computer move:" + step_pc)
    win_result.valid_win()
    print("HMAC key:\n" + pc_hmac.key)
else:
    exit()













