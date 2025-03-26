from cryptography.fernet import Fernet
import subprocess
import os
key = Fernet.generate_key()
subprocess.run(["export", f'ENCRYPTION_KEY="{key}"'])
value = os.getenv("ENCRYPTION_KEY")
if value is not None:
    pass
else:
    key = Fernet.generate_key()
    subprocess.run(["export", f'ENCRYPTION_KEY="{key}"'])