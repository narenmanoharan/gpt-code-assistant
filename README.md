<div align="center">
  <h1>gpt-code-search</h1>
  <img
    height="240"
    width="240"
    alt="logo"
    src="https://raw.githubusercontent.com/wolfia-app/gpt-code-search/main/public/logo.png"
  />
  <p>
    <b>gpt-code-search</b> is an AI-powered tool enabling you to search your codebase with natural language. It utilizes GPT-4 to retrieve, search and answer queries about your code, boosting productivity and code understanding.
  </p>
</div>

## Features

- 🧠 **GPT-4**: Code search, retrieval, and answering all done with OpenAI and [function calling](https://openai.com/blog/function-calling-and-other-api-updates).
- 🔐 **Privacy-first**: Code snippets only leave your machine when you ask a question and the LLM requests the relevant code.
- 🔥 **Works instantly**: No pre-processing, chunking, or indexing, get started right away.
- 📦 **File-system backed**: Works with any code on your machine.

## Getting Started

### Installation

```bash
pip install gpt-code-search
```

### Usage

#### Ask a question about your codebase

```bash
gcs query "What does this codebase do?"

gcs query "Can you generate a test for analytics.py?" # Note: Mentioning the file name is advised to improve accuracy

gcs query "How do I use the analytics module?" # Note: Mentioning keywords to search across the codebase is advised to improve accuracy
```

#### Select a model

```bash
gcs select-model
```

Defaults to `gpt-3.5-turbo-16k`. The selected model is stored in `~/$HOME/.gpt-code-search/config.toml`.


### Configuration

The tool will prompt you to configure the `OPENAI_API_KEY`, if you haven't already.

## Problem

You want to leverage the power of GPT-4 to search your codebase, but you don't want to manually copy and paste code snippets into a prompt nor send your code to another third-party service.

This tool solves these problems by letting GPT-4 determine the most relevant code snippets within your codebase. This removes the need to copy and paste or send your code to another third-party. Also, it meets you where you already live, in your terminal, not a new UI or window.

Examples of the types of questions you might want to ask:

- 🐛 Help debugging errors and finding the relevant code and files
- 📝 Document large files or functionalities formatted as markdown
- 🛠️ Generate new code based on existing files and conventions
- 📨 Ask general questions about any part of the codebase

## How it works

This tool utilizes [OpenAI's function calling](https://platform.openai.com/docs/guides/gpt/function-calling) to allow GPT to call functions in your codebase. This enables us to automatically upload context directly from the file system on-demand, without having to manually copy and paste code snippets. This also means that no code is sent to any third-party service (other than OpenAI), only the question you ask and the code snippets that are requested by the LLM.

The functions currently available for the LLM to call are:

- `search_codebase` - searches the codebase using a TF-IDF vectorizer
- `get_file_tree` - provides the file tree of the codebase
- `get_file_contents` - provides the contents of a file

Combining these three functions, we can ask the LLM to search the codebase for a keyword, and then retrieve the contents of the file that contains the keyword. And it's as simple as that!

### Privacy

Outside of the LLM, no data is sent or stored.

The only data sent to LLM is the question you ask and the code snippets that it requests related to your question. All code snippets are retrieved from your local machine.

## Limitations

This does have some limitations, namely:

- The LLM is unable to search and load context across mutliple files at once. This means that if you ask a question that requires context from multiple files, you will need to ask multiple questions.
- Specify the file name and keywords in your question to improve accuracy. For example, if you want to ask a question about `analytics.py`, mention the file name in your question.
- The level of search and retrieval is limited by the context window, which refers to the scope of the search conducted by the tool, meaning that we can only search 5 levels deep in the file system. So you need to run the tool from the folder/package closest to the code you want to search.

These limitations lead to suboptimal results in a few cases, but we're working on improving this. **We wanted to get this tool out there as soon as possible to get feedback and iterate on it!**

## Wolfia Codex

`gpt-code-search` is a simplified version of [Wolfia Codex](https://wolfia.com), a cloud tool that enables you to ask any question about open source and private code bases like [`Langchain`](https://wolfia.com/?projectId=2b964031-0ce8-472a-abb7-27079a7b84f3), [`Vercel ai`](https://wolfia.com/?projectId=4710df1f-43f8-4d30-863b-d67876ae0f06), or [`gpt-engineer`](https://wolfia.com/?projectId=8d9dd449-da2d-410e-a4fc-f2ff75a30f73).

If you're looking for a more powerful tool which solves the above limitations by using vector embeddings and a more powerful search and retrieval system, or avoiding the setup, check out [Wolfia Codex](https://wolfia.com), search codebases, share your questions and answers, and more!

## Analytics

We collect anonymous crash and usage data to help us improve the tool. This data aids in understanding usage patterns and improving the tool. You can opt out of analytics by running:

```bash
gcs opt-out-of-analytics
```

You can check the data that by looking at the [analytics](core/analytics.py) and [config](core/config.py) files.

Here's an exhaustive list of the data we collect:

```
- exception - stacktraces of crashes
- uuid - a unique identifier for the user
- model - the model used for the query
- usage - the type of usage (query_count, query_at, query_execution_time)
```

**Note: We do not collect any PII (ip-address), queries or code snippets.**

## Development

The project uses [poetry](https://python-poetry.org/) for dependency management and packaging. The codebase is structured in a modular fashion, making it easier for contributions. To get started, install poetry and run the following commands:

```bash
# Install dependencies
poetry install
```

Run the project

```bash
# Run the project
poetry run python core/main.py
```

Install pre-commit hooks

```bash
# Install pre-commit hooks
poetry run pre-commit install
```

```bash
# Setup local development
export LOCAL_DEV=true
```

## Contributing

We love contributions from the community! ❤️ If you'd like to contribute, feel free to fork the repository and submit a pull request.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guide](CONTRIBUTING.md) for more detailed steps and information.

## Code of Conduct

We are committed to fostering a welcoming community. To ensure that everyone feels safe and welcome, we have a [Code of Conduct](CODE_OF_CONDUCT.md) that all contributors, maintainers, and users of this project are expected to adhere to.

## Support

If you're having trouble using `gpt-code-search`, feel free to [open an issue](https://github.com/wolfia-app/gpt-code-search/issues) on our GitHub. You can also reach out to us directly at [support@wolfia.com](mailto:support@wolfia.com). We're always happy to help!

## Feedback

Your feedback is very important to us! If you have ideas for how we can improve `gpt-code-search`, we'd love to hear from you. Please [open an issue](https://github.com/wolfia-app/gpt-code-search/issues) with your suggestions, or you can email [support@wolfia.com](mailto:support@wolfia.com).

## License

Apache 2.0 © [Wolfia](https://wolfia.com)
