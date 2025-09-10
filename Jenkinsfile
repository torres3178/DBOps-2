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
                echo "Building app Docker image..."
                bat "docker build -t %APP_IMAGE% ."
            }
        }

        stage('Start Database') {
            steps {
                script {
                    echo "Stopping old DB container if exists..."
                    bat "docker rm -f %DB_CONTAINER% || exit 0"

                    echo "Starting new Postgres container..."
                    bat """
                    docker run -d --name %DB_CONTAINER% ^
                        -e POSTGRES_DB=%DB_NAME% ^
                        -e POSTGRES_USER=%DB_USER% ^
                        -e POSTGRES_PASSWORD=%DB_PASS% ^
                        -p 5432:5432 ^
                        -v "%cd%\\migrations:/migrations" ^
                        %DB_IMAGE%
                    """

                    echo "Waiting 20 seconds for DB to initialize..."
                    bat "ping -n 20 127.0.0.1 >NUL"
                }
            }
        }

        stage('Apply Migrations') {
    steps {
        script {
            echo "Listing migration files..."

            // Get list of migration files relative to workspace
            def migrationFiles = bat(
                script: 'dir /B "migrations\\*.sql"',
                returnStdout: true
            ).trim().split("\r\n")

            echo "Applying migrations..."
            for (f in migrationFiles) {
                f = f.trim() // clean up whitespace
                echo "Running migration: ${f}"
                
                // Run migration inside Docker container using container path
                bat """docker exec -i %DB_CONTAINER% psql -U %DB_USER% -d %DB_NAME% -f "/migrations/${f}" """
            }
        }
    }
}


        stage('Start App') {
            steps {
                echo "Stopping old App container if exists..."
                bat "docker rm -f %APP_CONTAINER% || exit 0"

                echo "Starting App container..."
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
