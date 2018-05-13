pipeline {
  parameters {
    booleanParam(defaultValue: true, description: 'Execute pipeline?', name: 'shouldBuild')
  }
  agent {
    node {
      label 'master'
      customWorkspace "${JENKINS_HOME}/workspace/${JOB_NAME}"
    }
  }
  stages {
    stage('prepare') {
      steps {
        script {
          result = sh(script: "git log -1 | grep '.*\\[ci skip\\].*'", returnStatus: true)
          if (result == 0) {
            echo ("'ci skip' spotted in git commit. Aborting.")
            env.shouldBuild = "false"
          }
        }
      }
    }     
    stage('debug-output') {
      steps {
        sh 'printenv'
      }
    }
    stage('test-py35') {
      when { expression { return env.shouldBuild != "false" } }
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e py35'
        }
      }
    }
    stage('test-py36') {
      when { expression { return env.shouldBuild != "false" } }
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e py36'
        }
      }
    }
    stage('test-coverage') {
      when { expression { return env.shouldBuild != "false" } }
      steps {
        withPythonEnv('psikon-py35') {
          pysh 'tox -e coverage'
          step([$class: 'CoberturaPublisher',
          autoUpdateHealth: false,
          autoUpdateStability: false,
          coberturaReportFile: 'coverage.xml',
          failUnhealthy: false,
          failUnstable: false,
          maxNumberOfBuilds: 30,
          onlyStable: true,
          sourceEncoding: 'ASCII',
          zoomCoverageChart: true])
        }
      }
    }
       
    stage('set-build-number') {
      when { 
        branch 'develop'
        expression { return env.shouldBuild != "false" }
      }
      steps {
        cleanWs()
        sshagent(credentials: ['psikon-ci-github-ssh']) {
          script {
            sh 'git clone git@github.com:psistats/ci-testing.git .'
            sh 'git checkout develop'
            withPythonEnv('psikon-py35') {
              pysh 'building/change_version.py --set-build=${BUILD_NUMBER}'
            }
            sh 'git commit setup.py -m "Increasing build number [ci skip]"'
            sh 'git push git@github.com:psistats/ci-testing.git'
          }
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
      emailext (
        subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':
                 Check console output at ${env.BUILD_URL}""",
        to: 'ci@psikon.com',
        recipientProviders: ['developers']
      )
    }
  }
}
