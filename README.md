# Docker Text Analysis

This project completes the Project 3 Docker requirements.

The container reads both text files from `/home/data`. It splits contractions at each apostrophe.
It writes the report to `/home/data/output/result.txt`. It also prints the report before it exits.

## Files

- `Dockerfile` builds a small Python Alpine image.
- `scripts.py` counts words and gets the container IP address.
- `data/` contains the two course files.
- `tests/` contains the unit tests.
- `kubernetes-job.yaml` runs two pods for the extra credit.
- `build-and-export.sh` builds, tests, and exports the image.

## Test the Python script

Run this command:

```sh
python3 -m unittest discover -s tests -v
```

Run the script without Docker:

```sh
DATA_DIR="$PWD/data" python3 scripts.py
```

## Build and run the image

Start Docker Desktop. Then run these commands:

```sh
docker build -t docker-text-analysis:latest .
docker run --name docker-text-analysis docker-text-analysis:latest
docker cp docker-text-analysis:/home/data/output/result.txt ./result.txt
docker rm docker-text-analysis
```

Use this command when you want the output file on the host:

```sh
mkdir -p data/output
docker run --rm -v "$PWD/data/output:/home/data/output" docker-text-analysis:latest
```

The bind mount can fail if it replaces the container directory with a host directory that is not writable.
Use the first commands if Docker Desktop blocks host write access.

## Create the required tar file

Pass your email username to the script. Do not include the `@` sign or the domain.

```sh
chmod +x build-and-export.sh
./build-and-export.sh cohen2jl
```

The script creates `COHEN2JL.tar`.

Load and run the submitted image with these commands:

```sh
docker load --input COHEN2JL.tar
docker run --rm docker-text-analysis:latest
```

## Take the Docker Desktop screenshot

Run the container without `--rm`. Open Docker Desktop while the container runs.

The script exits quickly. Use this command to keep the container visible for 60 seconds:

```sh
docker run --name docker-text-analysis --entrypoint sh docker-text-analysis:latest -c \
  'python3 /home/scripts.py; sleep 60'
```

Take the screenshot. Then remove the stopped container:

```sh
docker rm -f docker-text-analysis
```

## Run the extra-credit job

The included `kube_output.txt` shows the completed two-pod test. The test uses Minikube with the Docker driver.

Build the image. Then run these commands:

```sh
minikube start -p project3-docker --driver=docker
minikube image load docker-text-analysis:latest -p project3-docker
kubectl apply -f kubernetes-job.yaml
kubectl wait --for=condition=complete job/docker-text-analysis --timeout=120s
kubectl get pods
kubectl get pods > kube_output.txt
cat kube_output.txt
kubectl logs -l app=docker-text-analysis --prefix=true
```

The job starts two pods. Each pod creates its report and exits.

Delete the old job before you run it again:

```sh
kubectl delete -f kubernetes-job.yaml
```
