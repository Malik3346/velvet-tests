pipeline {
    agent any
    stages {
        stage("Clone") {
            steps {
                git branch: "main", url: "https://github.com/Malik3346/velvet-tests.git"
            }
        }
        stage("Deploy") {
            steps {
                sh "cd /home/ubuntu/Velvet && npm install && (pm2 restart backend || pm2 start server.js --name backend)"
            }
        }
        stage("Build") {
            steps {
                sh "docker build -t velvet-tests ."
            }
        }
        stage("Test") {
            steps {
                sh "mkdir -p results && docker run --rm -v \$(pwd)/results:/app/results velvet-tests python -m pytest tests.py -v --tb=short --junit-xml=results/results.xml 2>&1 | tee test-output.txt"
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: "results/results.xml"
            script {
                def authorEmail = sh(script: "git log -1 --format=%ae", returnStdout: true).trim()
                def testOutput = fileExists("test-output.txt") ? readFile("test-output.txt") : "No output"
                def status = currentBuild.result ?: "SUCCESS"
                emailext(subject: "Velvet Tests: ${status} - Build #${env.BUILD_NUMBER}", body: "Build: ${status}\n\n${testOutput}", to: "${authorEmail}", mimeType: "text/plain")
            }
        }
    }
}
