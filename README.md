<div align="center">
  <h1>gpt-code-search</h1>
  <img
    height="240"
    width="240"
    alt="logo"
    src="https://raw.githubusercontent.com/wolfia-app/gpt-code-search/main/public/logo.png"
  />
  <p>
    <b>gpt-code-search</b> enables you to search your codebase with natural language using GPT-4.
  </p>
</div>

## Problem

You want to leverage the power of GPT-4 to search your codebase, but you don't want to manually copy and paste code snippets into a prompt nor send your code to another third-party service.

This tool solves these problems by letting GPT-4 determine the most relevant code snippets within your codebase. This removes the need to copy and paste or send your code to another third-party. Also, it meets you where you already live, in your terminal, not a new UI or window.

Examples of the types of questions you might want to ask:

- 🐛 Help debugging errors and finding the relevant code and files
- 📝 Document large files or functionalities formatted as markdown
- 📨 Ask general questions about any part of the code
- 🛠️ Generate new code based on existing files and conventions

## Features

- 🧠 **GPT-4**: code search, retrieval, and answering all done with OpenAI and [function calling](https://openai.com/blog/function-calling-and-other-api-updates).
- 🔐 **Privacy-first**: code snippets only leave your machine when you ask a question and the LLM requests the relevant code.
- 🔥 **Works instantly**: no pre-processing, chunking, or indexing, get started right away.
- 📦 **File-system backed**: works with any code on your machine.

## Getting Started

TODO

## Privacy

Outside of the LLM, no data is sent or stored.

The only data sent to LLM is the question you ask and the code snippets that is requests related to your question. All code snippets are retrieved from your local machine.

## Wolfia Codex

This tool is a simplified version of [Wolfia Codex](https://wolfia.com), a cloud tool that enables you to ask any question about open source and private code bases like [`Langchain`](https://wolfia.com/?projectId=2b964031-0ce8-472a-abb7-27079a7b84f3), [`Vercel ai`](https://wolfia.com/?projectId=4710df1f-43f8-4d30-863b-d67876ae0f06), or [`gpt-engineer`](https://wolfia.com/?projectId=8d9dd449-da2d-410e-a4fc-f2ff75a30f73).

If you're looking for a more powerful tool, or avoiding the setup, check out [Wolfia Codex](https://wolfia.com), search codebases, share your questions and answers, and more!
