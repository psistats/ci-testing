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
      withPythonEnv('psikon-py36') {
        steps {
          sh 'tox -e py36'
        }
      }
    }
    stage('test-coverage') {
      withPythonEnv('psikon-py35') {
        steps {
          sh 'tox -e coverage'
        }
      }
    }
  }
}
