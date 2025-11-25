#!/bin/bash
PORT=${PORT:-3000}
dagster-daemon run &
exec dagster-webserver -h 0.0.0.0 -p $PORT -w /opt/dagster/dagster_home/workspace.yaml
