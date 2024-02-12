FROM python:3.9-slim
LABEL maintainer="schrodingersfish@outlook.com"
WORKDIR /app
COPY . /app
RUN pip install frozenlist-1.3.0-py3-none-any.whl\
    && pip install multidict-6.0.2-py3-none-any.whl\
    && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
