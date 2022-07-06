#!/usr/bin/env bash
#

CTX_FILE=/tmp/datapipe-$(uuidgen)

echo "Running sample pipeline"
python first_step.py --context-file $CTX_FILE
python second_step.py --context-file $CTX_FILE

rm $CTX_FILE
