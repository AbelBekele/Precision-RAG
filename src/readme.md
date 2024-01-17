<div align="center">
  <!-- <img src="assets/bot_nana_logo.png" alt="logo" height="40%" width="50%"/> -->
  <h1><b>rag test starter</b></h1>

</div>

<!-- TABLE OF CONTENTS -->
<br/>

### Contents

- [Setup](#setup)
- [Installation](#installation)

# Setup

1. Clone this repository:

```sh
git clone git@github.com:abel-blue/prompt-evaluation.git
cd prompt-evaluation
```

2. Setup environment variables on `.env`:

(create .env file in the root directory)

```bash
#################
# Development env
#################

OPENAI_API_KEY=""
VECTORDB_MODEL="gpt-3.5-turbo"
```


# Installation

**Run**

```bash
# create virtual environment
python3 -m venv venv

# activate
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# to generate test data
make data_generate

# to evaluate user input data (prob., accur., confid.)
make data_evaluate
```