# Git Practice Exercises

Work through these in order. Each exercise lists the goal, the commands, and a
**Check** so you know it worked. Expect about 60 to 90 minutes for Part A if you
are new to Git; Part B takes about 15 minutes with a partner.

Commands are typed in a terminal (macOS Terminal, Linux shell, Git Bash on
Windows, or a cluster login node). Anything in `CAPITALS` should be replaced
with your own value.

> **Before you start:** complete the one-time setup in the Git SOP (install
> Git, set your name and email, and connect to GitHub with an SSH key).
> Check with `git --version` and `ssh -T git@github.com`.

---

## Part A: Solo exercises (on your own copy)

### Exercise 0: Get your own copy of this repository

You need a copy that you own, so you can push to it freely.

**Option 1, template (recommended).** On the group's `git-practice-compchem`
page on GitHub, click **Use this template → Create a new repository**.
Choose your own account as the owner, keep the name `git-practice-compchem`,
and **tick "Include all branches"**. Click **Create repository**.

**Option 2, fork.** Click **Fork**. On the next page **untick "Copy the main
branch only"** so the `exercise/conflict` branch comes with it.

Then clone *your* copy (use the green **Code** button → **SSH** to copy the URL):

```bash
git clone git@github.com:YOUR-USERNAME/git-practice-compchem.git
cd git-practice-compchem
```

**Check:** `git remote -v` shows your username in the URL.

---

### Exercise 1: Look around

```bash
git status                       # where am I, and what has changed?
git log --oneline                # project history, newest first
git log --oneline --graph --all  # history of every branch, as a graph
git branch -a                    # local and remote branches
git show HEAD                    # the most recent commit in detail
```

Questions to answer for yourself:

1. How many commits are on `main`?
2. Which branch exists on the remote that is not on `main`?
3. What did the most recent commit change?

**Check:** `git status` says `nothing to commit, working tree clean`.

---

### Exercise 2: Your first commit

Add a file about yourself to the `members/` folder.

```bash
cp members/TEMPLATE.md members/YOUR-GITHUB-USERNAME.md
# Edit the new file in any text editor (nano, VS Code, vim...) and fill it in.

git status                                 # file shows as "Untracked"
git add members/YOUR-GITHUB-USERNAME.md    # stage it
git status                                 # now under "Changes to be committed"
git commit -m "Add member profile for YOUR NAME"
git log --oneline -3                       # your commit is at the top
git push                                   # send it to GitHub
```

**Check:** refresh your repository page on GitHub and open the `members/`
folder. Your file is there.

---

### Exercise 3: Find and fix a bug using history

The unit-conversion tests fail. Somebody broke something.

```bash
python tests/test_units.py
python src/analyze_energies.py data/energies.csv
```

Two tests fail, and the gauche conformers of butane come out about 0.75
kcal/mol above anti, which is too high. Use Git to find out *when* and *how*
the bug appeared:

```bash
git log --oneline -- src/units.py           # commits that touched this file
git diff v0.1 HEAD -- src/units.py          # what changed since the v0.1 tag?
git blame -L 9,9 src/units.py               # who last changed line 9, and in which commit?
git log -S "672.509474" --oneline -- src/units.py   # which commit introduced this exact text?
```

You should discover that a commit called *"Tidy unit constants and add
docstrings"* changed `627.509474` to `672.509474` (two digits swapped).

Fix it: open `src/units.py`, change `672.509474` back to `627.509474`, save.

```bash
git diff                                    # review your change before committing
python tests/test_units.py                  # should now print: 5 passed, 0 failed
git add src/units.py
git commit -m "Fix transposed digits in Hartree to kcal/mol constant"
git push
```

**Check:** the tests pass, and `analyze_energies.py` now reports about
0.695 kcal/mol for the gauche conformers.

> **Lesson:** a small, well-described commit history turns "something is wrong
> somewhere" into "this exact line changed in this exact commit."

---

### Exercise 4: Keep calculation outputs out of Git (`.gitignore`)

```bash
bash scripts/fake_calculation.sh
git status
```

Git now sees a new `runs/` folder full of logs, checkpoints, scratch files,
and scheduler output. You want to keep the **input file** (`water_opt.inp`)
but ignore everything that can be regenerated.

