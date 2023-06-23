Contributing guidelines
=======================

### Git workflow
* Use git-flow - create a feature branch from `develop`, e.g. `feature/new-feature`
* Pull requests must contain a succinct, clear summary of what the user need is driving this feature change
* Ensure your branch contains logical atomic commits before sending a pull request
* You may rebase your branch after feedback if it's to include relevant updates from the develop branch. It is preferable to rebase here then a merge commit as a clean and straight history on develop with discrete merge commits for features is preferred
* To find out more about contributing click [here](https://contributing.md/)

### Commit messages
Please use the following format for commit messages:

```
* fix: for a bug fix
* feat: for a new feature
* docs: for documentation changes
* style: for changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* refactor: for refactoring production code
* test: for adding tests
* chore: for updating build tasks, package manager configs, etc
* build: for changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
```

### Pull requests
* Pull requests should be made to the `develop` branch
* Pull requests should be made from a feature branch, not `develop`
* Pull requests should be made with a succinct, clear summary of what the user need is driving this feature change
* An automated template will be provided to help with this process, please fill it out as best you can
