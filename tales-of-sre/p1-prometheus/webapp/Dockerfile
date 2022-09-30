FROM python
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 9092
ENTRYPOINT ["python"]
CMD ["metrics.py"]