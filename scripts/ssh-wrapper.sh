#!/bin/sh

GIT_SSH_KEY="$HOME/.ssh/swgit_sshKey"

if [ -e "$GIT_SSH_KEY" ]; then
    exec ssh -i "$GIT_SSH_KEY" "$@"
else
    exec ssh "$@"
fi
