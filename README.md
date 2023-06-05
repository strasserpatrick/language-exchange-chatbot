# Language Exchange Chatbot

This example project demonstrates how to build a chatbot using streamlit and terraform. 
Its aim is to provide a simple chat UI for language exchange as a webapp on Microsoft Azure.

## Use Case

Suppose you want to learn Spanish. You can use this chatbot to have conversations with ChatGPT instructed to only speak Spanish. This way, you can practice your Spanish skills and learn new words and phrases. You can also use this chatbot to learn other languages, such as German, French, or Italian. The only thing to do is to change the role configured in the `config.yaml` file.

## Description

The chatbot UI is built using the [Streamlit](https://www.streamlit.io/) framework. It is deployed to Microsoft Azure using [Terraform](https://www.terraform.io/). The chatbot itself is calles the OpenAI ChatGPT API with custom roles that can be specified in no-code YAML files. The chatbot is deployed to Microsoft Azure as a [Docker](https://www.docker.com/) Image.

## Getting Started

### Local Development

To run the chatbot locally, you need to have Python 3.7+ installed. Then, install the dependencies using the Makefile:

```bash
make install
```

Then, you can run the chatbot using the following command:

```bash
make streamlit
```

### Deployment

To deploy the chatbot, you need to have `terraform` and `cdktf` installed. Look [here](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install) for installation instructions.

All credentials need to be stored in a file named `.env` for secrets as well as configuring the `config.yaml` for further adjusting. For all .env variables you can look at the `.env.example` file.

To deploy the chatbot, run the following commands:

```bash
make deploy
```

Then, you can build the docker image locally by using `make build` and then push it to your newly deployed Azure Container Registry. Note: you need to match the name specified in `config.yaml`.

After that, you can access the chatbot by navigating to the URL specified in the output of the `make deploy` command.
