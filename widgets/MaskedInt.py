class MaskedInt:
    @staticmethod
    def max_length(value, type_action):
        if int(type_action) == 1:
            if len(value) <= 3:
                return True
            else:
                return False
        return True

    def mask_number(self, char, value, type_action) -> bool:
        if char.isdigit():
            return self.max_length(value, type_action)
        elif char == "":
            return True
        return False
