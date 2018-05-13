// vi: ft=Jenkinsfile
pipeline {
  agent {
    node {
      label 'master'
      customWorkspace "${JENKINS_HOME}/workspace/${JOB_NAME}"
    }
  }
  stages {
    stage('prepare') {
      steps {
        cleanWs()
        git(url: 'https://github.com/psistats/citest', credentialsId: 'psikon-ci-github-account', branch: 'develop')
        sshagent(credentials: ['psikon-ci-github-ssh']) {
          script {
            sh 'git checkout develop'

            script {
              def changeLogSets = currentBuild.changeSets
              for (int i = 0; i < changeLogSets.size(); i++) {
                for (int j = 0; j < changeLogSets[i].items.length; j++) {
                  def entry = changeLogSets[i].items[j];
                  echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}\n"
                }
              }
            }

            withPythonEnv('psikon-py35') {
              pysh 'building/change_version.py --set-build=${BUILD_NUMBER}'
            }
            sh 'git commit setup.py -m "Increasing build number [ci skip]"'
            sh 'git push git@github.com:psistats/citest'

            withPythonEnv('psikon-py35') {
              pysh 'building/build_deb.sh'
            }
          }
        }
      }
    }
  }
}
