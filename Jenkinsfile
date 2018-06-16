def debug(msg) {
    echo "[DEBUG] ${msg}"
}

def should_skip() {
    result = sh (script: "git log -1 | grep '.*\\[ci skip\\].*'", returnStatus: true)
    if (result == 0) {
        env.CI_SKIP = "true"
    }
}

def should_deloy() {
    result = sh (script: "git log -1 | grep .*\\[deploy\\].*'", returnStatus: true)
    if (result == 0) {
        env.DEPLOY = "true"
    }
}

def download_appveyor_artifacts(build_version, accountName, projectSlug) {

  debug('[APPVEYOR] Downloading artifacts');

  def content = httpRequest(
    url: "https://ci.appveyor.com/api/projects/${accountName}/${projectSlug}/build/${build_version}",
    customHeaders: [
      [name: 'Accept', value: 'application/json']
    ]
  );
  debug(groovy.json.JsonOutput.prettyPrint(content.getContent()));
  def build_obj = new groovy.json.JsonSlurperClassic().parseText(content.getContent());

  def job_id = build_obj.build.jobs[0].jobId;

  def artifact_response = httpRequest(
    url: "https://ci.appveyor.com/api/buildjobs/${job_id}/artifacts",
    customHeaders: [
      [name: 'Accept', value: 'application/json']
    ]
  );
  
  def artifact_response_content = artifact_response.getContent();
  debug(artifact_response_content);

  build_obj = new groovy.json.JsonSlurperClassic().parseText(artifact_response_content);
  
  build_obj.each {
    debug("[APPVEYOR] Artifact found: ${it.fileName}");
  };
  

}

def run_appveyor(appveyor_token, accountName, projectSlug, branch, commitId) {
    debug('[APPVEYOR] Starting')

    def request = [:]
    request['accountName'] = accountName
    request['projectSlug'] = projectSlug
    request['environmentVariables'] = env.environment;

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

    def content = build_response.getContent();
    debug(groovy.json.JsonOutput.prettyPrint(content));


    def build_obj = new groovy.json.JsonSlurperClassic().parseText(content)

    debug("[APPVEYOR] Build ID: ${build_obj.buildId}");
    debug("[APPVEYOR] Build Version: ${build_obj.version}");

    def appveyor_status = 'n/a';
    def appveyor_finished = false;


    while (appveyor_finished != true) {
        def status_response = httpRequest(
            url: "https://ci.appveyor.com/api/projects/${accountName}/${projectSlug}/build/${build_obj.version}",
            httpMode: 'GET',
            customHeaders: [
                [name: 'Authorization', value: "Bearer ${appveyor_token}"],
                [name: 'Accept', value: 'application/json']
            ]
        )

        def status_content = status_response.getContent()
        debug(groovy.json.JsonOutput.prettyPrint(status_content));
        def build_data = new groovy.json.JsonSlurperClassic().parseText(status_content)

        if (build_data.build.status == "queued" || build_data.build.status == "running") {
          debug("[APPVEYOR] Waiting ... ");
          sleep(5);
        } else {
          appveyor_finished = true;
          appveyor_status   = build_data.build.status;
        }
    }

    debug("[APPVEYOR] Build completed - status: ${appveyor_status}")

    if (appveyor_status != "success") {
        error("Appveyor build failed.")
    }

    return build_obj.version;
}



node('master') {

    def PROJECT_OWNER = 'psistats'
    def PROJECT_NAME  = 'citest'

    def APPVEYOR_OWNER = 'alex-dow'
    def APPVEYOR_TOKEN = 'appveyor-token'
    def APPVEYOR_NAME  = PROJECT_NAME

    def PY35_TOOL_NAME = 'psikon-py35'
    def PY36_TOOL_NAME = 'psikon-py36'

    // authenticationToken('secret-test-citest')

    properties([
        pipelineTriggers([
            [$class: 'GenericTrigger',
                genericVariables: [
                    [expressionType: 'JSONPath', key: 'APPVEYOR_ARTIFACTS', value: '$.artifacts[*]'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR', value: '$.environmentVariables.appveyor'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_ID', value: '$.buildId'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_NUMBER', value: '$.buildNumber'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_BUILD_VERSION', value: '$.buildVersion'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_COVERAGE_REPORT', value: '$.environmentVariables.COVERAGE'],
                    [expressionType: 'JSONPath', key: 'APPVEYOR_NEW_ARTIFACT', value: '$.environmentVariables.NEW_ARTIFACT']
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

                stage('appveyor') {
                    withCredentials([string(credentialsId: APPVEYOR_TOKEN, variable: 'TOKEN')]) {
                        build_version = run_appveyor(TOKEN, APPVEYOR_OWNER, APPVEYOR_NAME, scmVars.GIT_BRANCH, scmVars.GIT_COMMIT)
                        download_appveyor_artifacts(build_version, APPVEYOR_OWNER, APPVEYOR_NAME);
                    }
                }


                if (scmVars.GIT_BRANCH == 'develop') {
                    // A commit to branch means changing the build number
                    stage('set-build-number') {
                        withPythonEnv(PY35_TOOL_NAME) {
                            pysh "python building/change_version --set-build=${env.BUILD_NUMBER}"
                        }
                        sh 'git commit -am "Increase build number [deploy]"'
                        sh 'git push'
                    }
                    /*
                    stage('build-debian') {
                        withPythonEnv(PY35_TOOL_NAME) {
                            pysh "python building/build_deb.py"
                        }
                    }
                    */
                }
            }
        } else if (env.APPVEYOR == 'True')  {

            stage('appveyor-download-artifacts') {

                debug("Artifacts: ${env.APPVEYOR_ARTIFACTS}")

                def artifacts = new groovy.json.JsonSlurperClassic().parseText(env.APPVEYOR_ARTIFACTS)
                for (int i = 0; i < artifacts.size(); i++) {
                    def artifact = artifacts[i]
                    pysh "python building/download_appveyor_artifact.py \"${artifact.url}\" \"${artifact.fileName}\""
                }
            }

            if (env.APPVEYOR_NEW_ARTIFACT == 'true') {
                stage('deploy-appveyor-build') {
                    withPythonEnv(PY35_TOOL_NAME) {
                        archiveArtifacts artifacts: "artifact_download/*.exe"
                    }
                }
            }

            if (env.APPVEYOR_COVERAGE == 'true') {
                stage('publish-all-coverage') {
                    withPythonEnv(PY35_TOOL_NAME) {
                        sh 'cp artifact_dowloads/coverage.dat reports/coverage/raw_data/coverage-win.dat'
                        pysh 'tox -e coverage'
                        pysh 'coverage combine reports/coverage/raw_data'
                        pysh 'coverage report'
                        pysh 'coverage html'
                        pysh 'coverage xml'
                    }

                    step([$class: 'CoberturaPublisher',
                        autoUpdateHealth: false,
                        autoUpdateStability: false,
                        coberturaReportFile: 'reports/coverage/coverage.xml',
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
}
