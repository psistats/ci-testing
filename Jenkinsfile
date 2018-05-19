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

        def scmVars;

        if (env.APPVEYOR == null) {
            stage('prepare') {
                scmVars = checkout scm
                echo "scmVars: ${scmVars}"
                sh 'printenv'
                echo "${env}"
            }
            /*
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
            */
            stage('test-w32') {

                withCredentials([string(credentialsId: 'appveyor-token', variable: 'APPVEYOR_TOKEN')]) {
                    echo '---> STARTING APPVEYOR <---'

                    def body = """{
                        "accountName": "alex-dow",
                        "projectSlug": "citest",
                        "branch": "${scmVars.GIT_BRANCH}"
                    }"""

                    echo "Request body: ${body}"

                    response = httpRequest(
                        url: 'https://ci.appveyor.com/api/builds',
                        httpMode: 'POST',
                        customHeaders: [
                            [name: 'Authorization', value: "Bearer ${APPVEYOR_TOKEN}"],
                            [name: 'Content-type', value: 'application/json']
                        ],

                        requestBody: body
                    )
                    echo '---> APPVEYOR RESULTS <---'

                    def content = response.getContent();
                    def parser = new groovy.json.JsonSlurper();
                    def build = parser.parseText(content);

                    echo "--> BUILD ID: ${build.buildId}"

                    def appveyor_finished = false

                    while (appveyor_finished == false) {

                        def buildResponse = httpRequest(
                            url: 'https://ci.appveyor.com/api/projects/alex-dow/citest/history?recordsNumber=5',
                            customHeaders: [
                                [name: 'Accept', value: 'application/json'],
                                [name: 'Authorization', value: "Bearer ${APPVEYOR_TOKEN}"]
                            ]
                        )

                        def buildContent = buildResponse.getContent();
                        echo "--> STATUS CONTENT: ${buildContent}";
                        def buildObj = parser.parseText(buildContent);

                        buildObj.builds.each{ buildData ->
                            if (buildData.buildId == build.buildId) {
                                echo "--> BUILD_STATUS: ${buildData.status}"
                            } else {
                                return;
                            }
                        }
                    }
                }
            }
            /*
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
            */
        } else if (env.APPVEYOR == 'True')  {
            stage('post-appveyor') {
                echo 'POST APPVEYOR'
            }
        }
    }
}
