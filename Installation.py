import sys
import subprocess

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of packages to install
packages = [
    "boto3",
    "sagemaker",
    "amazon-textract-caller",
    "amazon-textract-prettyprinter==0.1.10",
    "amazon-textract-response-parser<0.2,>=0.1",
    "docutils>=0.20,<0.22",
]

# Install each package
for package in packages:
    print(f"Installing {package}...")
    install_package(package)

print("All packages installed successfully.")