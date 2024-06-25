import subprocess
import sys

# List of required packages
required_packages = [
    'beautifulsoup4',
    'requests',
    'pyfiglet',
    'termcolor'
]


def install_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages([pkg.split('==')[0] for pkg in required_packages])