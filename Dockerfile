FROM public.ecr.aws/lambda/python:3.8

COPY lambda/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY lambda/app.py ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]
