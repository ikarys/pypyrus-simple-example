# Pypyrus simple example

## Overview

This repository serves as a simple example showcasing the capabilities of Pypyrus, a powerful file generation tool. In this example, Pypyrus is utilized to create an ArgoCD application along with an Nginx deployment document.


## Usage

### Prerequisites

Ensure you have Pypyrus installed. If not, you can install it using:

```bash
pip install pypyrus
```

### Running Pypyrus
```bash
pypyrus -u https://github.com/ikarys/pypyrus-simple-example -t my_folder
```

Follow the prompts and provide the requested information:
* application_name: Enter the name for the ArgoCD application.
* nginx_version: Select the version of Nginx.
* nginxPort: Specify the port for the Nginx deployment.

## Generated Files

Upon completion, Pypyrus will generate the following files:

* argocd/argocd-application.yaml: ArgoCD application configuration.
* nginx/nginx-deployment.yaml: Nginx deployment configuration.

Feel free to customize the generated files based on your project requirements.

## Feedback

If you encounter any issues or have suggestions for improvement, please open an issue. Your feedback is highly appreciated!