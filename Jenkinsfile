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
                    bat "docker rm -f %DB_CONTAINER% || exit 0"

                    bat """
                    docker run -d --name %DB_CONTAINER% ^
                        -e POSTGRES_DB=%DB_NAME% ^
                        -e POSTGRES_USER=%DB_USER% ^
                        -e POSTGRES_PASSWORD=%DB_PASS% ^
                        -p 5432:5432 ^
                        -v %cd%\\migrations:/migrations ^
                        %DB_IMAGE%
                    """

                    // safer: wait until DB is ready
                    bat '''
                    for /l %%x in (1,1,30) do (
                        docker exec %DB_CONTAINER% pg_isready -U %DB_USER% -d %DB_NAME%
                        if !errorlevel! == 0 (
                            echo Database is ready
                            exit /b 0
                        )
                        ping -n 2 127.0.0.1 >NUL
                    )
                    echo Database did not become ready in time
                    exit /b 1
                    '''
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    def migrationFiles = bat(
                        script: "dir /B migrations\\*.sql",
                        returnStdout: true
                    ).trim().split("\r\n")

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
