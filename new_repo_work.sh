# Check current remotes:
git remote -v >> new_repo_work.md

# Add a new remote (e.g., "neworigin"):
# git remote add neworigin https://github.com/yourusername/orbital-new.git
git remote add neworigin git@github.com:fekerr/orbital-new.git

# To push to the new remote:
# git push neworigin master
git push neworigin main
