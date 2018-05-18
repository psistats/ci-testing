node('master') {

    properties([
        pipelineTriggers([
            [$class: 'GenericTrigger',
                genericVariables: [
                    [expressionType: 'JSONPath', key: 'APPVEYOR_ARTIFACT', value: '$.artifacts[0].url']
                ]
            ]
        ])
    ])

    ws("${env.JENKINS_HOME}/workspace/${env.JOB_NAME}") {
        stage('prepare') {
            def scmVars = checkout scm
            echo "scmVars: ${scmVars}"
            sh 'printenv'
            echo "${env}"
        }
        stage('test-py35') {
            withPythonEnv('psikon-py35') {
                pysh 'pip install tox'
                pysh 'tox -e py35'
            }
        }
        stage('test-py36') {
            withPythonEnv('psikon-py36') {
                pysh 'pip install tox'
                pysh 'tox -e py36'
            }
        }
        stage('test-coverage') {
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
                    zoomCoverageCharge: true
                ])
            }
        }
    }
}
