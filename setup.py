import os
import subprocess
import sys
import venv

def is_venv_active(env_name=".venv"):
	"""Check if the virtual environment is already active."""
	python_executable = os.path.join(env_name, "bin", "python") if os.name != "nt" else os.path.join(env_name, "Scripts", "python.exe")
	return os.path.exists(python_executable)

def are_dependencies_installed(env_name=".venv"):
	"""Check if pytest (or another core dependency) is installed."""
	python_executable = os.path.join(env_name, "bin", "python") if os.name != "nt" else os.path.join(env_name, "Scripts", "python.exe")
	try:
		subprocess.run([python_executable, "-m", "pytest", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		return True
	except (subprocess.CalledProcessError, FileNotFoundError):
		return False

def create_virtualenv(env_name=".venv"):
	"""Create a virtual environment."""
	if is_venv_active(env_name):
		print(f"Virtual environment '{env_name}' already exists.")
		return

	print(f"Creating virtual environment '{env_name}'...")
	venv.create(env_name, with_pip=True)
	print(f"Virtual environment '{env_name}' created.")

def install_dependencies(env_name=".venv", requirements_file="requirements.txt"):
	"""Install dependencies in the virtual environment."""
	if are_dependencies_installed(env_name):
		print("Dependencies already installed. Skipping installation.")
		return

	python_executable = os.path.join(env_name, "bin", "python") if os.name != "nt" else os.path.join(env_name, "Scripts", "python.exe")

	# Upgrade pip
	subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

	# Install dependencies
	if os.path.exists(requirements_file):
		print(f"Installing dependencies from '{requirements_file}'...")
		subprocess.run([python_executable, "-m", "pip", "install", "-r", requirements_file], check=True)
	else:
		print(f"No '{requirements_file}' file found. Skipping dependency installation.")

def main():
	"""Main script to set up the environment."""
	env_name = ".venv"
	requirements_file = "requirements.txt"

	create_virtualenv(env_name)
	install_dependencies(env_name, requirements_file)

	activate_command = (
		f"source {env_name}/bin/activate" if os.name != "nt" else f"{env_name}\\Scripts\\activate"
	)
	print(f"Setup complete. To activate the virtual environment, run:\n\n{activate_command}\n")

if __name__ == "__main__":
	main()