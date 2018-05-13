# citest

This project aims to act as a template for future projects. It setups a series of jenkin jobs, has a bunch of helpful scripts, and ultimately automates the whole process of pull request testing, deploying packages of various kinds, and incrementing version numbers, and so on.

It also serves as a point of documentation for starting up your own CI environment from scratch.

It aims to do a lot but it's also very opinionated and expects a certain kind of workflow. Going outside of this workflow will have its own challenges.

This project is python-centric, but could be adapted to fit any other ecosystem.

Following the instructions here, you will end up having

1. A Jenkins server with Github integration
2. A local debian repository
3. A simple unit tested python project
4. test coverage reporting with tox

## Workflow

### Github Repository


```
feature2 ------\
                \
feature ----\    \
             \    \
develop ------*----*---\----
                        \
master ------------------*---
```

When you want to add a new feature, or fix a new bug, you should first branch off of develop, and do your changes there. Afterwards, submit a pull request against the develop branch. Once reviewed, merge the PR into the `develop` branch.

Every time a commit is done to the develop branch, it will trigger a new snapshot build. So one should not commit anything into the develop branch outside of pull requests. This also means pull requests should be squashed, with the commit message explaining what new feature was added or what bug was fixed. A change log will be generated between each commit and it will be used wherever a change log is necessary.

When you feel ready to make a new release, make a pull request between develop and master. The commit message should include a "[release version x.y.z]" where x.y.z is the new version you wish to release. It's assumed this new version follows the https://semver.org/ format.

When a commit happens on master, a new release is created and deployed. The version the develop branch will change to x.y.z+1. So if the release version was 4.2.1, the develop version becomes 4.2.2.

### Squashing Commits

These commands will squash all commits in a branch. Use it for your feature/bug fix branches.

```
git checkout [branch name]
git reset $(get merge-base develop [branch name])
git add -A
git commit -m "Describe the feature"
```

### Commit Special Commands

If these messages are included in the commit, they trigger different actions

| Command | Description |
|---------|-------------|
| [ci skip] | Skip various build steps |
| [release version x.y.z] | Release a new version on master with version `x.y.z` |

## Installation

Setting everything up is a bit of a time consuming process. You will need a few prerequisites:

1. A debian-based operating system (Debian, Mint, Ubuntu, etc)
2. A github account that has administrative rights on a repository

I suggest creating a unique github account specific for Jenkins. First fork this repository then follow these instructions to get it up and running. You can tweak anything here that you'd like in order to match your own environment and project.

### Quick Jenkins Install

These instructions will setup Jenkins and a control script for it in your `$HOME` directory.

You can replace `$HOME` with another folder.

```
$ cd $HOME
$ mkdir Jenkins
$ wget http://mirrors.jenkins.io/war/latest/jenkins.war ./Jenkins
$ wget https://raw.githubusercontent.com/psistats/citest/master/jenkins-control.sh ./Jenkins/jenkins-control.sh
$ chmod u+x ./Jenkins/jenkins-control.sh
```

Edit jenkins-control.sh and set the various settings to match your environment. Afterwards you can start Jenkins

```
$ $HOME/Jenkins/jenkins-control.sh start
```

And now you can visit your Jenkins installation at http://127.0.0.1:8080/jenkins. You will be asked to perform a few tasks during installation. You can pick and choose some plugins to install now, but the next section will have the definitive list of plugins to install to make this project work.

### Jenkins Plugins

To provide the complete CI solution, the following plugins should be installed:

1. Blue Ocean
2. GitHub Pipeline for Blue Ocean
3. Blue Ocean Pipeline Editor
4. Workspace Cleanup
5. Email Extension
6. Pyenv Pipeline
7. ShiningPanda
8. Cobertura

Once the plugins are selected click `Download now and install after restart`.

The plugins will download and Jenkins will restart itself. You may need to refresh your screen several times to see the current state of Jenkins.

### Jenkins Github Integration

The next step is to integrate your Jenkins server with Github. To do this, we need to create three sets of credentials:

1. An SSH Key
2. A username/password
3. A Github token

