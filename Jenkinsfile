pipeline {
  agent any
  stages {
    stage('test-py35') {
      steps {
        sh 'tox -e py35'
      }
    }
    stage('test-py36') {
      steps {
        sh 'tox -e py36'
      }
    }
    stage('test-coverage') {
      steps {
        sh 'tox -e coverage'
      }
    }
  }
}
