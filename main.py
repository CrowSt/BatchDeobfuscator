class Deobfuscator:
    def __init__(self, filename: str, with_save: bool = True, save_sets: bool = False):
        self.file = open(filename)
        self.deob_file = open(filename + '.deob', 'w')
        self.obf_strings = {}
        self.with_save = with_save
        self.save_sets = save_sets

    def parse_file(self):
        line = self.file.readline()
        while line:
            string = self.parse_line(self.deobfuscate_line(line))
            if string.startswith(('set', '@set')):
                if self.save_sets:
                    print(string, end='')

                    if self.with_save:
                        self.deob_file.write(string)

            elif not string.isspace():
                print(string, end='')
                if self.with_save:
                    self.deob_file.write(string)

            line = self.file.readline()

    def deobfuscate_line(self, line):
        deobfuscated_string = ''
        key_name = False
        key_name_string = ''

        for symbol in line:
            if symbol == '%':
                key_name = not key_name
                if key_name:
                    key_name_string = ''
                else:
                    # in this context it IS "set=something" and I don't know if it is possible to use otherwise
                    if ':' in key_name_string and key_name_string.endswith('='):
                        key, pattern = key_name_string.split(':')
                        key = self.obf_strings.get(key, None)
                        if key is None:  # just if it is a null string or a bug
                            return ''
                        key = key.replace(pattern[:-1], '')  # set

                        deobfuscated_string += key
                        if key != 'set ':  # JUST IF POSSIBLE
                            input(('what??', key, pattern))
                        continue

                    if key_name_string == 'systemdrive':
                        deobfuscated_string += '%systemdrive%'
                        continue

                    value = self.obf_strings.get(key_name_string, None)
                    if value is not None:
                        deobfuscated_string += value
                    # else it is a null string
                continue

            if key_name:
                if key_name_string == '' and symbol == '~':
                    key_name = not key_name
                    deobfuscated_string += '%~'
                    continue
                key_name_string += symbol
            else:
                deobfuscated_string += symbol

        return deobfuscated_string

    def parse_line(self, line: str):
        if line.startswith(('@set', 'set')):
            temp_line = line.split(' ', 1)[1]
            if '"' in line:
                temp_line = temp_line[1:-2]

            key, value = temp_line.split('=', 1)

            self.obf_strings[key] = value

        return line


Deobfuscator("FoliaDupe.bat").parse_file()
