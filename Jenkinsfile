pipeline {
    agent any

    environment {
        APP_IMAGE = "employee-app"
        DB_IMAGE = "postgres:14"
        DB_CONTAINER = "pg_container"
        APP_CONTAINER = "app_container"
        DB_NAME = "employees_db"
        DB_USER = "postgres"
        DB_PASS = "postgres"
    }

    stages {
        stage('Build App Image') {
            steps {
                bat "docker build -t %APP_IMAGE% ."
            }
        }

        stage('Start Database') {
            steps {
                script {
                    // stop old container if exists
                    bat "docker rm -f %DB_CONTAINER% || exit 0"

                    // start new postgres
                    bat """
                    docker run -d --name %DB_CONTAINER% ^
                        -e POSTGRES_DB=%DB_NAME% ^
                        -e POSTGRES_USER=%DB_USER% ^
                        -e POSTGRES_PASSWORD=%DB_PASS% ^
                        -p 5432:5432 ^
                        %DB_IMAGE%
                    """

                    // wait for DB to initialize (Windows sleep)
                    bat "ping -n 15 127.0.0.1 >NUL"
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    // get list of migration files in Windows way
                    def migrationFiles = bat(script: "dir /B migrations\\*.sql", returnStdout: true).trim().split("\r\n")

                    for (f in migrationFiles) {
                        bat "docker exec -i %DB_CONTAINER% psql -U %DB_USER% -d %DB_NAME% -f /migrations/${f}"
                    }
                }
            }
        }

        stage('Start App') {
            steps {
                bat "docker rm -f %APP_CONTAINER% || exit 0"

                bat """
                docker run -d --name %APP_CONTAINER% ^
                    --link %DB_CONTAINER%:db ^
                    -p 5000:5000 ^
                    %APP_IMAGE%
                """
            }
        }
    }
}
