import os
import requests

GITHUB_TOKEN="${{ secrets.PAT_NAME }}"
# PR_NUMBER=""
GITHUB_REPOSITORY="DaceT/starter-workflows"
GITHUB_HEAD_REF= "main"


pr_number = PR_NUMBER
url = f'https://api.github.com/repos/GITHUB_REPOSITORY}/actions/runs?event=push&status=success&branch={GITHUB_HEAD_REF}&per_page=100'
headers = {
  'Accept': 'application/vnd.github+json',
  'Authorization': f'token {GITHUB_TOKEN}',
}

response = requests.get(url, headers=headers)
response.raise_for_status()

for run in response.json()['workflow_runs']:
  if run['head_branch'] == GITHUB_HEAD_REF: #and run['pull_requests'][0]['number'] == int(pr_number):
    artifacts_url = f'{run["url"]}/artifacts'
    artifacts_response = requests.get(artifacts_url, headers=headers)
    artifacts_response.raise_for_status()
    for artifact in artifacts_response.json()['artifacts']:
      artifact_url = f'{artifacts_url}/{artifact["id"]}/zip'
      artifact_response = requests.get(artifact_url, headers=headers)
      artifact_response.raise_for_status()
      with open(f'{artifact["name"]}.zip', 'wb') as f:
        f.write(artifact_response.content)
