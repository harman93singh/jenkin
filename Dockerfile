FROM  hsingh1993/jobs:scrap
#CMD jupyter notebook --ip 0.0.0.0 --port 80 --no-browser --allow-root &
EXPOSE 8080/tcp 
RUN id
USER  jovyan
WORKDIR /home/jovyan/trustdjobs
#RUN su jovyan
#CMD ["jupyter", "notebook", "--port=8000", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
#RUN jupyter notebook --ip 0.0.0.0 --port 80 --no-browser --allow-root &
#CMD ["jupyter", "notebook", "--ip","0.0.0.0","--port=8000","--allow-root","--no-browser"]
CMD ["python","manage.py","runserver","0.0.0.0:8080"]
#CMD python manage.py runserver 0.0.0.0:8000
