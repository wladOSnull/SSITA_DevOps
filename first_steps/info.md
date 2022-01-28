# GitFlow - first steps

- clone repo from github

  ```bash
  ~ cd gitflow
  ~ git clone git@github.com:wladOSnull/first_jira.git
  ~ cd first_jira
  ```

- add new file (for hw1 python) and then

  ```bash
  ~ git status
  ~ git add .
  ~ git status
  
  ~ git commit -m "file: new python file hw1"
  ~ git status
  ```

- add new folder + move hw1.py to the folder and then

  ```bash
  ~ git status
  ~ git commit -m "folder: new folder + move file python hw1"
  ~ git status
  ```

- check status

  ```bash
  ~ git log --oneline
  ~ git branch
  ```

- sync local and remote repos

  ```bash
  ~ git push origin main
  ~ git status
  ```

- check the repo on github

- create new branch
  
  ```bash
  # list branches
  # for remote: git branch -r
  # for all: git branch -a
  # for local: git branch
  ~ git branch
  ~ git branch python_hw2
  ~ git branch -a

  ~ git checkout python_hw2
  ~ git branch
  ```

- add new folder and files for hw2 python (*.py + hw2_example.json) and then

  ```bash
  ~ git status
  ~ git add .
  ~ git commit -m "folder & file: add new folder and important files for hw2 python"

  ~ git status
  ~ git loag --oneline
  ```

- push new branch to remote

  ```bash
  ~ git push origin python_hw2
  ```

- add new minor files for hw2 and then
  ```bash
  ~ git add .
  ~ git commit -m "file: add new minor files for hw2 python"
  ~ git status

  ~ git push origin python_hw2
  ~ git log --oneline
  ```
  ![image](1_merge.png?raw=true "screenshot of merging python_hw2 into main")

- merge main and python_hw2 locally
  
  ```bash
  ~ git branch
  ~ git checkout main
  ~ git merge python_hw2

  ~ git status
  ~ git log --oneline

  ~ git push origin main

  ~ git status
  ~ git log --oneline
  ```
  ![image](2_final.png?raw=true "screenshot of final pushing")

## Appendix:  
  
  Some commands ...

  ```bash
  ~ git reset HEAD -- .  
  ~ git ls-files  
  ```