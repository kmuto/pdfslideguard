# docker login; docker buildx  build --platform linux/arm64,linux/amd64 -t kenshimuto/pdfslideguard . --push

FROM debian:trixie-slim
ENV LANG=en_US.UTF-8

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-fitz python3-pymupdf python3-reportlab python3-pypdf fonts-ipaexfont-gothic \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
COPY ./pdfslideguard /usr/bin/pdfslideguard
RUN chmod a+x /usr/bin/pdfslideguard
CMD ["/usr/bin/pdfslideguard"]
