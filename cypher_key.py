import subprocess
import os
from cryptography.fernet import Fernet

def is_env_var_set(var_name):
    # Проверяем в текущем окружении
    if os.getenv(var_name):
        return True
    # Проверяем в ~/.bashrc, ~/.zshrc и т.д.
    config_files = [".bashrc", ".bash_profile", ".zshrc", ".profile"]
    for file in config_files:
        file_path = os.path.expanduser(f"~/{file}")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                if f"export {var_name}=" in f.read():
                    return True
    return False

if not is_env_var_set("ENCRYPTION_KEY"):
    key = Fernet.generate_key().decode()
    # Добавляем в ~/.bashrc (или другой конфиг)
    with open(os.path.expanduser("~/.bashrc"), "a") as f:
        f.write(f'\nexport ENCRYPTION_KEY="{key}"\n')
    # Обновляем текущую сессию
    subprocess.run(f'export ENCRYPTION_KEY="{key}"', shell=True, check=True)
    print("Ключ сохранён в ~/.bashrc и текущей сессии:", key)
else:
    print("Ключ уже существует:", os.getenv("ENCRYPTION_KEY"))