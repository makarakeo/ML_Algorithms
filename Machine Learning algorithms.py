{
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "In this notebook we try to practice all the classification algorithms.\n",
                "\n",
                "We load a dataset using Pandas library, and apply the following algorithms, and find the best one for this specific dataset by accuracy evaluation methods.\n",
                "\n",
                "Lets first load required libraries:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [],
            "source": [
                "import itertools\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "from matplotlib.ticker import NullFormatter\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.ticker as ticker\n",
                "from sklearn import preprocessing\n",
                "%matplotlib inline"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### About dataset"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "This dataset is about past loans. The __Loan_train.csv__ data set includes details of 346 customers whose loan are already paid off or defaulted. It includes following fields:\n",
                "\n",
                "| Field          | Description                                                                           |\n",
                "|----------------|---------------------------------------------------------------------------------------|\n",
                "| Loan_status    | Whether a loan is paid off on in collection                                           |\n",
                "| Principal      | Basic principal loan amount at the                                                    |\n",
                "| Terms          | Origination terms which can be weekly (7 days), biweekly, and monthly payoff schedule |\n",
                "| Effective_date | When the loan got originated and took effects                                         |\n",
                "| Due_date       | Since it’s one-time payoff schedule, each loan has one single due date                |\n",
                "| Age            | Age of applicant                                                                      |\n",
                "| Education      | Education of applicant                                                                |\n",
                "| Gender         | The gender of applicant                                                               |"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Lets download the dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "--2019-07-11 00:43:34--  https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_train.csv\n",
                        "Resolving s3-api.us-geo.objectstorage.softlayer.net (s3-api.us-geo.objectstorage.softlayer.net)... 67.228.254.193\n",
                        "Connecting to s3-api.us-geo.objectstorage.softlayer.net (s3-api.us-geo.objectstorage.softlayer.net)|67.228.254.193|:443... connected.\n",
                        "HTTP request sent, awaiting response... 200 OK\n",
                        "Length: 23101 (23K) [text/csv]\n",
                        "Saving to: ‘loan_train.csv’\n",
                        "\n",
                        "100%[======================================>] 23,101      --.-K/s   in 0.002s  \n",
                        "\n",
                        "2019-07-11 00:43:34 (12.8 MB/s) - ‘loan_train.csv’ saved [23101/23101]\n",
                        "\n"
                    ]
                }
            ],
            "source": [
                "!wget -O loan_train.csv https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_train.csv"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### Load Data From CSV File  "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 4,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                },
                "scrolled": true
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Unnamed: 0</th>\n",
                            "      <th>Unnamed: 0.1</th>\n",
                            "      <th>loan_status</th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>effective_date</th>\n",
                            "      <th>due_date</th>\n",
                            "      <th>age</th>\n",
                            "      <th>education</th>\n",
                            "      <th>Gender</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/8/2016</td>\n",
                            "      <td>10/7/2016</td>\n",
                            "      <td>45</td>\n",
                            "      <td>High School or Below</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>2</td>\n",
                            "      <td>2</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/8/2016</td>\n",
                            "      <td>10/7/2016</td>\n",
                            "      <td>33</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>3</td>\n",
                            "      <td>3</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>9/8/2016</td>\n",
                            "      <td>9/22/2016</td>\n",
                            "      <td>27</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>4</td>\n",
                            "      <td>4</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/9/2016</td>\n",
                            "      <td>10/8/2016</td>\n",
                            "      <td>28</td>\n",
                            "      <td>college</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>6</td>\n",
                            "      <td>6</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/9/2016</td>\n",
                            "      <td>10/8/2016</td>\n",
                            "      <td>29</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Unnamed: 0  Unnamed: 0.1 loan_status  Principal  terms effective_date  \\\n",
                            "0           0             0     PAIDOFF       1000     30       9/8/2016   \n",
                            "1           2             2     PAIDOFF       1000     30       9/8/2016   \n",
                            "2           3             3     PAIDOFF       1000     15       9/8/2016   \n",
                            "3           4             4     PAIDOFF       1000     30       9/9/2016   \n",
                            "4           6             6     PAIDOFF       1000     30       9/9/2016   \n",
                            "\n",
                            "    due_date  age             education  Gender  \n",
                            "0  10/7/2016   45  High School or Below    male  \n",
                            "1  10/7/2016   33              Bechalor  female  \n",
                            "2  9/22/2016   27               college    male  \n",
                            "3  10/8/2016   28               college  female  \n",
                            "4  10/8/2016   29               college    male  "
                        ]
                    },
                    "execution_count": 4,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df = pd.read_csv('loan_train.csv')\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 5,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "(346, 10)"
                        ]
                    },
                    "execution_count": 5,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df.shape"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### Convert to date time object "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 6,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Unnamed: 0</th>\n",
                            "      <th>Unnamed: 0.1</th>\n",
                            "      <th>loan_status</th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>effective_date</th>\n",
                            "      <th>due_date</th>\n",
                            "      <th>age</th>\n",
                            "      <th>education</th>\n",
                            "      <th>Gender</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>45</td>\n",
                            "      <td>High School or Below</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>2</td>\n",
                            "      <td>2</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>33</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>3</td>\n",
                            "      <td>3</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-09-22</td>\n",
                            "      <td>27</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>4</td>\n",
                            "      <td>4</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>28</td>\n",
                            "      <td>college</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>6</td>\n",
                            "      <td>6</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>29</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Unnamed: 0  Unnamed: 0.1 loan_status  Principal  terms effective_date  \\\n",
                            "0           0             0     PAIDOFF       1000     30     2016-09-08   \n",
                            "1           2             2     PAIDOFF       1000     30     2016-09-08   \n",
                            "2           3             3     PAIDOFF       1000     15     2016-09-08   \n",
                            "3           4             4     PAIDOFF       1000     30     2016-09-09   \n",
                            "4           6             6     PAIDOFF       1000     30     2016-09-09   \n",
                            "\n",
                            "    due_date  age             education  Gender  \n",
                            "0 2016-10-07   45  High School or Below    male  \n",
                            "1 2016-10-07   33              Bechalor  female  \n",
                            "2 2016-09-22   27               college    male  \n",
                            "3 2016-10-08   28               college  female  \n",
                            "4 2016-10-08   29               college    male  "
                        ]
                    },
                    "execution_count": 6,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df['due_date'] = pd.to_datetime(df['due_date'])\n",
                "df['effective_date'] = pd.to_datetime(df['effective_date'])\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "# Data visualization and pre-processing\n",
                "\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Let’s see how many of each class is in our data set "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "PAIDOFF       260\n",
                            "COLLECTION     86\n",
                            "Name: loan_status, dtype: int64"
                        ]
                    },
                    "execution_count": 7,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df['loan_status'].value_counts()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "260 people have paid off the loan on time while 86 have gone into collection \n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Lets plot some columns to underestand data better:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "Solving environment: done\n",
                        "\n",
                        "## Package Plan ##\n",
                        "\n",
                        "  environment location: /opt/conda/envs/Python36\n",
                        "\n",
                        "  added / updated specs: \n",
                        "    - seaborn\n",
                        "\n",
                        "\n",
                        "The following packages will be downloaded:\n",
                        "\n",
                        "    package                    |            build\n",
                        "    ---------------------------|-----------------\n",
                        "    ca-certificates-2019.5.15  |                0         133 KB  anaconda\n",
                        "    openssl-1.1.1              |       h7b6447c_0         5.0 MB  anaconda\n",
                        "    certifi-2019.6.16          |           py36_0         154 KB  anaconda\n",
                        "    seaborn-0.9.0              |           py36_0         379 KB  anaconda\n",
                        "    ------------------------------------------------------------\n",
                        "                                           Total:         5.7 MB\n",
                        "\n",
                        "The following packages will be UPDATED:\n",
                        "\n",
                        "    ca-certificates: 2019.5.15-0       --> 2019.5.15-0      anaconda\n",
                        "    certifi:         2019.6.16-py36_0  --> 2019.6.16-py36_0 anaconda\n",
                        "    openssl:         1.1.1c-h7b6447c_1 --> 1.1.1-h7b6447c_0 anaconda\n",
                        "    seaborn:         0.9.0-py36_0      --> 0.9.0-py36_0     anaconda\n",
                        "\n",
                        "\n",
                        "Downloading and Extracting Packages\n",
                        "ca-certificates-2019 | 133 KB    | ##################################### | 100% \n",
                        "openssl-1.1.1        | 5.0 MB    | ##################################### | 100% \n",
                        "certifi-2019.6.16    | 154 KB    | ##################################### | 100% \n",
                        "seaborn-0.9.0        | 379 KB    | ##################################### | 100% \n",
                        "Preparing transaction: done\n",
                        "Verifying transaction: done\n",
                        "Executing transaction: done\n"
                    ]
                }
            ],
            "source": [
                "# notice: installing seaborn might takes a few minutes\n",
                "!conda install -c anaconda seaborn -y"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 8,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "image/png": "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IIcccgjnnHMODzzwQMt2ffr0aXkkxwUXXMD8+fP53Oc+11L3nDlzGDFiBMOGDePwww9nzpw5LesuvPBCBg4cyMaNGwFYu3YtNTU1HfqdtJcft2FmZW3lO29z1HWPFK2+Z7+Vb+zsrUUEZ555JhMnTmwZtbyhoYHVq1dz4YUXMnXqVMaNG8f69es566yzuPPOO1tGiuiIL3zhCy2jnDfbsGEDp5xyCt/97nc59dRTAXjiiSeorq5uGX5p9OjRTJkypWW8vvnz57fs/+KLL3LFFVcwb948amtreeONNzjxxBM54IADGDFiBJA8W2r69OlccsklHY65I3wFZWZWZE888QRVVVVcfPHFLWV1dXUsX76cY489lnHjxgGwyy67cPvtt3PTTTcV7dj33XcfRx99dEtyAvjsZz/b8kDEtkyZMoVrr72W2tpaAGpra7nmmmu49dZbW7aZPHkyt912G5s3by5a3Pk4QZmZFdnSpUs/8UgMyP+ojCFDhvDhhx/ywQcfdPg4ud12dXV1fPTRR60eu73a8ziPwYMHc9xxx/HjH/+408dpD3fxmZl1k20fi5GrtfLtydfFV6h8MeYru/baaznttNM45ZRTinr8XL6CMjMrskMPPZRFixblLd92XMXXX3+dPn360Ldv3y49dkf23zbGfI/zOPDAA6mrq+PBBx/s9LHa4gRlZlZkY8aMYePGjdx9990tZc8//zxDhw5lwYIF/PrXvwaSBxtefvnlXHnllUU79he/+EV+85vf8POf/7yl7JFHHuGll15q1/5XXHEF3/72t2lsbASgsbGRG2+8ka9//euf2PYb3/gGU6ZMKUrc+biLz8zK2oCB+7XrzruO1NcWScyePZvJkydz00030bt3b2pqavje977HQw89xFe/+lUuvfRStmzZwvnnn7/VreUzZszY6rbuZ55JngE7YsQIdtghuaY455xzGDFiBA888MBWz5O68847OeaYY5g7dy6TJ09m8uTJVFVVMWLECL7//e+36/XV1dVx8803c+qpp7Jp0yaqqqq45ZZbWp4QnOvQQw9l1KhR7X50fUe163EbXc2PE7Du4MdtVAY/biM7Cn3cRptdfJKmS3pP0tKcslslvSppiaTZknZPy2skfSSpIZ1+2N5AzMzMcrXnM6gZwLbXx/OAwyJiBLAcuCZn3e8joi6dLsbMzKwT2kxQEfEk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",
                        "text/plain": [
                            "<Figure size 432x216 with 2 Axes>"
                        ]
                    },
                    "metadata": {
                        "needs_background": "light"
                    },
                    "output_type": "display_data"
                }
            ],
            "source": [
                "import seaborn as sns\n",
                "\n",
                "bins = np.linspace(df.Principal.min(), df.Principal.max(), 10)\n",
                "g = sns.FacetGrid(df, col=\"Gender\", hue=\"loan_status\", palette=\"Set1\", col_wrap=2)\n",
                "g.map(plt.hist, 'Principal', bins=bins, ec=\"k\")\n",
                "\n",
                "g.axes[-1].legend()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 9,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "image/png": "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ZMCAAaxbtw6AlStXMnjw4Hb9TQrhufgKMKi6mg+XLSt2GGbWQUs//ojDb3g6tfpe/tfxbW4TEZxxxhlMmDChZdbyhoYGPv30Uy688ELuu+8+xo0bx5o1azjzzDO59957W2aKaI/vfOc7LbOcN1u7di0nnXQSd9xxB6eccgoAs2bNoqqqqmX6pdGjR3P77be3zNc3e/bslve//vrrXHXVVcycOZPa2lo++OADTjjhBPbZZx+GDx8O5O4t9eCDD3LppZe2O+ZCOUEVIK17yfguuGY9x6xZs6ioqOCSSy5pKaurq+OBBx5g1KhRjBs3DoAddtiBu+++m9GjR3coQeXzyCOPcOSRR7YkJ4Djjjuu4PfffvvtXH/99dTW1gJQW1vLddddx2233cavf/1rACZNmsSdd97J9773vVRizsddfGZmXWDhwoWb3RID8t8qY99992X16tV88cUX7d5P6267uro6vvrqqy3uu1CF3M5j4MCBHH300S0Jqyv4DMrMrBtteluM1rZUvjX5uvg6K1+M+cquv/56Tj31VE466aRU99/MZ1BmZl3goIMOYt68eXnL586du1HZ+++/T58+fejbt2+X7rs97980xny389hvv/2oq6vj8ccf7/C+tsYJysysC4wZM4Z169bxy1/+sqXs1VdfZciQIcyZM4dnn30WyN3Y8IorruDqq69Obd/f/e53+fOf/8zvf//7lrKnn36aN954o6D3X3XVVfz0pz+lsbERgMbGRm666SauvPLKzbb90Y9+xO23355K3JtyF5+Zlb3qAXsXNPKuPfW1RRLTpk1j0qRJ3HzzzVRWVjJ48GDuuusunnzySS6//HImTpzIhg0bOP/88zcaWj5lypSNhnW/9NJLAAwfPpxttsmdV5xzzjkMHz6cxx57bKP7Sd17770cddRRzJgxg0mTJjFp0iQqKioYPnw4P/vZzwo6vrq6Om655RZOOeUUvv76ayoqKrj11ltb7hDc2kEHHcTIkSMLvnV9exR0u4201NfXx6anjaUgrdtk1HzS5NttlL8O3W6jtVJtJ1ni221kR3fcbsPMzKxbOUGZmVkmOUGZWVlyF3jxdfZv4ARlZmWnsrKSVatWOUkVUUSwatUqKisrO1yHR/GZWdmpqamhqamJFStWFDuUHq2yspKamo4PDHOCKlHb0bFfneczsH9/lixdmkpdZllQ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",
                        "text/plain": [
                            "<Figure size 432x216 with 2 Axes>"
                        ]
                    },
                    "metadata": {
                        "needs_background": "light"
                    },
                    "output_type": "display_data"
                }
            ],
            "source": [
                "bins = np.linspace(df.age.min(), df.age.max(), 10)\n",
                "g = sns.FacetGrid(df, col=\"Gender\", hue=\"loan_status\", palette=\"Set1\", col_wrap=2)\n",
                "g.map(plt.hist, 'age', bins=bins, ec=\"k\")\n",
                "\n",
                "g.axes[-1].legend()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "# Pre-processing:  Feature selection/extraction"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### Lets look at the day of the week people get the loan "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 9,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "image/png": "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",
                        "text/plain": [
                            "<Figure size 432x216 with 2 Axes>"
                        ]
                    },
                    "metadata": {
                        "needs_background": "light"
                    },
                    "output_type": "display_data"
                }
            ],
            "source": [
                "df['dayofweek'] = df['effective_date'].dt.dayofweek\n",
                "bins = np.linspace(df.dayofweek.min(), df.dayofweek.max(), 10)\n",
                "g = sns.FacetGrid(df, col=\"Gender\", hue=\"loan_status\", palette=\"Set1\", col_wrap=2)\n",
                "g.map(plt.hist, 'dayofweek', bins=bins, ec=\"k\")\n",
                "g.axes[-1].legend()\n",
                "plt.show()\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "We see that people who get the loan at the end of the week dont pay it off, so lets use Feature binarization to set a threshold values less then day 4 "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 16,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Unnamed: 0</th>\n",
                            "      <th>Unnamed: 0.1</th>\n",
                            "      <th>loan_status</th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>effective_date</th>\n",
                            "      <th>due_date</th>\n",
                            "      <th>age</th>\n",
                            "      <th>education</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>dayofweek</th>\n",
                            "      <th>weekend</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>45</td>\n",
                            "      <td>High School or Below</td>\n",
                            "      <td>male</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>2</td>\n",
                            "      <td>2</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>33</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>female</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>3</td>\n",
                            "      <td>3</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-09-22</td>\n",
                            "      <td>27</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>4</td>\n",
                            "      <td>4</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>28</td>\n",
                            "      <td>college</td>\n",
                            "      <td>female</td>\n",
                            "      <td>4</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>6</td>\n",
                            "      <td>6</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>29</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "      <td>4</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Unnamed: 0  Unnamed: 0.1 loan_status  Principal  terms effective_date  \\\n",
                            "0           0             0     PAIDOFF       1000     30     2016-09-08   \n",
                            "1           2             2     PAIDOFF       1000     30     2016-09-08   \n",
                            "2           3             3     PAIDOFF       1000     15     2016-09-08   \n",
                            "3           4             4     PAIDOFF       1000     30     2016-09-09   \n",
                            "4           6             6     PAIDOFF       1000     30     2016-09-09   \n",
                            "\n",
                            "    due_date  age             education  Gender  dayofweek  weekend  \n",
                            "0 2016-10-07   45  High School or Below    male          3        0  \n",
                            "1 2016-10-07   33              Bechalor  female          3        0  \n",
                            "2 2016-09-22   27               college    male          3        0  \n",
                            "3 2016-10-08   28               college  female          4        1  \n",
                            "4 2016-10-08   29               college    male          4        1  "
                        ]
                    },
                    "execution_count": 16,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df['weekend'] = df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "## Convert Categorical features to numerical values"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Lets look at gender:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 17,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "Gender  loan_status\n",
                            "female  PAIDOFF        0.865385\n",
                            "        COLLECTION     0.134615\n",
                            "male    PAIDOFF        0.731293\n",
                            "        COLLECTION     0.268707\n",
                            "Name: loan_status, dtype: float64"
                        ]
                    },
                    "execution_count": 17,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "86 % of female pay there loans while only 73 % of males pay there loan\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Lets convert male to 0 and female to 1:\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 18,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Unnamed: 0</th>\n",
                            "      <th>Unnamed: 0.1</th>\n",
                            "      <th>loan_status</th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>effective_date</th>\n",
                            "      <th>due_date</th>\n",
                            "      <th>age</th>\n",
                            "      <th>education</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>dayofweek</th>\n",
                            "      <th>weekend</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>45</td>\n",
                            "      <td>High School or Below</td>\n",
                            "      <td>0</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>2</td>\n",
                            "      <td>2</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-10-07</td>\n",
                            "      <td>33</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>1</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>3</td>\n",
                            "      <td>3</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>2016-09-08</td>\n",
                            "      <td>2016-09-22</td>\n",
                            "      <td>27</td>\n",
                            "      <td>college</td>\n",
                            "      <td>0</td>\n",
                            "      <td>3</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>4</td>\n",
                            "      <td>4</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>28</td>\n",
                            "      <td>college</td>\n",
                            "      <td>1</td>\n",
                            "      <td>4</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>6</td>\n",
                            "      <td>6</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>2016-09-09</td>\n",
                            "      <td>2016-10-08</td>\n",
                            "      <td>29</td>\n",
                            "      <td>college</td>\n",
                            "      <td>0</td>\n",
                            "      <td>4</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Unnamed: 0  Unnamed: 0.1 loan_status  Principal  terms effective_date  \\\n",
                            "0           0             0     PAIDOFF       1000     30     2016-09-08   \n",
                            "1           2             2     PAIDOFF       1000     30     2016-09-08   \n",
                            "2           3             3     PAIDOFF       1000     15     2016-09-08   \n",
                            "3           4             4     PAIDOFF       1000     30     2016-09-09   \n",
                            "4           6             6     PAIDOFF       1000     30     2016-09-09   \n",
                            "\n",
                            "    due_date  age             education  Gender  dayofweek  weekend  \n",
                            "0 2016-10-07   45  High School or Below       0          3        0  \n",
                            "1 2016-10-07   33              Bechalor       1          3        0  \n",
                            "2 2016-09-22   27               college       0          3        0  \n",
                            "3 2016-10-08   28               college       1          4        1  \n",
                            "4 2016-10-08   29               college       0          4        1  "
                        ]
                    },
                    "execution_count": 18,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "## One Hot Encoding  \n",
                "#### How about education?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 19,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "education             loan_status\n",
                            "Bechalor              PAIDOFF        0.750000\n",
                            "                      COLLECTION     0.250000\n",
                            "High School or Below  PAIDOFF        0.741722\n",
                            "                      COLLECTION     0.258278\n",
                            "Master or Above       COLLECTION     0.500000\n",
                            "                      PAIDOFF        0.500000\n",
                            "college               PAIDOFF        0.765101\n",
                            "                      COLLECTION     0.234899\n",
                            "Name: loan_status, dtype: float64"
                        ]
                    },
                    "execution_count": 19,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df.groupby(['education'])['loan_status'].value_counts(normalize=True)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "#### Feature befor One Hot Encoding"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 20,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>age</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>education</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>45</td>\n",
                            "      <td>0</td>\n",
                            "      <td>High School or Below</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>33</td>\n",
                            "      <td>1</td>\n",
                            "      <td>Bechalor</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>27</td>\n",
                            "      <td>0</td>\n",
                            "      <td>college</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>28</td>\n",
                            "      <td>1</td>\n",
                            "      <td>college</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>29</td>\n",
                            "      <td>0</td>\n",
                            "      <td>college</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Principal  terms  age  Gender             education\n",
                            "0       1000     30   45       0  High School or Below\n",
                            "1       1000     30   33       1              Bechalor\n",
                            "2       1000     15   27       0               college\n",
                            "3       1000     30   28       1               college\n",
                            "4       1000     30   29       0               college"
                        ]
                    },
                    "execution_count": 20,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "df[['Principal','terms','age','Gender','education']].head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "#### Use one hot encoding technique to conver categorical varables to binary variables and append them to the feature Data Frame "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 21,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>age</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>weekend</th>\n",
                            "      <th>Bechalor</th>\n",
                            "      <th>High School or Below</th>\n",
                            "      <th>college</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>45</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>33</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>27</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>28</td>\n",
                            "      <td>1</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>29</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Principal  terms  age  Gender  weekend  Bechalor  High School or Below  \\\n",
                            "0       1000     30   45       0        0         0                     1   \n",
                            "1       1000     30   33       1        0         1                     0   \n",
                            "2       1000     15   27       0        0         0                     0   \n",
                            "3       1000     30   28       1        1         0                     0   \n",
                            "4       1000     30   29       0        1         0                     0   \n",
                            "\n",
                            "   college  \n",
                            "0        0  \n",
                            "1        0  \n",
                            "2        1  \n",
                            "3        1  \n",
                            "4        1  "
                        ]
                    },
                    "execution_count": 21,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "Feature = df[['Principal','terms','age','Gender','weekend']]\n",
                "Feature = pd.concat([Feature,pd.get_dummies(df['education'])], axis=1)\n",
                "Feature.drop(['Master or Above'], axis = 1,inplace=True)\n",
                "Feature.head()\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### Feature selection"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Lets defind feature sets, X:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 36,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>age</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>weekend</th>\n",
                            "      <th>Bechalor</th>\n",
                            "      <th>High School or Below</th>\n",
                            "      <th>college</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>45</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>33</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>15</td>\n",
                            "      <td>27</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>28</td>\n",
                            "      <td>1</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>29</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Principal  terms  age  Gender  weekend  Bechalor  High School or Below  \\\n",
                            "0       1000     30   45       0        0         0                     1   \n",
                            "1       1000     30   33       1        0         1                     0   \n",
                            "2       1000     15   27       0        0         0                     0   \n",
                            "3       1000     30   28       1        1         0                     0   \n",
                            "4       1000     30   29       0        1         0                     0   \n",
                            "\n",
                            "   college  \n",
                            "0        0  \n",
                            "1        0  \n",
                            "2        1  \n",
                            "3        1  \n",
                            "4        1  "
                        ]
                    },
                    "execution_count": 36,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "X = Feature\n",
                "X[0:5]"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "What are our lables?"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 45,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "array([1, 1, 1, 1, 1], dtype=uint8)"
                        ]
                    },
                    "execution_count": 45,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "y = pd.get_dummies(df['loan_status'])['PAIDOFF'].values\n",
                "y[0:5]"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "## Normalize Data "
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Data Standardization give data zero mean and unit variance (technically should be done after train test split )"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": null,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [],
            "source": [
                "X= preprocessing.StandardScaler().fit(X).transform(X)\n",
                "X[0:5]"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "# Classification "
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "Now, it is your turn, use the training set to build an accurate model. Then use the test set to report the accuracy of the model\n",
                "You should use the following algorithm:\n",
                "- K Nearest Neighbor(KNN)\n",
                "- Decision Tree\n",
                "- Support Vector Machine\n",
                "- Logistic Regression\n",
                "\n",
                "\n",
                "\n",
                "__ Notice:__ \n",
                "- You can go above and change the pre-processing, feature selection, feature-extraction, and so on, to make a better model.\n",
                "- You should use either scikit-learn, Scipy or Numpy libraries for developing the classification algorithms.\n",
                "- You should include the code of the algorithm in the following cells."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# K Nearest Neighbor(KNN)\n",
                "Notice: You should find the best k to build the model with the best accuracy.  \n",
                "**warning:** You should not use the __loan_test.csv__ for finding the best k, however, you can split your train_loan.csv into train and test to find the best __k__."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 48,
            "metadata": {},
            "outputs": [],
            "source": [
                "from sklearn.neighbors import KNeighborsClassifier\n",
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn import metrics\n",
                "X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 49,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "image/png": "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",
                        "text/plain": [
                            "<Figure size 432x288 with 1 Axes>"
                        ]
                    },
                    "metadata": {
                        "needs_background": "light"
                    },
                    "output_type": "display_data"
                }
            ],
            "source": [
                "mean_acc=np.zeros(50)\n",
                "std_acc = np.zeros(50)\n",
                "for n in range(1,51):\n",
                "    knnmodel=KNeighborsClassifier(n_neighbors=n).fit(X_train,y_train)\n",
                "    y_pred=knnmodel.predict(X_test)\n",
                "    mean_acc[n-1]=metrics.accuracy_score(y_test,y_pred)\n",
                "    std_acc[n-1]=np.std(y_pred==y_test)/np.sqrt(y_pred.shape[0])\n",
                "    \n",
                "plt.plot(range(1,51),mean_acc,'g')\n",
                "plt.fill_between(range(1,51),mean_acc - 1 * std_acc,mean_acc + 1 * std_acc, alpha=0.10)\n",
                "plt.legend(('Accuracy ', '+/- 3xstd'))\n",
                "plt.ylabel('Accuracy ')\n",
                "plt.xlabel('Number of Nabors (K)')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 50,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "The best accuracy was with 0.7857142857142857 with k= 37\n"
                    ]
                }
            ],
            "source": [
                "print( \"The best accuracy was with\", mean_acc.max(), \"with k=\", mean_acc.argmax()+1) "
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Decision Tree"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 51,
            "metadata": {},
            "outputs": [],
            "source": [
                "from sklearn.tree import DecisionTreeClassifier"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 79,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=4,\n",
                            "            max_features=None, max_leaf_nodes=None,\n",
                            "            min_impurity_decrease=0.0, min_impurity_split=None,\n",
                            "            min_samples_leaf=1, min_samples_split=2,\n",
                            "            min_weight_fraction_leaf=0.0, presort=False, random_state=None,\n",
                            "            splitter='best')"
                        ]
                    },
                    "execution_count": 79,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "dtmodel = DecisionTreeClassifier(criterion=\"entropy\", max_depth = 4)\n",
                "dtmodel.fit(X_train,y_train)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 80,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "0.6142857142857143"
                        ]
                    },
                    "execution_count": 80,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "y_pred=dtmodel.predict(X_test)\n",
                "TreeAccuracy=metrics.accuracy_score(y_test,y_pred)\n",
                "TreeAccuracy"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Support Vector Machine"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 68,
            "metadata": {},
            "outputs": [
                {
                    "name": "stderr",
                    "output_type": "stream",
                    "text": [
                        "/opt/conda/envs/Python36/lib/python3.6/site-packages/sklearn/svm/base.py:196: FutureWarning: The default value of gamma will change from 'auto' to 'scale' in version 0.22 to account better for unscaled features. Set gamma explicitly to 'auto' or 'scale' to avoid this warning.\n",
                        "  \"avoid this warning.\", FutureWarning)\n"
                    ]
                },
                {
                    "data": {
                        "text/plain": [
                            "SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,\n",
                            "  decision_function_shape='ovr', degree=3, gamma='auto_deprecated',\n",
                            "  kernel='rbf', max_iter=-1, probability=False, random_state=None,\n",
                            "  shrinking=True, tol=0.001, verbose=False)"
                        ]
                    },
                    "execution_count": 68,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "from sklearn import svm\n",
                "svmmodel=svm.SVC(kernel='rbf')\n",
                "svmmodel.fit(X_train,y_train)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 75,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "array([1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
                            "       0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
                            "       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
                            "       1, 1, 1, 1], dtype=uint8)"
                        ]
                    },
                    "execution_count": 75,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "y_pred=svmmodel.predict(X_test)\n",
                "y_pred"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 76,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "0.7571428571428571"
                        ]
                    },
                    "execution_count": 76,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "metrics.accuracy_score(y_test,y_pred)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Logistic Regression"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 81,
            "metadata": {},
            "outputs": [],
            "source": [
                "from sklearn.linear_model import LogisticRegression\n",
                "from sklearn.metrics import confusion_matrix\n",
                "lrmodel=LogisticRegression(C=0.01,solver='liblinear').fit(X_train,y_train)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 59,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n",
                        " 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]\n",
                        "[[0.32295451 0.67704549]\n",
                        " [0.25028458 0.74971542]\n",
                        " [0.18058968 0.81941032]\n",
                        " [0.31842814 0.68157186]\n",
                        " [0.23877924 0.76122076]\n",
                        " [0.20537939 0.79462061]\n",
                        " [0.27303975 0.72696025]\n",
                        " [0.24257638 0.75742362]\n",
                        " [0.31842814 0.68157186]\n",
                        " [0.29873276 0.70126724]\n",
                        " [0.30139145 0.69860855]\n",
                        " [0.31870506 0.68129494]\n",
                        " [0.29486638 0.70513362]\n",
                        " [0.29712705 0.70287295]\n",
                        " [0.13826387 0.86173613]\n",
                        " [0.16477552 0.83522448]\n",
                        " [0.3961522  0.6038478 ]\n",
                        " [0.18361846 0.81638154]\n",
                        " [0.33624938 0.66375062]\n",
                        " [0.22107799 0.77892201]\n",
                        " [0.28403971 0.71596029]\n",
                        " [0.31011812 0.68988188]\n",
                        " [0.3587312  0.6412688 ]\n",
                        " [0.36668443 0.63331557]\n",
                        " [0.21036655 0.78963345]\n",
                        " [0.34061581 0.65938419]\n",
                        " [0.34961925 0.65038075]\n",
                        " [0.1467569  0.8532431 ]\n",
                        " [0.34519783 0.65480217]\n",
                        " [0.1398959  0.8601041 ]\n",
                        " [0.22240276 0.77759724]\n",
                        " [0.34397153 0.65602847]\n",
                        " [0.28135638 0.71864362]\n",
                        " [0.27709473 0.72290527]\n",
                        " [0.21009772 0.78990228]\n",
                        " [0.19606528 0.80393472]\n",
                        " [0.33624938 0.66375062]\n",
                        " [0.14255195 0.85744805]\n",
                        " [0.31313687 0.68686313]\n",
                        " [0.21412393 0.78587607]\n",
                        " [0.35425731 0.64574269]\n",
                        " [0.22801433 0.77198567]\n",
                        " [0.16927732 0.83072268]\n",
                        " [0.34061581 0.65938419]\n",
                        " [0.18966569 0.81033431]\n",
                        " [0.34010247 0.65989753]\n",
                        " [0.22936843 0.77063157]\n",
                        " [0.31870506 0.68129494]\n",
                        " [0.18986182 0.81013818]\n",
                        " [0.18629367 0.81370633]\n",
                        " [0.24092811 0.75907189]\n",
                        " [0.20179757 0.79820243]\n",
                        " [0.2389319  0.7610681 ]\n",
                        " [0.29333468 0.70666532]\n",
                        " [0.26315166 0.73684834]\n",
                        " [0.10211024 0.89788976]\n",
                        " [0.20766284 0.79233716]\n",
                        " [0.24532558 0.75467442]\n",
                        " [0.22240276 0.77759724]\n",
                        " [0.27278662 0.72721338]\n",
                        " [0.1154932  0.8845068 ]\n",
                        " [0.27683928 0.72316072]\n",
                        " [0.19606528 0.80393472]\n",
                        " [0.40572037 0.59427963]\n",
                        " [0.23510262 0.76489738]\n",
                        " [0.31011812 0.68988188]\n",
                        " [0.27683928 0.72316072]\n",
                        " [0.20154559 0.79845441]\n",
                        " [0.16374879 0.83625121]\n",
                        " [0.23510262 0.76489738]]\n"
                    ]
                }
            ],
            "source": [
                "y_pred=lrmodel.predict(X_test)\n",
                "print(y_pred)\n",
                "print(LR.predict_proba(X_test))"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 82,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "0.6142857142857143"
                        ]
                    },
                    "execution_count": 82,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "metrics.accuracy_score(y_test,y_pred)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Model Evaluation using Test set"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 136,
            "metadata": {},
            "outputs": [],
            "source": [
                "from sklearn.metrics import jaccard_similarity_score\n",
                "from sklearn.metrics import f1_score\n",
                "from sklearn.metrics import log_loss"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "First, download and load the test set:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 62,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "--2019-07-11 02:32:38--  https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_test.csv\n",
                        "Resolving s3-api.us-geo.objectstorage.softlayer.net (s3-api.us-geo.objectstorage.softlayer.net)... 67.228.254.193\n",
                        "Connecting to s3-api.us-geo.objectstorage.softlayer.net (s3-api.us-geo.objectstorage.softlayer.net)|67.228.254.193|:443... connected.\n",
                        "HTTP request sent, awaiting response... 200 OK\n",
                        "Length: 3642 (3.6K) [text/csv]\n",
                        "Saving to: ‘loan_test.csv’\n",
                        "\n",
                        "100%[======================================>] 3,642       --.-K/s   in 0s      \n",
                        "\n",
                        "2019-07-11 02:32:38 (638 MB/s) - ‘loan_test.csv’ saved [3642/3642]\n",
                        "\n"
                    ]
                }
            ],
            "source": [
                "!wget -O loan_test.csv https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_test.csv"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "source": [
                "### Load Test set for evaluation "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 120,
            "metadata": {
                "button": false,
                "new_sheet": false,
                "run_control": {
                    "read_only": false
                }
            },
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Unnamed: 0</th>\n",
                            "      <th>Unnamed: 0.1</th>\n",
                            "      <th>loan_status</th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>effective_date</th>\n",
                            "      <th>due_date</th>\n",
                            "      <th>age</th>\n",
                            "      <th>education</th>\n",
                            "      <th>Gender</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>1</td>\n",
                            "      <td>1</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/8/2016</td>\n",
                            "      <td>10/7/2016</td>\n",
                            "      <td>50</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>5</td>\n",
                            "      <td>5</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>300</td>\n",
                            "      <td>7</td>\n",
                            "      <td>9/9/2016</td>\n",
                            "      <td>9/15/2016</td>\n",
                            "      <td>35</td>\n",
                            "      <td>Master or Above</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>21</td>\n",
                            "      <td>21</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/10/2016</td>\n",
                            "      <td>10/9/2016</td>\n",
                            "      <td>43</td>\n",
                            "      <td>High School or Below</td>\n",
                            "      <td>female</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>24</td>\n",
                            "      <td>24</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>9/10/2016</td>\n",
                            "      <td>10/9/2016</td>\n",
                            "      <td>26</td>\n",
                            "      <td>college</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>35</td>\n",
                            "      <td>35</td>\n",
                            "      <td>PAIDOFF</td>\n",
                            "      <td>800</td>\n",
                            "      <td>15</td>\n",
                            "      <td>9/11/2016</td>\n",
                            "      <td>9/25/2016</td>\n",
                            "      <td>29</td>\n",
                            "      <td>Bechalor</td>\n",
                            "      <td>male</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Unnamed: 0  Unnamed: 0.1 loan_status  Principal  terms effective_date  \\\n",
                            "0           1             1     PAIDOFF       1000     30       9/8/2016   \n",
                            "1           5             5     PAIDOFF        300      7       9/9/2016   \n",
                            "2          21            21     PAIDOFF       1000     30      9/10/2016   \n",
                            "3          24            24     PAIDOFF       1000     30      9/10/2016   \n",
                            "4          35            35     PAIDOFF        800     15      9/11/2016   \n",
                            "\n",
                            "    due_date  age             education  Gender  \n",
                            "0  10/7/2016   50              Bechalor  female  \n",
                            "1  9/15/2016   35       Master or Above    male  \n",
                            "2  10/9/2016   43  High School or Below  female  \n",
                            "3  10/9/2016   26               college    male  \n",
                            "4  9/25/2016   29              Bechalor    male  "
                        ]
                    },
                    "execution_count": 120,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "test_df = pd.read_csv('loan_test.csv')\n",
                "test_df.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 131,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/html": [
                            "<div>\n",
                            "<style scoped>\n",
                            "    .dataframe tbody tr th:only-of-type {\n",
                            "        vertical-align: middle;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe tbody tr th {\n",
                            "        vertical-align: top;\n",
                            "    }\n",
                            "\n",
                            "    .dataframe thead th {\n",
                            "        text-align: right;\n",
                            "    }\n",
                            "</style>\n",
                            "<table border=\"1\" class=\"dataframe\">\n",
                            "  <thead>\n",
                            "    <tr style=\"text-align: right;\">\n",
                            "      <th></th>\n",
                            "      <th>Principal</th>\n",
                            "      <th>terms</th>\n",
                            "      <th>age</th>\n",
                            "      <th>Gender</th>\n",
                            "      <th>weekend</th>\n",
                            "      <th>Bechalor</th>\n",
                            "      <th>High School or Below</th>\n",
                            "      <th>college</th>\n",
                            "    </tr>\n",
                            "  </thead>\n",
                            "  <tbody>\n",
                            "    <tr>\n",
                            "      <th>0</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>50</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>1</th>\n",
                            "      <td>300</td>\n",
                            "      <td>7</td>\n",
                            "      <td>35</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>2</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>43</td>\n",
                            "      <td>1</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>3</th>\n",
                            "      <td>1000</td>\n",
                            "      <td>30</td>\n",
                            "      <td>26</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "    </tr>\n",
                            "    <tr>\n",
                            "      <th>4</th>\n",
                            "      <td>800</td>\n",
                            "      <td>15</td>\n",
                            "      <td>29</td>\n",
                            "      <td>0</td>\n",
                            "      <td>1</td>\n",
                            "      <td>1</td>\n",
                            "      <td>0</td>\n",
                            "      <td>0</td>\n",
                            "    </tr>\n",
                            "  </tbody>\n",
                            "</table>\n",
                            "</div>"
                        ],
                        "text/plain": [
                            "   Principal  terms  age  Gender  weekend  Bechalor  High School or Below  \\\n",
                            "0       1000     30   50       1        0         1                     0   \n",
                            "1        300      7   35       0        1         0                     0   \n",
                            "2       1000     30   43       1        1         0                     1   \n",
                            "3       1000     30   26       0        1         0                     0   \n",
                            "4        800     15   29       0        1         1                     0   \n",
                            "\n",
                            "   college  \n",
                            "0        0  \n",
                            "1        0  \n",
                            "2        0  \n",
                            "3        1  \n",
                            "4        0  "
                        ]
                    },
                    "execution_count": 131,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "test_df['effective_date']=pd.to_datetime(test_df['effective_date'])\n",
                "test_df['dayofweek'] = test_df['effective_date'].dt.dayofweek\n",
                "test_df['weekend'] = test_df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)\n",
                "Feature_test = test_df[['Principal','terms','age','Gender','weekend']]\n",
                "Feature_test = pd.concat([Feature_test,pd.get_dummies(test_df['education'])], axis=1)\n",
                "Feature_test.drop(['Master or Above'], axis = 1,inplace=True)\n",
                "Feature_test.head()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 143,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\n",
                            "       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,\n",
                            "       0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=uint8)"
                        ]
                    },
                    "execution_count": 143,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "X_testset=Feature_test\n",
                "y_testset=pd.get_dummies(test_df['loan_status'])['PAIDOFF'].values\n",
                "y_testset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 145,
            "metadata": {},
            "outputs": [],
            "source": [
                "y_pred_knn=knnmodel.predict(X_testset)\n",
                "y_pred_dt=dtmodel.predict(X_testset)\n",
                "y_pred_svm=svmmodel.predict(X_testset)\n",
                "y_pred_lr=lrmodel.predict(X_testset)\n",
                "y_pred_lr_proba=lrmodel.predict_proba(X_testset)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 151,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "0.851063829787234\n",
                        "0.8157894736842106\n",
                        "0.8602150537634409\n",
                        "0.851063829787234\n"
                    ]
                }
            ],
            "source": [
                "print(f1_score(y_testset,y_pred_knn))\n",
                "print(f1_score(y_testset,y_pred_dt))\n",
                "print(f1_score(y_testset,y_pred_svm))\n",
                "print(f1_score(y_testset,y_pred_lr))"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 152,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [
                        "0.7407407407407407\n",
                        "0.7407407407407407\n",
                        "0.7592592592592593\n",
                        "0.7407407407407407\n"
                    ]
                }
            ],
            "source": [
                "print(jaccard_similarity_score(y_testset,y_pred_knn))\n",
                "print(jaccard_similarity_score(y_testset,y_pred_dt))\n",
                "print(jaccard_similarity_score(y_testset,y_pred_svm))\n",
                "print(jaccard_similarity_score(y_testset,y_pred_lr))"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 154,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "text/plain": [
                            "0.5446922340322017"
                        ]
                    },
                    "execution_count": 154,
                    "metadata": {},
                    "output_type": "execute_result"
                }
            ],
            "source": [
                "LR_log_loss=log_loss(y_testset,y_pred_lr_proba)\n",
                "LR_log_loss"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Report\n",
                "You should be able to report the accuracy of the built model using different evaluation metrics:"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "| Algorithm          | Jaccard | F1-score | LogLoss |\n",
                "|--------------------|---------|----------|---------|\n",
                "| KNN                | 0.741   | 0.851    | NA      |\n",
                "| Decision Tree      | 0.741   | 0.816    | NA      |\n",
                "| SVM                | 0.759   | 0.860    | NA      |\n",
                "| LogisticRegression | 0.741   | 0.851    | 0.545   |"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3.6",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.6.8"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}
