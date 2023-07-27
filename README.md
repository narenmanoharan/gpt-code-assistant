<div align="center">
  <img
    height="240"
    width="240"
    alt="logo"
    src="https://raw.githubusercontent.com/narenmanoharan/gpt-code-assistant/main/public/logo.png"
  />
  <h1>gpt-code-assistant</h1>
  <p>
    <b>gpt-code-assistant</b> is an AI-based open-source tool for exploring, querying, and understanding any codebase using Language Models (LLMs) and vector embeddings (a technique to convert objects, like text, into vectors).
  </p>
</div>

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Configuration](#configuration)
- [Problem](#problem)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Features

- **LLM-based Search & Retrieval**: Uses Language Models for efficient code search, retrieval, and comprehension.
- **File-system Integration**: Designed to work with any codebase and operates directly with any local code on your machine, allowing seamless integration with your existing workflow.
- **Language Agnostic**: Supports multiple programming languages.
- **Privacy-centric Design**: Code snippets are only transmitted when a question is asked and the Language Model requests the relevant code, ensuring privacy. **(Note: Code snippets are shared with OpenAI)**

Future plans include supporting local models and the ability to generate code.

## Getting Started

### Installation

```bash
pip install gpt-code-assistant
```

### Usage

#### Create a project

First, create a project to index all the files. This step involves creating embeddings for each file and storing them in a local database.

```bash
gpt-code-assistant create-project <project-name> <path-to-codebase>

gpt-code-assistant create-project gpt-code-assistant .
```

#### Ask a question about your codebase

To query about the purpose of your codebase, you can use the `query` command:

```bash
gpt-code-assistant query <project-name> "What does this codebase do?"
```

<img src="public/demo.gif" width="750"  alt="gpt-code-assistant demo"/>

If you want to generate a test for a specific file, for example analytics.py, you can mention the file name to improve accuracy:

```bash
gpt-code-assistant query gpt-code-assistant "Can you generate a test for analytics.py?"
```

For a general usage question about a certain module, like analytics, you can use keywords to search across the codebase:

```bash
gpt-code-assistant query gpt-code-assistant "How do I use the analytics module?"
```

**Remember, mentioning the file name or specific keywords improves the accuracy of the search.**

#### List all projects

To get a list of all the projects:

```bash
gpt-code-assistant list-projects
```

#### Refresh a project

If you want to reindex a project and update the embeddings to the latest content:

```bash
gpt-code-assistant refresh-project <project-name>
```

#### Delete a project

If you wish to delete a project and all its data (including embeddings):

```bash
gpt-code-assistant delete-project <project-name>
```

#### Select a model to use

You can select which model to use for your queries:

```bash
gpt-code-assistant select-model
```

Defaults to `gpt-3.5-turbo-16k`. The selected model is stored in `$HOME/.gpt-code-assistant/config.toml`.

### Configuration

The tool will prompt you to configure the `OPENAI_API_KEY`, if you haven't already.

## Problem

You want to leverage the power of GPT-4 to search your codebase, but you don't want to manually copy and paste code snippets into a prompt nor send your code to another third-party service (other than OpenAI). This tool solves these problems by letting GPT-4 determine the most relevant code snippets within your codebase. It also allows you to perform your queries in your terminal, removing the need for a separate UI.

Examples of the types of questions you might want to ask:

- 🐛 Help debugging errors and finding the relevant code and files
- 📝 Document large files or functionalities formatted as markdown
- 🛠️ Generate new code based on existing files and conventions
- 📨 Ask general questions about any part of the codebase

## Roadmap

- [x] Use vector embeddings to improve search and retrieval
- [ ] Add support for additional models (Claude, Bedrock, etc)
- [ ] Add support for local models (Llama2, Starcoder, etc)
- [ ] Add support for generating code and saving it to a file
- [ ] Support for searching across multiple codebases
- [ ] Allow the model to create new functions that it can then execute
- [ ] Use [guidance](https://github.com/microsoft/guidance) to improve prompts

## Contributing

We love contributions from the community! ❤️ If you'd like to contribute, feel free to fork the repository and submit a pull request.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guide](CONTRIBUTING.md) for more detailed steps and information.

## Code of Conduct

We are committed to fostering a welcoming community. To ensure that everyone feels safe and welcome, we have a [Code of Conduct](CODE_OF_CONDUCT.md) that all contributors, maintainers, and users of this project are expected to adhere to.

## Support

If you're having trouble using `gpt-code-assistant`, feel free to [open an issue](https://github.com/narenmanoharan/gpt-code-assistant/issues) on our GitHub. You can also reach out to us directly at [narenkmanoharan@gmail.com](mailto:narenkmanoharan@gmail.com). We're always happy to help!

## Feedback

Your feedback is very important to us! If you have ideas for how we can improve `gpt-code-assistant`, we'd love to hear from you. Please [open an issue](https://github.com/narenmanoharan/gpt-code-assistant/issues) or reach out to us directly at [narenkmanoharan@gmail](mailto:narenkmanoharan@gmail) with your feedback or thoughts.

## License

This project is licensed under the terms of the [Apache 2.0](LICENSE).
