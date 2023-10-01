import re
from typing import Any


def add_error(field_name: str, msg: str, errors: dict) -> bool:
    if errors.get(field_name) is None:
        errors[field_name] = []
    errors[field_name].append(msg)


def is_in_range(
    field_value: int | float,
    field_name: str,
    low: int | float,
    high: int | float,
    errors: dict,
) -> bool:
    if low <= field_value <= high:
        return True
    else:
        add_error(
            field_name, f"O valor deste campo deve estar entre {low} e {high}.", errors
        )
        return False


def is_not_none(field_value: Any, field_name: str, errors: dict) -> bool:
    if field_value is not None:
        return True
    else:
        add_error(field_name, f"O valor deste campo não pode ser nulo.", errors)
        return False


def is_not_empty(field_value: str, field_name: str, errors: dict) -> bool:
    if field_value.strip() != "":
        return True
    else:
        add_error(field_name, f"O valor deste campo não pode ser vazio.", errors)
        return False


def is_size_between(
    field_value: str, field_name: str, min_size: int, max_size: int, errors: dict
) -> bool:
    if min_size <= len(field_value) <= max_size:
        return True
    else:
        add_error(
            field_name,
            f"Este campo deve ter entre {min_size} e {max_size} caracteres.",
            errors,
        )
        return False


def is_max_size(field_value: str, field_name: str, max_size: int, errors: dict) -> bool:
    if len(field_value) <= max_size:
        return True
    else:
        add_error(
            field_name, f"Este campo deve ter no máximo {max_size} caracteres.", errors
        )
        return False


def is_min_size(field_value: str, field_name: str, min_size: int, errors: dict) -> bool:
    if len(field_value) >= min_size:
        return True
    else:
        add_error(
            field_name, f"Este campo deve ter no mínimo {min_size} caracteres.", errors
        )
        return False


def is_matching_regex(
    field_value: str, field_name: str, regex: str, errors: dict
) -> bool:
    if re.match(regex, field_value) is not None:
        return True
    else:
        add_error(
            field_name, "O valor deste campo está com o formato incorreto.", errors
        )
        return False


def is_email(field_value: str, field_name: str, errors: dict) -> bool:
    if (
        re.match(
            r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
            field_value,
        )
        is not None
    ):
        return True
    else:
        add_error(
            field_name,
            "O valor deste campo deve ser um e-mail com formato válido.",
            errors,
        )
        return False


def is_cpf(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", field_value) is not None:
        return True
    else:
        add_error(field_name, "O valor deste campo deve ser um CPF válido.", errors)
        return False


def is_cnpj(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$", field_value) is not None:
        return True
    else:
        add_error(field_name, "O valor deste campo deve ser um CNPJ válido.", errors)
        return False


def is_phone_number(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^\(\d{2}\)\d{4,5}-\d{4}$", field_value) is not None:
        return True
    else:
        add_error(
            field_name, "O valor deste campo deve ser um telefone válido.", errors
        )
        return False


def is_cep(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^\d{5}-\d{3}$", field_value) is not None:
        return True
    else:
        add_error(field_name, "O valor deste campo deve ser um CEP válido.", errors)
        return False


def is_person_name(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^[a-zA-ZÀ-ú']{2,40}$", field_value) is not None:
        return True
    else:
        add_error(field_name, "O valor deste campo deve ser um nome válido.", errors)
        return False


def is_person_fullname(field_value: str, field_name: str, errors: dict) -> bool:
    if (
        re.match(r"^[a-zA-ZÀ-ú']{2,40}(?:\s[a-zA-ZÀ-ú']{2,40})+$", field_value)
        is not None
    ):
        return True
    else:
        add_error(
            field_name, "O valor deste campo deve ser um nome completo válido.", errors
        )
        return False


def is_project_name(field_value: str, field_name: str, errors: dict) -> bool:
    if re.match(r"^[\w]+(\s[\w]+)*$", field_value) is not None:
        return True
    else:
        add_error(field_name, "O valor deste campo deve ser um nome válido.", errors)
        return False


def is_password(field_value: str, field_name: str, errors: dict) -> bool:
    """
    Tenha pelo menos um caractere minúsculo.
    Tenha pelo menos um caractere maiúsculo.
    Tenha pelo menos um dígito.
    Tenha pelo menos um caractere especial dentre os especificados (@$!%*?&).
    Tenha um comprimento de pelo menos 4 e no máximo 64 caracteres.
    """
    if (
        re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,64}$",
            field_value,
        )
        is not None
    ):
        return True
    else:
        add_error(
            field_name,
            "O valor deste campo deve ser uma senha válida entre 4 e 64 caracteres, contendo caracteres maiúsculos, minúsculos, dígitos e caracteres especiais (@$!%*?&).",
            errors,
        )
        return False


def is_matching_fields(
    field_value: str,
    field_name: str,
    matching_field_value: str,
    matching_field_name: str,
    errors: dict,
) -> bool:
    if field_value.strip() == matching_field_value.strip():
        return True
    else:
        add_error(
            field_name,
            f"O valor deste campo deve ser igual ao do campo {matching_field_name}.",
            errors,
        )
        return False


def is_greater_than(
    field_value: int | float, field_name: str, value: int | float, errors: dict
) -> bool:
    if field_value > value:
        return True
    else:
        add_error(
            field_name, f"O valor deste campo deve ser maior que {value}.", errors
        )
        return False


def is_selected_id_valid(field_value: int, field_name: str, errors: dict) -> bool:
    if field_value > 0:
        return True
    else:
        add_error(field_name, f"Selecione uma opção para este campo.", errors)
        return False


def is_less_than(
    field_value: int | float, field_name: str, value: int | float, errors: dict
) -> bool:
    if field_value < value:
        return True
    else:
        add_error(
            field_name, f"O valor deste campo deve ser menor que {value}.", errors
        )
        return False


def is_greater_than_or_equal(
    field_value: int | float, field_name: str, value: int | float, errors: dict
) -> bool:
    if field_value >= value:
        return True
    else:
        add_error(
            field_name,
            f"O valor deste campo deve ser maior ou igual a {value}.",
            errors,
        )
        return False


def is_less_than_or_equal(
    field_value: int | float, field_name: str, value: int | float, errors: dict
) -> bool:
    if field_value <= value:
        return True
    else:
        add_error(
            field_name,
            f"O valor deste campo deve ser menor ou igual a {value}.",
            errors,
        )
        return False
