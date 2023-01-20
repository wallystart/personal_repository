import json
import requests

# replace with job id
JOB_ID = 316
# replace with token
AUTHORIZATION = 'TOKEN'
# replace with URL
WORKSPACE_URL = '"https://TOCOMPLETE.azuredatabricks.net/api/2.0/jobs/run-now'


def execute_job(notebook_params, job_id=JOB_ID):
    '''
    Perform job execution and return run_id and number_in_job

            Parameters:
                    notebook_params (dict): notebook parameters
                    job_id (int): job id to execute

            Returns:
                    run_id, number_in_job (tuple)
    '''

    payload={
        "job_id": job_id,
        "notebook_params": notebook_params
    }
    headers = {
        'Authorization': AUTHORIZATION,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", WORKSPACE_URL, headers=headers, data=json.dumps(payload))
    run_id = response.json()["run_id"]
    number_in_job = response.json()["number_in_job"]

    return run_id, number_in_job


def get_status_execution(run_id, number_in_job, job_id=JOB_ID):
    '''
    Return job status

            Parameters:
                    run_id (dict): run id
                    number_in_job (int): -
                    job_id (int): job id

            Returns:
                    status (str): running status
    '''

    payload = {
        'job_id': job_id,
        'run_id': run_id,
        'number_in_job': number_in_job
    }
    headers = {
        'Authorization': AUTHORIZATION,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", WORKSPACE_URL, headers=headers, data=json.dumps(payload))
    status = response.json()["metadata"]["state"]

    return status


def get_results_html(run_id, views_to_export="ALL"):
    '''
    Returns an html of a view of a notebook

            Parameters:
                    run_id (dict): run id
                    views_to_export (str): name of view or 'ALL'

            Returns:
                    response (dict): -
    '''

    payload={
        'run_id': run_id,
        'views_to_export': views_to_export
    }
    headers = {
        'Authorization': AUTHORIZATION
    }

    response = requests.request("GET", WORKSPACE_URL, headers=headers, data=json.dumps(payload))

    return response
