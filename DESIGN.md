# Functional spec and design

## Intro

I'm using this repo to test some Travis workflows for a different project. This
one is zero risk, while that one runs the risk of overwriting data that should
not be modified.

I'll create mocks of the other repo's functionaliy, with the goal of walking
all paths. Put another way, [..]

The other repo has three named branches, corresponding to their three
environments: `dev` (`env:dev`), stage (`env:stg`), and `master` (`env:prd`).
It also has feature branches that feed into `dev`.

Their current Travis configuration impedes this effort. All branches build, but
the logic I need to verify only runs on merge to one of the environment
branches. I can't test and fix without pushing to dev. By then it's too late.

For that reason, I am setting up this repo. It will emulate the current
configuration, and test all code paths. All I need to do is send up a flare on
each code path. The actions taking place in the original repo don't matter so
much. What matters is that only that they only run when they're supposed to.


## Functional spec

Here's the current `.travis.yml`:


```yaml
language: python
python:
  - 3.7
before_install:
  - bash write_pip_config.sh
install:
  - pip install -r dev-requirements.txt
script:
  - invoke test
  - bash docker.sh update_image
  # UNDO
  # Temporary for testing. This will be a pre-task of deploy-jobs.
  - invoke update-job-configs
deploy:
  provider: script
  script:
    - invoke deploy-jobs
  on:
    all_branches: true
    condition: $TRAVIS_BRANCH =~ ^(dev|stage|master)$
env:
  global:
    # ARTIFACTORY_USERNAME
    - secure: redacted
    # ARTIFACTORY_PASSWORD
    - secure: redacted
```

* `bash docker.sh update_image` checks if there's a Docker image in Artifactory
  matching the `package_version` in the Dockerfile in the repo root. Right now
  we've only got (Docker) repo `docker-data-dev`, so this command should
  execute based on environment. Here's the first limitation. How to tell Travis
  which environment we're targeting?

* Should I add a `TARGET_ENVIRONMENT` environment variable? 

  Barring that, since we don't have an environment 

  # UNDO
  # Temporary for testing. This will be a pre-task of deploy-jobs.
  - invoke update-job-configs

The `UNDO` is coming out. `invoke` task `update-job-configs` will be a pre-task
of `deploy-jobs`. This is the first complication that I may reconsider. I'm not
sure they should be bound together that way. `update-job-configs` modifies
Databricks job configs (JSON files) to add Artifactory credentials for pulling
custom Docker images.


