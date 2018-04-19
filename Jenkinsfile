pipeline {
  agent any
  stages {
    stage('test-py35') {
      steps {
        withPythonEnv('psikon-py35') {
          sh 'pip install tox'
          sh 'tox -e py35'
        }
      }
    }
    stage('test-py36') {
      steps {
        withPythonEnv('psikon-py36') {
          sh 'pip install tox'
          sh 'tox -e py36'
        }
      }
    }
    stage('test-coverage') {
      steps {
        withPythonEnv('psikon-py35') {
          sh 'pip install tox'
          sh 'tox -e coverage'
        }
      }
    }
  }
  post {
    always {
      junit 'coverage.xml'
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
