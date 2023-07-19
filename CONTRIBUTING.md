# Contributing guidelines

## Git workflow

* Use git-flow - create a feature branch from `develop`, e.g. `feat/new-feature`
* Pull requests must contain a succinct, clear summary of what the user need is driving this feature change
* Ensure your branch contains logical atomic commits before sending a pull request
* You may rebase your branch after feedback if it's to include relevant updates from the develop branch. It is preferable to rebase here then a merge commit as a clean and straight history on develop with discrete merge commits for features is preferred
* To find out more about contributing click [here](https://contributing.md/)

## Commit messages

Please use the following format for commit messages:

```textbox
* fix: for a bug fix
* feat: for a new feature
* docs: for documentation changes
* style: for changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* refactor: for refactoring production code
* test: for adding tests
* chore: for updating build tasks, package manager configs, etc
* build: for changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
```

## Pull requests

* Pull requests should be made to the `develop` branch
* Pull requests should be made from a feature branch, not `develop`
* Pull requests should be made with a succinct, clear summary of what the user need is driving this feature change
* An automated template will be provided to help with this process, please fill it out as best you can

## Release branches and Tagging

* Once a single or set of changes has been made that can be released, we create a release branch off develop
  * Releases should be as small as possible so that it is easier to fix issues and rollback code in production environment without losing many features at once
  * Release branches should be of the following structure:

    ```sh
    release/0.1.0
    ```

  * The release name should abide by [semantic versioning (semver)](https://semver.org/)
* Once release branch has been created, a pull request should be made against the `main` branch
* Once approved, the release branch can be merged locally :warning: **WARNING - Do not push to remote** :warning:
* Tag the release and push to remote - [see tagging](#tagging)

## Tagging

* Tag latest commit on branch, this should be the local merge commit
  * Check latest local commit, run: `git show HEAD`
  * Create tag, run: `tag -s <tag> -m <message>`
    * where `tag` is the semver value (should be taken from the release branch name) and `<message>` is a general, short and concise message of the change
* Push release merge and tag to remote, run: `git push --follow-tags`
* Once pushed, go to the Github releases page for the repository in question, which can be found by clicking on the <> Code tab and clicking on Releases on the right hand side:
  * Select Tags
  * Click on the v0.1.0 tag that you just created
  * Choose Create release from tag
  * Copy the release name and make human-friendly (capitalise, remove /) to create a release title (e.g. release/0.1.0 -> Release 0.1.0)
  * Add relevant release notes, this can be expanded from initial message created against the tag. Advised to use bullet points to list out changes
  * Hit Publish release
