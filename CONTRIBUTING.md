# Contributing Guide

First off, thank you for considering contributing to gpt-code-search! 🚀

## Where do I go from here?

If you've noticed a bug or have a feature request, make one here! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

Issue Tracker: https://github.com/wolfia-app/gpt-code-search/issues

## Fork & Create a Branch

If this is something you think you can fix, then fork gpt-code-search and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```bash
git checkout -b 325-contribution-guide
```

## Get the Code Running

The following steps will get you running the gpt-code-search project locally.

1. Clone the repository:

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/gpt-code-search.git
```

1. Change directory to gpt-code-search:

```bash
cd gpt-code-search
```

1. Install poetry using the instructions here: https://python-poetry.org/docs/#installing-with-the-official-installer. The project uses [poetry](https://python-poetry.org/) for dependency management and packaging.

1. Install dependencies:

```bash
poetry install
```

1. Install pre-commit hooks:

```bash
poetry run pre-commit install
```

1. Set the environment variable `LOCAL_DEV` to `true` for local development:

```bash
export LOCAL_DEV=true
```

1. Run the project:

```bash
poetry run python core/main.py
```

Now you can modify the codebase and see your changes!

## Make Changes Locally

Now that you have a new branch, you can make your changes. In the process of doing so, ensure that your changes stick to the "code of conduct" as explained in our Coding Guidelines.

1. Commit your changes and push your branch to GitHub:

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin BRANCH-NAME
```

## Make a Pull Request

1. Navigate to your fork on GitHub, and press the "Compare & pull request" button on the page.
2. You'll be taken to a page where you can enter a title and description for your pull request.
3. Press the "Create pull request" button.
4. Now we wait for the maintainers to review your pull request!
5. Once your pull request has been reviewed and the branch passes all tests, it will be merged into the main branch.
6. Congratulations! You've successfully contributed to gpt-code-search!

## Code review process

The bigger the pull request, the longer it will take to review and merge. Try to break down large pull requests into smaller chunks that are easier to review and merge. It is also always helpful to have some context or background for your pull request. What was the purpose of the change? What was the behavior before the change?

Remember, code review is a tool for both quality and knowledge sharing. It's important to be patient and considerate of the reviewer's time.

Thank you for your contribution! ❤️❤️❤️

## Communication

We use GitHub comments to communicate about pull requests. If you have questions about the project, you can reach out by creating a new issue.
