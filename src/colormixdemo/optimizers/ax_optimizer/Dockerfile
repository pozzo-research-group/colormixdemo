FROM ubuntu

RUN apt-get update

RUN apt-get install wget -y
RUN apt-get install build-essential -y

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# install miniconda
RUN bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN conda init bash


# 
RUN mkdir /usr/local/ax_serve
COPY ax_setup.py /user/local/ax_serve
COPY serve_ax.py /usr/local/ax_serve
COPY environment.yml /usr/local/ax_serve

WORKDIR /usr/local/ax_serve 

RUN conda env create --file environment.yml

#CMD ["conda", "run", "-n" "colormix", "flask", "--app", "serve_ax", "run", "--debug"]

EXPOSE 5000