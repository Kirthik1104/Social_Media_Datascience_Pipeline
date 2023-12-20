# Reddit and 4chan Data Collection and Storage

## Overview

This repository contains Python scripts designed to collect data from Reddit and 4chan, storing it in a PostgreSQL database and enabling export to CSV files for further analysis.

## Scripts

### Reddit Data Collection

#### Description

The `reddit.py` script collects data from Reddit, focusing on posts and comments within the "guns" and "firearms" subreddits. It stores the acquired data in a PostgreSQL database and allows for exporting to a CSV file.

#### Usage

To initiate Reddit data collection: `python3 reddit.py`

### 4chan Data Collection

#### Description

The `4chan.py` script collects posts from specified boards and threads on 4chan, storing the data in a PostgreSQL database and providing an option for exporting to CSV for analysis.

####Usage

To initiate 4chan data collection: `python3 4chan.py`

### Scheduler Configuration

The scheduling of data collection is handled by the scheduler.py script. It utilizes nohup along with Python's schedule library to automate data retrieval. This orchestrates the execution of reddit.py for Reddit data and 4chan.py for 4chan data.

#### To schedule data retrieval: `nohup python3 scheduler.py &`

```bash
python3 reddit.py
