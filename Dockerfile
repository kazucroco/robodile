FROM python
WORKDIR /robodile
COPY ./requirements.txt ./robodile.py .
RUN pip install -r ./requirements.txt
RUN --mount=type=secret,id=ROBODILE_TOKEN,env=ROBODILE_TOKEN \
    echo $ROBODILE_TOKEN > token.txt
CMD ["python", "robodile.py"]
