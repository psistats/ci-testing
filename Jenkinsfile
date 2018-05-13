pipeline {
  agent {
    node {
      label 'master'
      customWorkspace "${JENKINS_HOME}/workspace/${JOB_NAME}"
    }
  }
  stages {
    stage('debug-output') {
      steps {
        sh 'printenv'
      }
    }
    /*
    stage('test-py35') {
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e py35'
        }
      }
    }
    stage('test-py36') {
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e py36'
        }
      }
    }
    stage('test-coverage') {
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e coverage'
        }
      }
    }
    */
       
    stage('set-build-number') {
      when { branch 'develop' }
      steps {
        cleanWs()
        sh 'git clone git@github.com:psistats/ci-testing.git'
        sh 'git checkout develop'
        
        withPythonEnv('psikon-py35') {
          pysh 'building/change_version.py --set-build=${BUILD_NUMBER}'
        }

        sh 'git commit setup.py -m "Increasing build number"'

        /*
        withCredentials([sshUserPrivateKey(credentialsId: 'psikon-ci-github-ssh', keyFileVariable: 'GITHUB_KEY')]) {
          sh 'echo ssh -i $GITHUB_KEY -l git -o StrictHostKeyChecking=no \\"$@\\" > run_ssh.sh'
          sh 'chmod +x run_ssh.sh'
          withEnv(['GIT_SSH=run_ssh.sh']) {
            sh 'git remote set-url origin git@github.com:psistats/ci-testing.git'
            sh 'git push origin develop'
          }
        }
        */

        sshagent(credentials: ['psikon-ci-github-ssh']) {
          sh 'git push origin develop'
        }

        /*
        withCredentials([usernamePassword(credentialsId: 'psikon-ci-github-accoutn', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
          sh 'git checkout develop'
          sh 'git pull'
          sh 'git commit setup.py -m "Increasing build number"'
          sh 'git push origin develop'
        }
        */
      }
    }
  }
  post {
    always {
      step([$class: 'CoberturaPublisher',
        autoUpdateHealth: false,
        autoUpdateStability: false,
        coberturaReportFile: 'coverage.xml',
        failUnhealthy: false,
        failUnstable: false,
        maxNumberOfBuilds: 0,
        onlyStable: false,
        sourceEncoding: 'ASCII',
        zoomCoverageChart: false
      ])
    }
  }
}