Open `.gitignore` and add these lines under the *Computational chemistry
outputs* heading:

```gitignore
*.log
*.chk
*.fchk
*.gbw
*.tmp
slurm-*.out
scratch/
```

Then:

```bash
git status                                         # only water_opt.inp (and .gitignore) remain
git check-ignore -v runs/water_opt/water_opt.chk   # shows which rule ignores the file
git add .gitignore runs/water_opt/water_opt.inp
git commit -m "Ignore calculation outputs and track water_opt input"
git push
```

**Check:** `git status` is clean, but `ls runs/water_opt` still shows every
file on your disk. Ignored files are not deleted, only hidden from Git.

> The SOP package includes a fuller `compchem.gitignore` covering Gaussian,
> ORCA, VASP, CP2K, Q-Chem, GROMACS, AMBER, and LAMMPS.

---

### Exercise 5: Work on a branch and open a pull request

Never develop directly on `main` in a shared project. Use a branch.

```bash
git switch main
git pull                                    # always start from the latest main
git switch -c add-ammonia                   # create and switch to a new branch
```

Create `data/molecules/ammonia.xyz` with this content:

```text
4
Ammonia, approximate geometry (Angstrom)
N     0.000000     0.000000     0.116489
H     0.000000     0.939731    -0.271807
H     0.813831    -0.469865    -0.271807
H    -0.813831    -0.469865    -0.271807
```

```bash
python src/xyz_tools.py data/molecules/ammonia.xyz   # should report formula H3N
git add data/molecules/ammonia.xyz
git commit -m "Add ammonia geometry"
git push -u origin add-ammonia                       # -u links the branch to GitHub
```

On GitHub you will see a banner offering **Compare & pull request**. Click it,
write a short description, and click **Create pull request**. Look at the
**Files changed** tab: this is what a reviewer sees. Then click **Merge pull
request → Confirm merge**, and **Delete branch**.

Back in your terminal:

```bash
git switch main
git pull                                    # bring the merged work down
git branch -d add-ammonia                   # tidy up the local branch
```

**Check:** `ls data/molecules` on `main` now includes `ammonia.xyz`.

---

### Exercise 6: Resolve a merge conflict

A labmate changed the basis set on the `exercise/conflict` branch while
`main` was changed to something else. Merge their work in:

```bash
git switch main
git merge origin/exercise/conflict
```

> If Git says `origin/exercise/conflict` does not exist (you created your copy
> without all branches), run `bash scripts/create_conflict_branch.sh` and then
> `git merge exercise/conflict-local` instead. In that case the `HEAD` side
> of the conflict will read `basis: def2-SVP`.

Git stops and reports `CONFLICT (content): Merge conflict in
config/calc_settings.yaml`. Open that file. You will see:

```text
<<<<<<< HEAD
basis: 6-31G(d)
=======
basis: def2-TZVP
>>>>>>> origin/exercise/conflict
```

The part between `<<<<<<<` and `=======` is your version (`main`). The part
between `=======` and `>>>>>>>` is the incoming version. Notice that the
branch's *other* change (`max_scf_cycles: 500`) merged automatically, because
nobody else had touched that line.

Decide the correct result. Here, the group agreed production runs use
def2-TZVP, so edit the block until only this line remains (delete all three
marker lines):

```text
basis: def2-TZVP
```

```bash
git status                                 # file listed under "Unmerged paths"
git add config/calc_settings.yaml          # mark the conflict as resolved
git commit --no-edit                       # finish the merge with the default message
git log --oneline --graph -6               # see the two lines of history join
git push
```

**Check:** `grep -n "<<<<<<<\|>>>>>>>" config/calc_settings.yaml` prints
nothing.

> **Escape hatch:** if a merge goes badly before you commit, `git merge --abort`
> returns everything to how it was before you started.

---

### Exercise 7: Undo things safely

**a. Throw away an unwanted edit (not yet staged)**

```bash
echo "oops" >> README.md
git status
git restore README.md          # discard the change; the file is back to the last commit
```

**b. Unstage a file you added by mistake**

```bash
echo "temporary notes" > notes.txt
git add notes.txt
git restore --staged notes.txt # unstage, but keep the file on disk
rm notes.txt
```

**c. Fix the message of your last commit (only if not yet pushed)**

