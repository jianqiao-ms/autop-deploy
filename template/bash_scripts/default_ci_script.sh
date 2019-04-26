#!/usr/bin/env bash
BUILD_STATUS=0
{{ build_cmd }} && BUILD_STATUS=1
[ $((BUILD_STATUS)) == 0 ] && curl -s -F "GITLAB_PROJECT_ID=$CI_PROJECT_ID" -F "COMMIT_SHA=$CI_COMMIT_SHA" -F "BUILD_STATUS=0" http://192.168.2.200:60000/api/v1/gitlab/jobscripts && exit 101
{% for t, a in  token_map.items() %}
curl -s -H "Artifact-Token:{{t}}" -H "SHA:`sha256sum {{a['project']['artifact']}}|awk '{print $1}'`" -T {{a['project']['artifact']}}  http://192.168.2.200:60000/api/v1/gitlab/receiver | bash
{% end %}
