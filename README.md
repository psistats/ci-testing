# ci-testing
This project is to test various Jenkins CI related things.

Once complete, it will serve as documentation for setting up a Jenkins environment in a similar fashion as well as gotchas

## Repository Workflow

This project imposes a specific kind of workflow.


```
feature2 ------\
                \
feature ----\    \
             \    \
develop ------*----*---\----
                        \
master ------------------*---
```

Each new feature and/or bug fix must be a squashed pull request to the develop branch.

At some point, the develop branch will merge into the master bracnh. All changed between the last merge and this merge will count as the change log. When master is updated, this means a new release, thus a new version tag.

Whenever a new feature / fix is merged into the develop branch, then the build number should increase and a snapshot should be built, packaged, and deployed.

## git tricks

### squash the feature branch

```
git checkout yourBranch
git reset $(get merge-base develop yourBranch)
git add -A
git commit -m "describe the feature"
```

## Jenkins Setup

### Plugins

1. Cobertura Plugin
2. Git Plugin
3. Git Autostatus Plugin
4. GitHub Branch Source Plugin
5. Git Custom Notification Context SCM Behavior
6. GitHub Integration Plugin
7. HTML Publisher plugin
8. MultiJob Plugin
9. Pipeline Github Notify Step Plugin
10. Pipeline GitHub
11. Pipeline GitHub Groovy Libraries
12. Pipeline Multibranch
13. Pyenv Pipeline Plugin
14. ShiningPanda Plugin

### Setup

Jenkins will be used to automate all facets of building and deploying artifacts. Its responsibilities will be:

1. Build pull requests on the develop branch
2. Build pull requests on the master branch
3. Build a new release when the master branch changes
4. Build a new snapshot when the develop branch changes


#### Credentials

You need to setup your GitHub credentials first. I've never managed to use the "Add Credential" feature. So instead goto to:

`Jenkins -> Credentials`

1. Add your GitHub username/password.
2. Goto https://github.com/settings/tokens and generate a new token
3. Give it all repo, admin:org, admin:repo_hook, notifications, user, write:discussion permissions
4. Copy the generated token and create a new secret key credential with this token

## Versioning

The develop branch will always have the NEXT version. It will be `x.y.z-dev[build_number]`. So when something gets merged into develop, its build number will go up.

The master branch's version will be decided by develop branch.

## Building Steps

1. Code quality/linting
2. Unit testing
3. Prepare source distribution
4. Prepare debian package
5. Prepare RPM package
6. Prepare Windows package
7. Upload artifacts to their respective locations


The preparation of packages should be a standalone job.
