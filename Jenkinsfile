pipeline {
    agent any

    environment {
        PYTHON_EXE = "C:\\Users\\win10\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        PIP_EXE = "C:\\Users\\win10\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning source code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                echo 'Verifying Python and pip installations...'
                bat '''
                "%PYTHON_EXE%" --version
                "%PIP_EXE%" --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat '''
                "%PIP_EXE%" install --upgrade pip
                "%PIP_EXE%" install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo 'Training model...'
                bat '''
                "%PYTHON_EXE%" train_model.py > training_output.log 2>&1
                '''
            }
        }

        stage('Run Notebook') {
            steps {
                echo 'Executing Jupyter notebook...'
                bat '''
                "%PYTHON_EXE%" -m jupyter nbconvert --to notebook --execute ipl_score_predictor.ipynb --output output_notebook.ipynb
                "%PYTHON_EXE%" -m jupyter nbconvert --to html output_notebook.ipynb --output output_report.html
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                bat '''
                "%PYTHON_EXE%" -m pytest -q
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build succeeded! Archiving artifacts...'
            archiveArtifacts artifacts: 'output_report.html, output_notebook.ipynb, training_output.log, model.pkl, predictions.csv', fingerprint: true
        }
        failure {
            echo '❌ Build failed. Check console output for errors.'
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}
