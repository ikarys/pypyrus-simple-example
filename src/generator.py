import os
from jinja2 import Environment, FileSystemLoader

def render_folder_name(folder_name, variables):
    return Environment().from_string(folder_name).render(variables)

def render_file(file_path, variables):
    with open(file_path, 'r') as file:
        content = file.read()
    template_dir = os.path.dirname(file_path)
    loader = FileSystemLoader(template_dir)
    env = Environment(loader=loader)
    template = env.get_template(os.path.basename(file_path))
    return template.render(variables)

def process_folder(source_folder, target_folder, variables):
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        target_path = os.path.join(target_folder, render_folder_name(relative_path, variables))

        # Create the target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)

        # Process files in the current directory and its subdirectories
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_path, file)

            # Render the Jinja2 template with variables
            rendered_content = render_file(source_file_path, variables)

            # Write the rendered content to the target file
            with open(target_file_path, 'w') as target_file:
                target_file.write(rendered_content)
