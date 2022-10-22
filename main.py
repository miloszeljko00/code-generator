from models import *
from jinja2 import Template
import os
import yaml

def generate_model():
    exists = os.path.exists(current_directory + "\\model\\")
    if not exists:
        os.makedirs("model")

    model_file = open(current_directory + "\\model\\" + data["class"]["name"] + ".cs", "w")

    j2_template = Template(model_template)
    model_file.write(j2_template.render(data))

    model_file.close()


def generate_repository():
    exists = os.path.exists(current_directory + "\\repository\\")
    if not exists:
        os.makedirs("repository")

    repository_interface_file = open(current_directory + "\\repository\\I" + data["class"]["name"]+"Repository.cs", "w")

    j2_template = Template(repository_interface_template)
    repository_interface_file.write(j2_template.render(data))

    repository_interface_file.close()

    repository_file = open(current_directory + "\\repository\\" + data["class"]["name"] + "Repository.cs", "w")

    j2_template = Template(repository_template)
    repository_file.write(j2_template.render(data))

    repository_file.close()


def generate_service():
    exists = os.path.exists(current_directory + "\\service\\")
    if not exists:
        os.makedirs("service")

    repository_interface_file = open(current_directory + "\\service\\I" + data["class"]["name"]+"Service.cs", "w")

    j2_template = Template(service_interface_template)
    repository_interface_file.write(j2_template.render(data))

    repository_interface_file.close()

    repository_file = open(current_directory + "\\service\\" + data["class"]["name"] + "Service.cs", "w")

    j2_template = Template(service_template)
    repository_file.write(j2_template.render(data))

    repository_file.close()


def generate_controller():
    exists = os.path.exists(current_directory + "\\controller\\")
    if not exists:
        os.makedirs("controller")

    controller_file = open(current_directory + "\\controller\\" + data["class"]["name"] + "Controller.cs", "w")

    j2_template = Template(controller_template)
    controller_file.write(j2_template.render(data))

    controller_file.close()


def load_data():
    global data
    with open(current_directory + '\\data.yaml') as data_file:
        return yaml.load(data_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    current_directory = os.getcwd()

    try:
        print("Loading data.yaml...")
        data = load_data()
        print(data['language'])
        print("Generating model...")
        generate_model()
        print("Generating repository...")
        generate_repository()
        print("Generating service...")
        generate_service()
        print("Generating controller...")
        generate_controller()
    except Exception as e:
        print("Something else went wrong :(")
        print("\n\nERORR:\n")
        print(e)
