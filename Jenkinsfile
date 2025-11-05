pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\win10\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        PIP_EXE = 'C:\\Users\\win10\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe'
        JUPYTER_ALLOW_INSECURE_WRITES = 'true'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '🔁 Cloning source code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                echo '🐍 Verifying Python and pip installations...'
                bat """
                "%PYTHON_EXE%" --version
                "%PIP_EXE%" --version
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                bat """
                "%PIP_EXE%" install --upgrade pip
                "%PIP_EXE%" install -r requirements.txt
                "%PIP_EXE%" install pywin32
                """
            }
        }

        stage('Train Model') {
            steps {
                echo '🧠 Training model...'
                bat """
                "%PYTHON_EXE%" train_model.py > training_output.log 2>&1
                """
            }
        }

        stage('Run Notebook') {
            steps {
                echo '📓 Executing Jupyter notebook (with security bypass enabled)...'
                bat """
                set JUPYTER_ALLOW_INSECURE_WRITES=true
                "%PYTHON_EXE%" -m jupyter nbconvert --to notebook --execute ipl_score_predictor.ipynb --output output_notebook.ipynb --log-level=INFO
                "%PYTHON_EXE%" -m jupyter nbconvert --to html output_notebook.ipynb --output output_report.html
                """
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                echo '🧪 Running test suite...'
                bat """
                "%PYTHON_EXE%" -m pytest --maxfail=1 --disable-warnings -q
                """
            }
        }
    }

    post {
        always {
            echo '📦 Archiving build artifacts...'
            archiveArtifacts artifacts: '**/*.html, **/*.log, **/*.pkl', fingerprint: true
        }

        success {
            echo '✅ Build and notebook execution successful!'
        }

        failure {
            echo '❌ Build failed. Check console output for details.'
        }
    }
}
