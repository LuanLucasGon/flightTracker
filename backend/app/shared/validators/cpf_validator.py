def is_valid_cpf(cpf: str) -> bool:
    digits = "".join(filter(str.isdigit, cpf))

    if len(digits) != 11:
        return False

    if len(set(digits)) == 1:
        return False

    total = sum(int(digits[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    first = 0 if remainder < 2 else 11 - remainder
    if first != int(digits[9]):
        return False

    total = sum(int(digits[i]) * (11 - i) for i in range(10))
    remainder = total % 11
    second = 0 if remainder < 2 else 11 - remainder
    if second != int(digits[10]):
        return False

    return True