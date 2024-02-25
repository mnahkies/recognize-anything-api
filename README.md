# recognize-anything-api

Dockerized FastAPI wrapper around the impressive [recognize-anything](https://github.com/xinyu1205/recognize-anything)
image recognition models.

All model weights, etc are baked into the docker image rather than fetched at runtime.

This means it's possible to run this image without granting it internet access, and
hopefully means it will continue to work in 6 months time. You can verify this by
running the image with `--net none` and using `docker exec` trying:

```shell
curl --verbose -F file=@/opt/app/recognize_anything/images/demo/demo1.jpg localhost:8000/
```

Caveat, the image is huge (~20gb, of which ~13gb is weights, ~6gb pip dependencies) as a
result - though it could probably be slimmed down a bit.

## Build

Pre-requisites:

- Docker/equivalent installed and running

Clone this repository with submodules:

```shell
git clone --recurse-submodules
````

Then run:

```
./bin/docker-build.sh`
```

## Usage

Simply run:

```shell
./bin/docker-run.sh
```

Then you can make requests like:

```shell
curl --verbose -F file=@/path/to/image.jpg localhost:8000/
```

You can choose which model is used by setting the `MODEL_NAME` environment variable to one of:

- `ram_plus` (default)
- `ram`
- `tag2text`

See [./server.py](./server.py) for other options.

## License

See [./LICENSE](./LICENSE) and [./recognize_anything/NOTICE.txt](./recognize_anything/NOTICE.txt)

## Contributing

This is a very scrappy project that I created to experiment with https://github.com/xinyu1205/recognize-anything
and there is plenty of scope for improvement!

PR's to improve the configurability, packaging, efficiency, etc are welcome.
