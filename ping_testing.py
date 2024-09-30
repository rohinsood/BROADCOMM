import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import time

# Define the three IP addresses
ip_addresses = ["192.168.1.1", "8.8.8.8", "1.1.1.1"]
request_count = 1000
csv_file = 'ping_results.csv'

# Function to ping an IP address and return the latency
def ping(ip):
    try:
        output = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True, timeout=2)
        if "time=" in output.stdout:
            latency = output.stdout.split("time=")[1].split(" ms")[0]
            return float(latency)
        else:
            return None
    except subprocess.TimeoutExpired:
        return None

# Prepare a DataFrame to store ping results
df = pd.DataFrame(columns=['Request Number', f'{ip_addresses[0]} Latency (ms)', f'{ip_addresses[1]} Latency (ms)', f'{ip_addresses[2]} Latency (ms)'])

# Ping IP addresses 1000 times
for i in range(1, request_count + 1):
    row = [i]
    for ip in ip_addresses:
        latency = ping(ip)
        row.append(latency if latency is not None else None)  # Use None for timeouts
    df.loc[i - 1] = row
    print(f"Request {i} completed.")
    time.sleep(0.1)  # Optional: Delay between pings

# Save DataFrame to CSV
df.to_csv(csv_file, index=False)
print(f"Results saved to {csv_file}")

# Plot the results
plt.figure(figsize=(10, 6))

# Plot latencies for each IP address
for ip in ip_addresses:
    plt.plot(df['Request Number'], df[f'{ip} Latency (ms)'], label=f'{ip}')

plt.title('Ping Latency Over Time')
plt.xlabel('Request Number')
plt.ylabel('Latency (ms)')
plt.legend()
plt.grid(True)
plt.show()
