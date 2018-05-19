def debug(msg) {
    echo "[DEBUG] ${msg}"
}

def run_appveyor(appveyor_token, accountName, projectSlug, branch, commitId) {
    debug('[APPVEYOR] Starting')

    def request_body = """{
        "accountName": "${accountName}",
        "projectSlug": "${projectSlug}",
        "branch": "${branch}",
        "commitId": "${commitId}"
    }"""

    response = httpRequest(
        url: 'https://ci.appveyor.com/api/builds',
        httpMode: 'POST',
        customHeaders: [
            [name: 'Authorization', value: "Bearer ${appveyor_token}"],
            [name: 'Content-type', value: 'application/json']
        ],
        requestBody: request_body
    )

    def content = response.getContent()
    def jsonParser = new groovy.json.JsonSlurperClassic()

    def build_obj = jsonParser.parseText(content)

    debug("[APPVEYOR] Build ID: ${build_obj.buildId}");

    def appveyor_status = 'n/a';
    def appveyor_finished = false;


    while (appveyor_finished != true) {
        response = httpRequest(
            url: "https://ci.appveyor.com/api/projects/${accountName}/${projectSlug}/history?recordsNumber=5",
            customHeaders: [
                [name: 'Authorization', value: "Bearer ${appveyor_token}"],
                [name: 'Accept', value: 'application/json']
            ]
        )

        content = response.getContent();

        debug("[APPVEYOR] ${content}")


        def build_data = new groovy.json.JsonSlurperClassic().parseText(response.getContent())

        build_data.builds.each{ b ->
            if (b.buildId == build_obj.buildId) {
                debug("[APPVEYOR] Build status: ${b.status}")
                if (b.status == "queued" || b.status == "running") {
                    return;
                } else {
                    appveyor_finished = true;
                    appveyor_status   = b.status;
                }
            }
        }

        sleep(5)
    }

    debug("[APPVEYOR] Build completed - status: ${appveyor_status}")

    if (appveyor_status != "success") {
        error("Appveyor build failed.")
    }
}

node('master') {

    def PROJECT_OWNER = 'psistats'
    def PROJECT_NAME  = 'citest'

    def APPVEYOR_OWNER = 'alex-dow'
    def APPVEYOR_TOKEN = 'appveyor-token'
    def APPVEYOR_NAME  = PROJECT_NAME

    def PY35_TOOL_NAME = 'psikon-py35'
    def PY36_TOOL_NAME = 'psikon-py36'

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
            }
            stage('test-py35') {
                withPythonEnv(PY35_TOOL_NAME) {
                    pysh 'pip install tox'
                    pysh 'tox -e py35'
                }
            }
            stage('test-py36') {
                withPythonEnv(PY36_TOOL_NAME) {
                    pysh 'pip install tox'
                    pysh 'tox -e py36'
                }
            }
            stage('test-w32') {
                withCredentials([string(credentialsId: APPVEYOR_TOKEN, variable: 'TOKEN')]) {
                    run_appveyor(TOKEN, APPVEYOR_OWNER, APPVEYOR_NAME, scmVars.GIT_BRANCH, scmVars.GIT_COMMIT)
                }
            }
            stage('test-coverage') {
                withPythonEnv(PY35_TOOL_NAME) {
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
