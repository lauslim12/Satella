#!/bin/bash

# Change directory to the previous directory.
cd ..

# Pull from the latest repository.
git pull origin master

# Run Python Virtual Environment.
# We need to use 'bash' to prevent the execution stack switching to the virtual environment.
PYTHON_VENV=venv
source "$PYTHON_VENV/bin/activate"
python3 main.py
deactivate
echo "The CSV file has been written with a suggestion for you!"

# Setting commit message.
# Before doing this, ensure that you have performed these following operations:
# 1) git config --global user.name <YOUR_USERNAME>
# 2) git config --global user.email <YOUR_EMAIL>
# 3) Make sure that you have configured Git beforehand to use your password via 'git config --global credential.helper store'.
# 4) You have already configured the repository and the remote origin via 'git init' and 'git remote add origin <YOUR_GITHUB_REPO>'.
# 5) Alternatively, use SSH (https://stackoverflow.com/questions/8588768/how-do-i-avoid-the-specification-of-the-username-and-password-at-every-git-push).
CURRENT_DATE=$(date -I)
COMMIT_MESSAGE="chore: Character/anime suggestion on $CURRENT_DATE"
git add data/
git commit -m "$COMMIT_MESSAGE"
git push -u origin master
echo "Committed successfully with commit message: $COMMIT_MESSAGE"
