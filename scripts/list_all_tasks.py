import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
token = 'pk_234154001_WRSQMB8UMM4MO9QKR3N8E5GPOKUKDTEM'
url = 'https://api.clickup.com/api/v2/list/901422611886/task?subtasks=true&include_closed=true'
req = urllib.request.Request(url, headers={'Authorization': token})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

tasks = data.get('tasks', [])
print(f"Total tasks: {len(tasks)}")
for t in tasks:
    status = t.get('status', {}).get('status', 'unknown')
    print(f"{t['id']} | {status:15} | {t['name']}")
