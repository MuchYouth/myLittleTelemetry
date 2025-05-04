
import os
import subprocess
import sys
import yaml

def run_compose(yaml_path):
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    project_dir = os.path.dirname(yaml_path)
    subprocess.run(["docker-compose", "-f", yaml_path, "up", "-d"], cwd=project_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_yaml.py <docker-compose.yml>")
    else:
        run_compose(sys.argv[1])
