#!/bin/sh
set -eu

email_username="${1:-cohen2jl}"
image_name="docker-text-analysis:latest"
tar_name="$(printf '%s' "$email_username" | tr '[:lower:]' '[:upper:]').tar"

docker build --tag "$image_name" .
docker run --rm "$image_name"
docker image inspect "$image_name" --format 'Image size: {{.Size}} bytes'
docker save --output "$tar_name" "$image_name"

printf 'Created %s\n' "$tar_name"
