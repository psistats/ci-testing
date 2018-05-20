def debug(msg) {
    echo "[DEBUG] ${msg}"
}

def should_skip() {
    result = sh (script: "git log -1 | grep '.*\\[ci skip\\].*'", returnStatus: true)
    if (result == 0) {
        env.CI_SKIP == "true"
    }
}

def run_appveyor(appveyor_token, accountName, projectSlug, branch, commitId) {
    debug('[APPVEYOR] Starting')

    def request = [:]
    request['accountName'] = accountName
    request['projectSlug'] = projectSlug

    if (branch.startsWith('PR')) {
        debug('Building a pull request')
        def pr = branch.split('-')[1]
        request['pullRequestId'] = pr
    } else {
        debug("Building: ${branch} : ${commitId}")
        request['branch'] = branch
        request['commitId'] = commitId
    }

    def request_body = new groovy.json.JsonBuilder(request).toPrettyString();
    debug("[APPVEYOR] Request body: ${request_body}")

    def build_response = httpRequest(
        url: 'https://ci.appveyor.com/api/builds',
        httpMode: 'POST',
        customHeaders: [
            [name: 'Authorization', value: "Bearer ${appveyor_token}"],
            [name: 'Content-type', value: 'application/json']
        ],
        requestBody: request_body
    )

    def content = build_response.getContent()
    def build_obj = new groovy.json.JsonSlurperClassic().parseText(content)

    debug("[APPVEYOR] Build ID: ${build_obj.buildId}");

    def appveyor_status = 'n/a';
    def appveyor_finished = false;


    while (appveyor_finished != true) {
        def status_response = httpRequest(
            url: "https://ci.appveyor.com/api/projects/${accountName}/${projectSlug}/history?recordsNumber=5",
            httpMode: 'GET',
            customHeaders: [
                [name: 'Authorization', value: "Bearer ${appveyor_token}"],
                [name: 'Accept', value: 'application/json']
            ]
        )

        def status_content = status_response.getContent()
        def build_data = new groovy.json.JsonSlurperClassic().parseText(status_content)

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
                    [expressionType: 'JSONPath', key: 'APPVEYOR_ARTIFACTS', value: '$.artifacts'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR', value: '$.environmentVariables.appveyor'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_ID', value: '$.buildId'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_NUMBER', value: '$.buildNumber'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_VERSION', value: '$.buildVersion']
                ]
            ]
        ])
    ])

    ws("${env.JENKINS_HOME}/workspace/${env.JOB_NAME}") {

        def scmVars;

        if (env.APPVEYOR == null) {
            stage('prepare') {
                scmVars = checkout scm
                should_skip()
            }

            if (env.CI_SKIP != "true") {
                /*
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
                */

                stage('appveyor') {
                    withCredentials([string(credentialsId: APPVEYOR_TOKEN, variable: 'TOKEN')]) {
                        run_appveyor(TOKEN, APPVEYOR_OWNER, APPVEYOR_NAME, scmVars.GIT_BRANCH, scmVars.GIT_COMMIT)
                    }
                }
                /*

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
                }*/




                if (scmVars.GIT_BRANCH == 'develop') {
                    stage('set-build-number') {
                        withPythonEnv(PY35_TOOL_NAME) {
                            pysh "python building/change_version --set-build=${env.BUILD_NUMBER}"
                        }
                        sh 'git commit -am "Increase build number [ci skip]"'
                        sh 'git push'
                    }
                    stage('build-debian') {
                        withPythonEnv(PY35_TOOL_NAME) {
                            pysh "python building/build_deb.py"
                        }
                    }
                }
            }
        } else if (env.APPVEYOR == 'True')  {
            stage('deploy-appveyor-build') {
                debug("Downloading appveyor artifacts")
                if (fileExists("artifact_downloads")) {
                    sh 'rm -rf ./artifact_downloads'
                }
                sh 'mkdir artifact_downloads'
                sh 'wget --no-parent -P ./artifact_downloads https://ci.appveyor.com/api/buildjobs/uuq6l0fv4sresk6m/artifacts/dist%2Fw32installer%2Fcitest_0.1.0.dev999.exe'
                env.APPVEYOR_ARTIFACTS.each{ artifact ->
                    sh "wget ${artifact.url}"
                }
            }
        }
    }
}
