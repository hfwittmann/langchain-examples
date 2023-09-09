Assumptions:
- python is 3.10

# 1

To install go
```
pip install torch
poetry install
```

Remark: ``pip install torch`` installs cuda dependencies poetry (currently) doesnt do that.

# .env file

The folder must contain an env file with the following structure (REPLACE with your key from openai):

```
OPENAI_API_KEY=sk-<SECRET>
```


To run Kedro from the command line you can alternatively first do
```
export OPENAI_API_KEY=sk-<SECRET>
```

and then
```
kedro run
```