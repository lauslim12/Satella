# Contributing

In order to contribute to this project, please follow these style guide and workflow.

## Coding Style Guide

Please follow this for the sake of the code to be as readable and maintainable as possible.

- **_Use your best spelling and punctuation, in English._**
- Please use `black` and `isort` packages to format your code.
- Please use `pylint` and/or `pylance` packages to lint your code for any possible errors.
- Please use `mypy` package to ensure that the data types that you code are correct.

All of the packages are available in the `pyproject.toml` file.

## Example Usage

Below is an example usage of how to conform to the coding style.

```bash
cd Satella
black .
isort .
mypy .
pylint src
```

## Commit Style Guide

Please use [Semantic Commit Messages](https://seesparkbox.com/foundry/semantic_commit_messages), but with past tense and first letter capitalized. For further details, please check [this gist](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716) and this [website](https://www.conventionalcommits.org/en/v1.0.0/). Using these kinds of commit messages will make contributors into better programmers because of its rigid style. Another reason of using it is because its rigid style actually forces contributors to **not commit lots of files in one setting.**

## Workflow

In order to contribute to this project, please create an issue about the problem that you are going to fix / add so that we can discuss it together. After that, follow these instructions below.

- Fork the repository.
- Create a new branch based on the issue number that you created beforehand. Example: `git checkout -b 10`.
- Commit and push your features / changes.
- Create a new pull request.
