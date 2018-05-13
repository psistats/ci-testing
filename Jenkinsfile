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
        sh 'printenv'
      }
    }     
    stage('debug-output') {
      steps {
        sh 'printenv'
      }
    }
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
       
    stage('snapshot') {
      when { 
        branch 'develop'
        expression { return env.shouldBuild != "false" }
      }
      steps {
        build (job: "citest-snapshot", wait: false)
      }
    }
  }
}