This is because different tools in this workflow connect to Github in different ways.

#### SSH Key

Generate your SSH key using:

```
$ ssh-keygen -t rsa -b 4096 -C "ci@psikon.com"
```

Use the default value for the location of your key, and enter in a good password.

Next you will need to add your SSH key to ssh-agent.

```
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa
```

Next you will need to add this key to your Github account. You can follow the instructions here: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/

Once your SSH key is associated to your Github account, test to make sure everything is setup properly:

```
$ mkdir tmp
$ cd tmp
$ git clone git@github.com:[your account]/citest.git
$ cd ..
$ rm -rf tmp
```

You should encounter no errors. Now you must add your SSH key to Jenkins. 

1. Using the left side menu, select Credentials.
2. In the next screen, under "Stores scoped to Jenkins" click on "_(global)". 
3. In the next screen click on "Add Credentials" from the left hand side menu. 
4. Select `SSH Username with private key` from the "Kind" dropdown. 
5. For username, enter your Github username. 
6. Select "From the Jenkins master ~/.ssh" 
7. Your passphrase is the one you used when generating your SSH key
8. Give a meaningful ID and description
9. Click OK

#### User/Pass Credentials

To add your github username/password to jenkins:

1. Using the left side menu, select Credentials.
2. In the next screen, under "Stores scoped to Jenkins" click on "_(global)".
3. In the next screen click on "Add Credentials" from the left hand side menu.
4. Select `Username with password` from the "Kind" dropdown.
5. Enter in your github username and password
6. Give a meaningful ID and description
7. Click OK

#### Github Token

You will also need to generate a github token and add it into Jenkins. First goto https://github.com/settings/tokens and click on `Generate New Token`.

After giving the token a meaningful name, select the following scopes:

1. repo
2. read:org
3. read:public_key
4. admin:repo_hook
5. admin:org_hook
6. notifications
7. read:user
8. user:email
9. write:discussion

Once created, you'll be shown your token. This will be the only time you get to see your token. Copy it, go to your Jenkins server and follow these instructions:

1. Using the left side menu, select Credentials.
2. In the next screen, under "Stores scoped to Jenkins" click on "_(global)".
3. In the next screen click on "Add Credentials" from the left hand side menu.
4. Select `Secret text` from the "Kind" dropdown.
5. Paste your token into the "Secret" field.
6. Give it a meaningful ID and description.
7. Click OK

## Setting up the Project

Jenkins is now running and connected to Github. It's time to setup the citest project and see if we can make it build.

### Jenkins Job Builder

This tool makes it easy to create new Jenkins jobs using configuration files.

For more information visit: https://docs.openstack.org/infra/jenkins-job-builder/index.html

#### Installation

```
pip install jenkins-job-builder
mkdir -p ~/.config/jenkins_jobs
touch ~/.config/jenkins_jobs/jenkins_jobs.ini
```

Now edit `$HOME/.config/jenkins_jobs/jenkins_jobs.ini` and put the following in it:

```
[job_builder]

[jenkins]
user=[your jenkins username]
password=[your jenkins password]
url=[url to your Jenkins server]
```

### Deploy Projects

Now that JJB is installed, it's time to deploy the citest projects to it. The first thing you need to do is to tweak some of the build scripts

#### Edit Build Files

First clone the repository:

```
$ git checkout https://github.com/[your name]/citest
```

Next, edit the file `citest/building/jenkins/citest-snapshot.groovy`. On line 13, change the url to match your github url, and change `credentialsId` to match the ID you used when creating the username/password credentials in Jenkins. On line 14, change the string 'psikon-ci-github-ssh' to the same id you used when creating the SSH key credential in Jenkins. Save the file when complete.

Afterwards, edit the file `citest/building/jenkins/citest-snapshot.yaml`. Change url to match your github url, and change the credentials id to the same one you used in `citest-snapshot.groovy`.

Finally, edit the file `citest/building/jenkins/citest.yaml` and change the URL and credential id accordingly.

#### Send Projects to Jenkins

You can now use JJB to send your projects to Jenkins:

```
$ 




