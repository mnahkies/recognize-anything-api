FROM nvidia/cuda:12.3.0-devel-ubuntu22.04 AS dependencies

RUN apt-get update && apt-get install python3 python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget curl git -y
RUN pip install --upgrade setuptools

FROM dependencies AS pip_dependencies

WORKDIR /opt/app
ADD requirements.txt setup.cfg setup.py /opt/app/
RUN --mount=type=cache,target=/root/.cache/pip pip install -e .

FROM dependencies AS models

RUN mkdir -p /data/pretrained/
RUN wget -O /data/pretrained/ram_plus_swin_large_14m.pth https://huggingface.co/xinyu1205/recognize-anything-plus-model/resolve/main/ram_plus_swin_large_14m.pth
RUN wget -O /data/pretrained/ram_swin_large_14m.pth https://huggingface.co/spaces/xinyu1205/Recognize_Anything-Tag2Text/resolve/main/ram_swin_large_14m.pth
RUN wget -O /data/pretrained/tag2text_swin_14m.pth https://huggingface.co/spaces/xinyu1205/Recognize_Anything-Tag2Text/resolve/main/tag2text_swin_14m.pth


FROM pip_dependencies AS runtime

COPY --from=models /data /data
ADD . /opt/app

RUN python3 /opt/app/init.py

ENTRYPOINT ["./server.sh"]
