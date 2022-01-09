:: Initial setup.
@ECHO OFF

:: Change directory to the previous directory.
cd ..

:: Pull from the latest repository.
git pull origin main

:: Run Python Virtual Environment.
:: CALL is used as 'activate' and 'deactivate' is a batch file.
:: This is to prevent the execution stack to be transferred to the 'activate' batch file.
SET PYTHON_VENV=.venv
CALL "%PYTHON_VENV%\Scripts\activate"
python src/main.py
CALL "%PYTHON_VENV%\Scripts\deactivate"
ECHO The CSV file has been written with a suggestion for you!

:: Setting commit message.
:: Before doing this, ensure that you have performed these following operations:
:: 1) git config --global user.name <YOUR_USERNAME>
:: 2) git config --global user.email <YOUR_EMAIL>
:: 3) Make sure that you have configured Git beforehand to use your password via 'git config --global credential.helper store'.
:: 4) You have already configured the repository and the remote origin via 'git init' and 'git remote add origin <YOUR_GITHUB_REPO>'.
:: 5) Alternatively, use SSH (https://stackoverflow.com/questions/8588768/how-do-i-avoid-the-specification-of-the-username-and-password-at-every-git-push).
SET COMMIT_MESSAGE=chore: Character/anime suggestion on %date%
git add data/
git commit -m "%COMMIT_MESSAGE%"
git push --set-upstream origin main
ECHO Committed successfully with commit message: %COMMIT_MESSAGE%
