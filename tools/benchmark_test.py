import os
import subprocess
import requests
import csv
import json
import argparse
import platform
from git import Repo
import signal
import sys

shell_folder = os.path.dirname(os.path.abspath(__file__))

def get_commit_sha_between(repo_path,start_sha,end_sha):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(f"{start_sha}^...{end_sha}",reverse=True))
    return [commit.hexsha[:8] for commit in commits]

def load_json(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)
    return data

def extract_value_from_log(log_file_path, keyword):
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            if keyword in line:
                return line.split(keyword)[-1].strip().split()[0]
    return ""

def test_commit(commit_hash,perf_test_command,get_value_keyword,system,token):
    url = f"https://artifactory/local/build/result_{commit_hash}_{system}.tar.gz"
    tar_path = f"result_{commit_hash}_{system}.tar.gz"
    try:
        response = requests.get(url, auth=(token["user"],token["password"]), proxies={"http": None, "https": None})
        response.raise_for_status()
        with open(tar_path, "wb") as f:
            f.write(response.content)

        subprocess.run(["tar", "xf", tar_path])
        os.rename("result", f"result_{commit_hash}")
        test_dir = os.path.join(f"result_{commit_hash}", "install_pkg", "tests")
        os.chdir(test_dir)
        print(os.getcwd())

        if platform.system().lower() == 'windows':
            perf_test_command = f"call ..\setupvars.bat && {perf_test_command}"
        else:
            perf_test_command = f"source ../setupvars.sh && {perf_test_command}"
        
        print(perf_test_command,flush=True)
        process = subprocess.Popen(perf_test_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, executable="/bin/bash", text='ignore')
        log_all = str(process.communicate(timeout=100)[0])

        print(log_all,flush=True)
        log_file_path = os.path.join(shell_folder, "log", f"commit_{commit_hash}.log")
        with open(log_file_path, "w") as log_file:
            log_file.write(perf_test_command + "\n")
            log_file.write(log_all)

        value = extract_value_from_log(log_file_path, get_value_keyword)

        os.chdir(shell_folder)
        os.remove(tar_path)
        subprocess.run(["rm", "-rf", f"result_{commit_hash}"])
        if 'LD_LIBRARY_PATH' in os.environ:
            del os.environ["LD_LIBRARY_PATH"]
        if 'TBB_DIR' in os.environ:
            del os.environ["TBB_DIR"]
        return value
    except requests.RequestException:
        print(f"Failed to download: {url}")
        return None

def benchmark_test(commits):
    json_path=os.path.join(shell_folder,"benchmark.json")
    json_data = load_json(json_path)
    perf_test_command = json_data["perf_test_command"]
    get_value_keyword = json_data["get_value_keyword"]
    system = json_data["system"]
    factor = float(json_data["factor"])
    token = json_data["token"]

    log_dir = os.path.join(shell_folder, "log")
    os.makedirs(log_dir, exist_ok=True)

    result_csv_path = os.path.join(shell_folder, "result.csv")

    if not commits or len(commits) < 2:
        return None
    with open(result_csv_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["linId", "hash", "value"])

        left = 0
        right = len(commits) - 1
        left_tag=True
        right_tag=True
        previous_value = None
        current_value = None


        # 获取 base commit 的性能值
        while left_tag and left < len(commits):
            try:
                previous_value = float(test_commit(commits[left], perf_test_command, get_value_keyword, system, token))
                left_tag = False
                writer.writerow([left,commits[left], previous_value])
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("get left current value Error")
                left += 1


        # 获取最后一个 commit 的性能值
        while right_tag and right >= 0:
            try:
                current_value = float(test_commit(commits[right], perf_test_command, get_value_keyword, system, token))
                writer.writerow([right,commits[left], current_value])
                right_tag = False
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("get right current value Error")
                right -= 1

        # 如果性能下降超过阈值，进入二分查找
        if previous_value is not None and current_value is not None and current_value < previous_value * factor:
            while left < right:
                mid = (left + right) // 2
                try:
                    mid_value = float(test_commit(commits[mid], perf_test_command, get_value_keyword, system, token))
                    writer.writerow([mid,commits[mid], mid_value])
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print(f"Error testing commit at index {mid}, skipping...")
                    #left = mid + 1
                    if mid + 1 < right:
                        mid += 1
                    elif mid -1 > left:
                        mid -=1
                    else:
                        print("No valid commit to test nearby.")
                        break
                    continue

                if mid_value < previous_value  * factor:
                    right = mid
                else:
                    previous_value = mid_value
                    left = mid + 1

            print(f"Performance dropped more than 5% at commit {commits[left]}.")
            return commits[left]
        else:
            print("No significant performance drop detected.")
            return None

def main():
    parser = argparse.ArgumentParser("find repo regression tools", add_help=True)
    parser.add_argument("-p", "--path", type=str, required=True, help="input repo path")
    parser.add_argument("-s", "--start_sha", type=str, required=True, help="input start commit sha")
    parser.add_argument("-e", "--end_sha", type=str, required=True, help="input end commit sha")
    args = parser.parse_args()
    
    commits = get_commit_sha_between(args.path,args.start_sha,args.end_sha)
    #print(commits)
    benchmark_test(commits)

if __name__ == "__main__":
    main()
