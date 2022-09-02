class MaskedEntry:
    @staticmethod
    def limit_max_length(value, type_action, max_length):
        if int(type_action) == 1:
            if len(value) <= max_length:
                return True
            return False
        return True

    def mask_number(self, char, value, type_action, max_length) -> bool:
        if char.isdigit():
            return self.limit_max_length(value, type_action, int(max_length))
        elif char == "":
            return True
        return False

    def mask_entry(self, value, type_action, max_length) -> bool:
        return self.limit_max_length(value, type_action, int(max_length))

