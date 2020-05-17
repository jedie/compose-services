from pathlib import Path

from bundlewrap.secrets import FILENAME_SECRETS, generate_initial_secrets_cfg

if __name__ == "__main__":
    file_path = Path(FILENAME_SECRETS)
    if file_path.is_file():
        print(f'File exists: {file_path.name}, ok.')
    else:
        with file_path.open('w') as f:
            f.write(
                generate_initial_secrets_cfg()
            )
        print(f'File {file_path.name} created, ok.')
