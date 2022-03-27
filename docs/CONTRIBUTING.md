# Contributing

🚀 Contributing to and extending this project is always welcome.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.

## Issues and feature requests

You've found a bug in the source code, a mistake in the documentation or maybe you'd like a new feature? You can help us by [submitting an issue on GitHub](https://github.com/maxhoheiser/maxland/issues). Before you create an issue, make sure to search the issue archive -- your issue may have already been addressed!

Please try to create bug reports that are:

- _Reproducible._ Include steps to reproduce the problem.
- _Specific._ Include as much detail as possible: which version, what environment, etc.
- _Unique._ Do not duplicate existing opened issues.
- _Scoped to a Single Bug._ One bug per report.

**Even better: Submit a pull request with a fix or new feature!**

<br>

## Development environment setup

You can use Windows, Linux or Mac based machines for developing.

To set up a development environment, please follow these steps:

1.  **Install dependencies**

- install anaconda for your system
- install git for your system
- install pip

2. **Clone the repo**

   ```sh
   git clone https://github.com/maxhoheiser/maxland
   ```

3. **Run installer script with dev flag**

   ```bash
   python install.py --dev
   ```

   for further details, follow the install section in the [README](https://github.com/maxhoheiser/maxland/blob/master/README.md#installation)

4. **Set up your dev environment**

   - install pre-commit hooks `pre-commit install`
   - use black for auto formatting
   - use pylint for linting

   You can use this settings for VS Code:

   ```json
   "python.linting.pylintEnabled": true,
   "python.linting.pylintArgs": ["--enable=W0611"],
   "python.linting.enabled": true,
   "python.linting.pylintCategorySeverity.convention": "Hint",
   "python.linting.maxNumberOfProblems": 120,
   "python.linting.mypyEnabled": true,
   "python.languageServer": "Pylance",
   "python.formatting.provider": "black",
   "python.sortImports.args": ["--profile", "black"],
   "python.formatting.blackArgs": ["--line-length=140"],
   "python.linting.pydocstyleArgs": ["--ignore=D400", "--ignore=D4"],
   "[python]": {
      "editor.defaultFormatter": "ms-python.python",
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
         "source.organizeImports": true
      }
   },
   ```

<br>

5. **Writing code**

   > ### **Please follow the code style guide outlined in the [README](https://github.com/maxhoheiser/maxland/blob/master/README)!!**

   <br>

   Type hinting:

   - use `:` instead of `->`
   - create new type definitions for custom data types where possible
   - try to type hint input arguments as much as possible
   - use Enum and typing Dict, List, Union

   <br>

   Testing:

   - always write unittests for new features
   - try to extend the end-to-end hardware in the loop tests to cover your new functionality as complete as possible
   - always run all tests and fix broken ones

<br>

## How to submit a Pull Request

1. Search our repository for open or closed
   [Pull Requests](https://github.com/maxhoheiser/maxland/pulls)
   that relate to your submission. You don't want to duplicate effort.
2. Fork the project
3. Create your feature branch (`git checkout -b feature/amazing_feature`) - clone from master for stable branches
4. Commit your changes (`git commit -m 'feat: add amazing_feature'`) Traekka Behavior Platform uses [conventional commits](https://www.conventionalcommits.org), so please follow the specification in your commit messages.
5. [Open a Pull Request](https://github.com/maxhoheiser/maxland/compare?expand=1) using the [PULL_REQUEST_TEMPLATE](https://github.com/maxhoheiser/maxland/blob/master/PULL_REQUEST_TEMPLATE.md). Don't forget to [link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if you are solving one.

- Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so the branch can be updated for a merge. Once you submit your PR, we will review your it. We may ask questions or request for additional information.
- We may ask for changes to be made before a PR can be merged, either using [suggested changes](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/incorporating-feedback-in-your-pull-request) or pull request comments. You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.
- As you update your PR and apply changes, mark each conversation as resolved.
- If you run into any merge issues, checkout this [git tutorial](https://lab.github.com/githubtraining/managing-merge-conflicts) to help you resolve merge conflicts and other issues.

<br>

> ## Your PR is merged! - Congratulations 🎉🎉
