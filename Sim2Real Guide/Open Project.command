#!/bin/zsh
project_dir="$(cd -- "$(dirname -- "$0")/.." && pwd -P)"
if [[ -d "/Applications/Visual Studio Code.app" ]]; then
  /usr/bin/open -a "/Applications/Visual Studio Code.app" "$project_dir"
else
  /usr/bin/open -a "Visual Studio Code" "$project_dir"
fi
