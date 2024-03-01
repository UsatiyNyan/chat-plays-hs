import subprocess
from pathlib import Path


def rcc(input_file, output_file):
    command = f'pyside6-rcc {input_file} -o {output_file}'
    subprocess.run(command, shell=True, check=True)


def main():
    app_dir = Path(__file__).resolve().parent
    frontend_dir = app_dir / 'Frontend'
    rcc(frontend_dir / 'app.qrc', app_dir / 'app_rc.py')
    rcc(frontend_dir / 'resources.qrc', app_dir / 'resources_rc.py')


if __name__ == '__main__':
    main()
