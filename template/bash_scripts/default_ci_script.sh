#!/usr/bin/env bash
{% import os %}
BUILD_STATUS=0

{{ build_cmd }} && BUILD_STATUS=1

[ $((BUILD_STATUS)) == 0 ] && curl -s -F "GITLAB_PROJECT_ID=$CI_PROJECT_ID" -F "COMMIT_SHA=$CI_COMMIT_SHA" -F "BUILD_STATUS=0" http://192.168.2.200:60000/api/v1/gitlab/jobscripts && exit 101
{% for uuid, pcb in  token_map.items() %}{% set artifact = os.path.join(pcb['project'].path,pcb['project'].artifact_path) %}
curl -s -H "Artifact-Token:{{uuid}}" -H "SHA:`sha256sum {{ artifact }}|awk '{print $1}'`" -T {{ artifact }}  http://192.168.2.200:60000/api/v1/gitlab/receiver | bash
{% end %}
