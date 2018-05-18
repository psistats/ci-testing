node('master') {

    properties([
        pipelineTriggers([
            [$class: 'GenericTrigger',
                genericVariables: [
                    [expressionType: 'JSONPath', key: 'APPVEYOR_ARTIFACT', value: '$.artifacts[0].url'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR', value: '$.environmentVariables.appveyor']
                ]
            ]
        ])
    ])

    ws("${env.JENKINS_HOME}/workspace/${env.JOB_NAME}") {
        if (env.APPVEYOR == null) {
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
            stage('test-w32') {

                withCredentials([string(credentialsId: 'appveyor-token', variable: 'APPVEYOR_TOKEN')]) {
                    ref response = httpRequest(
                        url: 'https://ci.appveyor.com/api/builds',
                        httpMode: 'POST',
                        customHeaders(
                            [name: 'Authorization', value: 'Bearer ${APPVEYOR_TOKEN}'],
                            [name: 'Content-type', value: 'application/json']
                        ),

                        requestBody: '''{
                            "accountName": "alex-dow",
                            "projectSlug": "citest",
                            "branch": "${svcVars.GIT_BRANCH}"
                        }'''
                    );
                    echo '---> APPVEYOR RESULTS <---'
                    echo response.getStatus();
                    echo response.getContent();
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
        } else if (env.APPVEYOR == 'True')  {
            stage('post-appveyor') {
                echo 'POST APPVEYOR'
            }
        }
    }
}
