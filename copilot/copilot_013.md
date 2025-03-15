<git-open-source> #010:

---

### Raw Prompt Input
```
$ git push
ERROR: Permission to ThomasAFink/orbital-mechanics.git denied to fekerr.
fatal: Could not read from remote repository.
so -- git push defaults to origin?
I should change the origin then, to be my repo?
```

---

### Restated Input Prompt
You've encountered an error when running `git push` because it tried to push to the remote "origin" (which still points to the original repository `ThomasAFink/orbital-mechanics.git`), and you don't have permission to push to that repository. You understand that `git push` defaults to the remote "origin", and are asking if you should change "origin" to point to your new repository instead.

---

### Detailed Response

Yes, when you run the command `git push` without specifying a remote, Git defaults to pushing to the remote named **origin**. In your case, **origin** points to the original repository (`ThomasAFink/orbital-mechanics.git`), and you don’t have the proper access rights to push there. That’s why you encountered the error:

```
ERROR: Permission to ThomasAFink/orbital-mechanics.git denied to fekerr.
```

Since you want to push your changes to your new repository (where you have permission), you have two main options:

1. **Explicitly Push to the New Remote:**  
   You can continue using your separate remote named **neworigin**. Instead of running `git push`, run:
   ```bash
   git push neworigin main
   ```
   This command tells Git to push the current branch (`main`) to the remote named **neworigin**—which is your new repo (`git@github.com:fekerr/orbital-new.git`).

2. **Change the Remote "origin":**  
   If you prefer that all your push commands go to your new repository by default, you can change the URL for the existing **origin** remote. This way, `git push` will automatically push to your new repository. You can do this by running:
   ```bash
   git remote set-url origin git@github.com:fekerr/orbital-new.git
   ```
   After running that command, check your remotes again with:
   ```bash
   git remote -v
   ```
   You should see that **origin** now points to your new repository.

---

### Recommendations

- **Retaining Original Repository Link:**  
  If you want to preserve the link to the original repository (for attribution or future reference), you might prefer to leave **origin** as is and use **neworigin** for pushing your changes.  
  Whenever you need to push, use:
  ```bash
  git push neworigin main
  ```

- **Switching Default Remote:**  
  If you're certain that your work is migrating entirely to your new repository and you don't need to interact with the original one, updating **origin** is perfectly acceptable.

- **Documentation:**  
  In your `work_history.md` or your project README, consider noting that your repository started from the original `ThomasAFink/orbital-mechanics.git` but has now transitioned to your own repository (`fekerr/orbital-new.git`). This preserves proper attribution and clearly explains your workflow.

---

### Next Steps

- **If You Want to Change "origin":**  
  Run:
  ```bash
  git remote set-url origin git@github.com:fekerr/orbital-new.git
  ```
  Then, simply run:
  ```bash
  git push
  ```
  And Git will push to your new repo by default.

- **If You Prefer to Explicitly Push to "neworigin":**  
  Continue to run:
  ```bash
  git push neworigin main
  ```

---

### References, URLs, and Follow-Up Topics

- **Git Remote Documentation:**  
  [Git Remote - Git SCM](https://git-scm.com/docs/git-remote) explains how to manage remotes.
- **GitHub CLI - Repository Creation:**  
  [GitHub CLI docs](https://cli.github.com/manual/repo_create) for creating new repositories via `gh`.
- **Best Practices in Open Source Attribution:**  
  Documenting the transition and maintaining history using files like `work_history.md` is a common open source practice.

---

**Summary:**  
`git push` defaults to **origin**, which in your case is still the original repo where you lack push permissions. You can either change the "origin" remote to your new repository or explicitly push to **neworigin**. Choose the method that best suits your long-term workflow.

Let me know if you need further clarification or assistance with your Git workflow!
