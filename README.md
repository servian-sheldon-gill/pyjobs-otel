# Job tracing using Python & OpenTelemetry

This repository demonstrates running multiple steps/jobs as independent processes.

Here, the processes run on the same machine and utilise the local filesystem to pass the traceparent context.

## Quickstart

```sh
source bin/configure
./sample_pipeline.sh
```