```bash
echo "Practice line" >> members/YOUR-GITHUB-USERNAME.md
git commit -am "Updte profile"             # typo on purpose
git commit --amend -m "Update profile"     # rewrite the last commit's message
git push
```

**d. Undo a commit that is already pushed**

```bash
echo "basis_override: STO-3G   # terrible idea" >> config/calc_settings.yaml
git commit -am "Switch to minimal basis"
git push
git log --oneline -2                       # copy the hash of "Switch to minimal basis"
git revert HASH                            # makes a NEW commit that undoes it
                                           # (an editor opens: save and close to accept the message)
git push
```

**Check:** `git log --oneline -4` shows both the bad commit and the
`Revert "Switch to minimal basis"` commit. On shared branches, `revert` is
the safe way to undo because it never rewrites history others may have pulled.

---

### Exercise 8: Travel through history and tag a version

```bash
git show v0.1 --stat                       # what the v0.1 tag points to
git show v0.1:src/units.py | head -12      # view an old version of a file
git diff v0.1 HEAD --stat                  # everything that changed since v0.1

git switch --detach v0.1                   # temporarily step back in time
ls                                         # no tests/ or scripts/ yet (untracked runs/ stays put)
git switch main                            # come back to the present
```

Now tag the current state, the way you would when submitting a paper:

```bash
git tag -a v1.0 -m "Version used for practice manuscript submission"
git push origin v1.0
git tag                                    # list all tags
```

**Check:** your repository page on GitHub lists `v1.0` under **Tags**.

---

### Exercise 9 (bonus): Record provenance for a calculation

```bash
bash scripts/record_provenance.sh runs/water_opt
```

This writes `runs/water_opt/provenance.txt` with the exact commit hash. Now
edit any tracked file without committing and run it again. It warns that
the result came from uncommitted code. Restore the file afterwards with
`git restore`. Look at `scripts/submit_job.sh` to see how this goes into a
SLURM job.

---

## Part B: Team exercise (on the group's shared copy)

This part uses the **group's** repository, where the maintainer has added you
as a collaborator. Work with a partner.

1. Clone the group copy into a *different* folder from your own copy:
   ```bash
   cd ~
   git clone git@github.com:GROUP-ORG/git-practice-compchem.git group-practice
   cd group-practice
   ```
2. Create a branch named after yourself and add your profile:
   ```bash
   git switch -c add-profile-YOUR-GITHUB-USERNAME
   cp members/TEMPLATE.md members/YOUR-GITHUB-USERNAME.md
   # edit the file
   git add members/YOUR-GITHUB-USERNAME.md
   git commit -m "Add member profile for YOUR NAME"
   git push -u origin add-profile-YOUR-GITHUB-USERNAME
   ```
3. Open a pull request on GitHub and, under **Reviewers**, request your partner.
4. Review your partner's pull request: open **Files changed**, leave at least
   one comment, then **Approve**.
5. Merge your own pull request once it is approved, and delete the branch.
6. Bring everyone's work down:
   ```bash
   git switch main
   git pull
   ls members/
   ```

**Check:** after a few minutes, `members/` contains a file for every person
in the room, and nobody had a conflict, because everybody edited a different
file.

**Optional partner conflict.** You and your partner each make a branch,
change the *same* line of `config/calc_settings.yaml` to different values,
and open pull requests. Merge one. GitHub will report that the other has
conflicts. Its author resolves them locally:

```bash
git switch YOUR-BRANCH
git pull origin main       # brings main in and shows the conflict
# fix the file, then:
git add config/calc_settings.yaml
git commit --no-edit
git push
```

---

## Stuck?

| Symptom | Fix |
|---|---|
| `Permission denied (publickey)` | Your SSH key is not set up. See the SOP, section 3 |
| `fatal: not a git repository` | You are not inside the repository folder. `cd git-practice-compchem` |
| A strange full-screen editor opened | It is probably vim. Type `:wq` and press Enter to save and quit |
| `rejected ... (fetch first)` when pushing | Someone pushed before you. Run `git pull`, then `git push` |
| `Your branch is ahead of 'origin/main'` | You have commits that are not on GitHub yet. Run `git push` |
| Everything is a mess | Your copy is disposable. Delete the folder and clone again |
