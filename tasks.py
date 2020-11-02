from invoke import task

@task
def test(c):
    print("Hello from tasks.py - test")

@task
def update_job_configs(c):
    print("Hello from tasks.py - update_job_configs")

@task
def deploy_jobs(c):
    print("Hello from tasks.py - deploy_jobs")
