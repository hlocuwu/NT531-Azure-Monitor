#!/bin/bash
set -e

echo "Starting Locust scenarios automatically..."

# Chạy từng kịch bản theo thứ tự
echo "!!!RUNNING SCENARIOS 1: STARTUP!!!"
locust -f Scenarios/Scenario_1_Startup.py --headless -u 50 -r 5 -t  1m --host https://youtube.com

echo "!!!RUNNING SCENARIOS 2: RAMPUP!!!"
locust -f Scenarios/Scenario_2_Rampup.py --headless -u 100 -r 10 -t 3m --host https://youtube.com

echo "!!!RUNNING SCENARIOS 3: SPIKE!!!"
locust -f Scenarios/Scenario_3_Spike.py --headless -u 300 -r 100 -t 2m --host https://youtube.com

echo "!!!RUNNING SCENARIOS 4: STEADY!!!"
locust -f Scenarios/Scenario_4_Steady.py --headless -u 150 -r 10 -t 5m --host https://youtube.com

echo "ALL SCENARIOS COMPLETED SUCCESSFULLY!"
