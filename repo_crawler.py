#!/usr/bin/env python
import git
import os
import sys
import datetime
import json
from collections import defaultdict

commits = []
authors = []
emails  = []
args = sys.argv[1:]
if len(args) == 0:
    args = [os.path.abspath(os.path.join('repos', i)) for i in os.listdir('repos/')]
for repo in map(os.path.abspath, args):
    r = git.Repo(repo)
    try:
        r.git.fetch()
    except git.exc.GitCommandError, e:
        pass
    branches = r.git.branch('-r', '--color=never')
    branches = list(set([i.strip() for i in branches.split()])-set(['->', 'origin/HEAD']))
    print branches
    hashes = []
    for b in branches:
        for commit in r.iter_commits(b):
            if commit.hexsha not in hashes:#and (str(commit.author).lower().find('lamberti')>=0 or str(commit.committer.email).lower().find('lamberti')>=0):
                hashes.append(commit.hexsha)
                commits.append(commit.committed_date)
                if commit.author not in authors:
                    authors.append(commit.author)
                if commit.committer.email not in emails:
                    emails.append(commit.committer.email)

d = defaultdict(int)
for c in commits:
    d[c] += 1
with open('data/commits.json', 'w') as f:
    f.write(json.dumps(d))

dates = map(datetime.datetime.fromtimestamp, commits)
hours = map(lambda x: x.strftime("%H"), dates)
for i in range(24):
    print i, hours.count(str(i).zfill(2))
