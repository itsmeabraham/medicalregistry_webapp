def remote = [:]
remote.name = "${JOB_BASE_NAME}"
remote.host = "${SSH_HOST}"
remote.user = "${SSH_USER}"
remote.identityFile = "${SSH_KEY}"
remote.allowAnyHosts = true
pipeline {
    agent any

    stages {
         stage('Setup Environment Files'){
            steps {
                sh '''
                    chmod +x etc/jnk/env.setup.sh
                    etc/jnk/env.setup.sh
                    '''
            }
        }
        stage('Code Deployment'){
            steps {
                script {
                    /* Cleanup remote src */
                    sshCommand remote:remote, command: "rm -rf ${REMOTE_WORKING_DIRECTORY}/src/"

                    /* Copy files to server */
                    sshPut remote: remote, from: 'bin/', into: "${REMOTE_WORKING_DIRECTORY}"
                    sshPut remote: remote, from: 'etc/', into: "${REMOTE_WORKING_DIRECTORY}"
                    sshPut remote: remote, from: 'src/', into: "${REMOTE_WORKING_DIRECTORY}"
                }
            }
        }
        stage('Setup Django'){
            steps {
                script {
                    sshCommand remote:remote, command: "chmod +x ${REMOTE_WORKING_DIRECTORY}/bin/setup.sh"
                    sshCommand remote:remote, command: "chmod +x ${REMOTE_WORKING_DIRECTORY}/bin/gunicorn_start.sh"
                    sshCommand remote:remote, command: "${REMOTE_WORKING_DIRECTORY}/bin/setup.sh"
                }
            }
        }
        stage('PIP update'){
            steps {
                script {
                    sshCommand remote:remote, command: "chmod +x ${REMOTE_WORKING_DIRECTORY}/bin/pip-update.sh"
                    sshCommand remote:remote, command: "${REMOTE_WORKING_DIRECTORY}/bin/pip-update.sh"
                }
            }
        }
        stage('Apply migrations'){
            steps {
                script {
                    sshCommand remote:remote, command: "chmod +x ${REMOTE_WORKING_DIRECTORY}/bin/dj-migrate.sh"
                    sshCommand remote:remote, command: "ls -lsha"
                }
            }
        }
        stage('Collect Statics'){
            steps {
                script {
                    sshCommand remote:remote, command: "chmod +x ${REMOTE_WORKING_DIRECTORY}/bin/dj-collectstatic.sh"
                    sshCommand remote:remote, command: "${REMOTE_WORKING_DIRECTORY}/bin/dj-collectstatic.sh"
                }
            }
        }
        stage('Finish Setup'){
            steps {
                script {
                    sshCommand remote:remote, command: "sudo supervisorctl restart ${DOMAIN}"
                    sshCommand remote:remote, command: "sudo supervisorctl restart ${DOMAIN}-celery"
                }
            }
        }
    }
}
