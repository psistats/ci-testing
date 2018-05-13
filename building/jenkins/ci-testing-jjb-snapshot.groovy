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
        git(url: 'https://github.com/psistats/ci-testing.git', credentialsId: 'psikon-ci-github-accoutn', branch: 'develop')
        sshagent(credentials: ['psikon-ci-github-ssh']) {
          script {
            sh 'git checkout develop'
            withPythonEnv('psikon-py35') {
              pysh 'building/change_version.py --set-build=${BUILD_NUMBER}'
            }
            sh 'git commit setup.py -m "Increasing build number [ci skip]"'
            sh 'git push git@github.com:psistats/ci-testing.git'
          }
        }
      }
  }
}
