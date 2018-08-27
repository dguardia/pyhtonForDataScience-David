FROM jupyter/datascience-notebook

RUN python --version

RUN pip install --upgrade pip

RUN conda install --quiet --yes -c \
    'conda-forge' \
    'osmnx' \
    'dask' \
    'spacy' \
    'pymongo' \
    'geopandas'    

RUN python -m spacy download en

RUN pip install -U geopy \
                   rtree \
                   folium \
                   numpy \
                   shapely \
                   fiona \
                   six \
                   pyproj \
                   numexpr==2.6.4 \
                   elasticsearch \
                   geojson \
                   plotly \
                   tqdm \
                   mapboxgl \
                   cufflinks \
                   geohash2 \
                   tables \
                   mixpanel \
                   SQLAlchemy \
                   GeoAlchemy2 \
                   twitter

RUN ["bash", "-c", "source activate root"]

ADD fonts /usr/share/fonts/truetype/
RUN fc-cache
RUN fc-list

VOLUME /notebooks
WORKDIR /notebooks

CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='demo'