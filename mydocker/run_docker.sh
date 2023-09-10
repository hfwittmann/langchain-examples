docker build -t my-python-bash-image .
docker run -v ./:/workdir -v /home/hfwittmann/Sync/DataScience/mylangchain/langchain-examples/gpt4all-files/:/gpt4all-files -it my-python-bash-image