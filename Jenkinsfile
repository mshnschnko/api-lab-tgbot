#!/usr/bin/sh

pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Stop old container') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker stop tg_bot || true'
                    } else {
                        bat 'docker stop tg_bot || true'
                    }
                }
            }
        }
        stage('Download git repo') {
            steps {
                echo 'Downloading git repo...'
                script {
                    if (isUnix()) {
                        sh 'rm -rf api-lab-tgbot'
                        sh 'git clone --depth=1 https://github.com/mshnschnko/api-lab-tgbot.git'
                        sh 'rm -rf api-lab-tgbot/.git*'
                        sh 'ls'
                    } else {
                        bat 'rm -rf api-lab-tgbot'
                        bat 'git clone --depth=1 https://github.com/mshnschnko/api-lab-tgbot.git'
                        bat 'rm -rf api-lab-tgbot/.git*'
                        bat 'ls'
                    }
                }
            }
        }
        stage('Getting env and buackup') {
            steps {
                echo 'Getting environment variables and backuping data...'
                withCredentials([file(credentialsId: 'TGBOTENV', variable: 'TGBOTENV'), file(credentialsId: 'DBENV', variable: 'DBENV')]) {
                    script {
                        if (isUnix()) {
                            sh 'cp $TGBOTENV ./.env'
                            sh 'cp $DBENV ./db.env'
                            sh 'mkdir -p ./storage/temp'
                            sh 'mkdir -p ./storage/backup'
                            // sh 'python backup.py'
                        } else {
                            bat 'powershell Copy-Item %TGBOTENV% -Destination ./.env'
                            bat 'powershell Copy-Item %DBENV% -Destination ./db.env'
                            bat 'If Not Exist storage\\temp mkdir storage\\temp'
                            bat 'If Not Exist storage\\backup mkdir storage\\backup'
                            // bat 'python backup.py'
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            withCredentials([string(credentialsId: 'DB_URL', variable: 'DB_URL')]) {
                script {
                    if (isUnix()) {
                        // sh 'cp $ENV ./.env'
                        // sh 'docker stop jenk_bot'
                        sh 'docker build -t mshnschnko/tg_bot_image .'
                        sh 'docker run --name tg_bot -d --rm mshnschnko/tg_bot_image'
                        sh 'touch storage/dump.sql'
                        sh 'docker exec tg_bot bash -c "pg_dump --dbname=$DB_URL -f storage/dump.sql"'
                        sh 'docker exec -d tg_bot bash -c "python backup.py"'
                        // sh 'python main.py'
                    } else {
                        // bat 'powershell Copy-Item %ENV% -Destination ./.env'
                        // bat 'docker stop jenk_bot'
                        bat 'docker build -t mshnschnko/tg_bot_image .'
                        bat 'docker run --name tg_bot -d --rm mshnschnko/tg_bot_image'
                        bat 'If Not Exist storage/dump.sql powershell New-Item storage/dump.sql'
                        bat 'docker exec tg_bot bash -c "pg_dump --dbname=%DB_URL% -f storage/dump.sql"'
                        bat 'docker exec -d tg_bot bash -c "python backup.py"'
                        // bat 'python3 -m venv .venv'
                        // bat '.\\.venv\\Scripts\\activate'
                        // bat 'pip install dotenv yadisk'
                        // bat 'python backup.py'
                        // bat 'docker exec -it mshnschnko/test_hook bash'
                        // bat 'python main.py'
                    }
                }
            }
        }
    }
}