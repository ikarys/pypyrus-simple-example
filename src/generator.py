import os
from typing import Union

from jinja2 import Environment, FileSystemLoader

from jinja2_filters import PypyrusFilters


def configure_jinja_environment(template_dir: Union[str, None] = None) -> Environment:
    env = Environment()
    if template_dir is not None:
        env = Environment(loader=FileSystemLoader(template_dir))
    env.filters.update({"slug": PypyrusFilters.slug})
    return env


def render_folder_name(folder_name, variables):
    return configure_jinja_environment().from_string(folder_name).render(variables)


def render_file(file_path, variables):
    with open(file_path, "r") as file:
        content = file.read()
    template_dir = os.path.dirname(file_path)
    template = configure_jinja_environment(template_dir).get_template(os.path.basename(file_path))
    return template.render(variables)


def process_folder(source_folder, target_folder, variables):
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        target_path = os.path.join(target_folder, render_folder_name(relative_path, variables))

        # Create the target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)

        # Process files in the current directory and its subdirectories
        for file in files:
            if file == "pypyrus.yaml":
                continue
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_path, file)

            # Render the Jinja2 template with variables
            rendered_content = render_file(source_file_path, variables)

            # Write the rendered content to the target file
            with open(target_file_path, "w") as target_file:
                target_file.write(rendered_content)
