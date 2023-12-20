"""New scheduler: runs codes every 2 hours"""
import schedule
import time
import subprocess
import sys

# Counter to track the number of executions for run_reddit every 2 hours
execution_count_reddit = 0
def run_4chan_board_k():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/4chan_board_k.py"])

def run_4chan_board_po():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/4chan_board_po.py"])

def run_toxicity_four_chan():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/toxicity_four_chan.py"])

def run_reddit():
    global execution_count_reddit

    # Check if the script has already run 12 times (24 hours / 2 hours)
    if execution_count_reddit < 20:
        # Execute the script
        subprocess.run(["python3", "/home/kkamara1/reddit-folder/reddit.py"])
        # Increment the execution count
        execution_count_reddit += 1
    else:
        # Stop further executions once the count reaches 12
        sys.exit()
        
def run_toxicity_reddit():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/toxicity_reddit.py"])

def run_politics():
    subprocess.run(["python3", "/home/kkamara1/reddit-folder/reddit-politics.py"])

# def run_new_politics():
    # subprocess.run({"python3", "/home/kkamara1/reddit-folder/new-reddit-politics.py"})


# Schedule the job to run run_reddit every 2 hours and run_4chan every 30 minutes
schedule.every(2).hours.do(run_reddit)
schedule.every(9).minutes.do(run_toxicity_reddit)
# schedule.every(50).minutes.do(run_new_politics)
schedule.every(45).minutes.do(run_politics)
schedule.every(13).minutes.do(run_4chan_board_k)
schedule.every(17).minutes.do(run_4chan_board_po)
schedule.every(20).minutes.do(run_toxicity_four_chan)


# Initial run to start the loop
run_reddit()
run_toxicity_reddit()
run_politics()
# run_new_politics()
run_4chan_board_k()
run_4chan_board_po()
run_toxicity_four_chan()

# Run the scheduling loop
while True:
    schedule.run_pending()
    time.sleep(60)  # Sleep for a minute to avoid excessive CPU usage

"""First Running scheduler: Runs every mid Night"""
# import schedule
# import time
# import subprocess
# import sys

# # Counter to track the number of executions
# execution_count = 0

# def run_4chan():
#     subprocess.run(["python3", "/home/kkamara1/reddit-folder/4chan.py"]) 

# def run_reddit():
#     global execution_count
    
#     # Check if the script has already run twenty times
#     if execution_count < 20:
#         # Execute the script
#         subprocess.run(["python3", "/home/kkamara1/reddit-folder/reddit.py"])
#         # Increment the execution count
#         execution_count += 1
#         time.sleep(3600)
#     else:
#         # Stop further executions once the count reaches 20
#         sys.exit()

# # Schedule the job to run every day at midnight
# schedule.every().day.at("00:00").do(run_reddit)
# schedule.every().day.at("00:00").do(run_4chan)


# while True:
#     schedule.run_pending()
#     time.sleep(10)
