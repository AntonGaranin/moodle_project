import pytest
from ..main import encrypt_password, decrypt_password
from ..main import cipher  # Импортируем объект шифрования


def test_encrypt_decrypt_roundtrip():
    """Тест, что шифрование и дешифрование работают согласованно"""
    original_password = "my_super_secret_password123"

    encrypted = encrypt_password(original_password)
    decrypted = decrypt_password(encrypted)

    assert decrypted == original_password
    assert encrypted != original_password  # Зашифрованная версия должна отличаться


def test_encrypt_different_outputs():
    """Тест, что повторное шифрование того же пароля даёт разные результаты"""
    password = "same_password"

    encrypted1 = encrypt_password(password)
    encrypted2 = encrypt_password(password)

    assert encrypted1 != encrypted2  # Из-за случайного salt/IV


def test_decrypt_invalid_input():
    """Тест обработки некорректных данных при дешифровании"""
    with pytest.raises(Exception):  # Конкретное исключение зависит от вашей crypto-библиотеки
        decrypt_password("invalid_encrypted_data")


def test_empty_password():
    """Тест обработки пустого пароля"""
    empty_pwd = ""

    encrypted = encrypt_password(empty_pwd)
    decrypted = decrypt_password(encrypted)

    assert decrypted == empty_pwd


@pytest.mark.parametrize("password", [
    "short",
    "very_long_password_" * 50,
    "special_chars_!@#$%^&*()",
    "unicode_🔑_пароль"
])
def test_various_password_formats(password):
    """Тест различных форматов паролей"""
    encrypted = encrypt_password(password)
    decrypted = decrypt_password(encrypted)

    assert decrypted == password