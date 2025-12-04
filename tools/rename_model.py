import os
import pandas as pd
import argparse
import csv
from pathlib import Path


def rename_csv(base):
    # Define the folder containing CSV files
    folder_path = base  # Current directory
    # Process each CSV file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.startswith("llm_summary"):
            os.remove(file_path)
        if filename.endswith('.csv'):
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Check if 'model' column exists
                if 'model' in df.columns:
                    # Extract model name from filename (before '_pytorch')
                    model_name = filename.split('_pytorch')[0]

                    # Update rows 2 to 15 (index 1 to 14) in 'model' column
                    for i in range(0,14):
                        if i > len(df):
                            break
                        if pd.isna(df.at[i,"iteration"]):
                            break
                        df.loc[i, 'model'] = model_name

                    # Save the updated CSV file
                    df.to_csv(file_path, index=False)
                    print(f"Updated file: {filename}")
                else:
                    print(f"Skipped file (no 'model' column): {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

def findAllFile(base):
    perf_long_files = []
    perf_short_files = []
    for root, dr, fs in os.walk(base):
        for f in fs:
            if f.endswith('_l.csv'):
                fullname = os.path.join(root, f)
                perf_long_files.append(fullname)
            elif f.endswith('_s.csv'):
                fullname = os.path.join(root, f)
                perf_short_files.append(fullname)
            elif f.endswith('.csv'):
                fullname = os.path.join(root, f)
                perf_short_files.append(fullname)
    return perf_short_files, perf_long_files


def output_comments(writer, header):
    result = {}
    for key in header:
        result[key] = ""
    writer.writerow(result)

    comment_list = []
    comment_list.append("text_gen or code_gen:")
    comment_list.append('    input_size: Input token size')
    comment_list.append('    output_size: Text/Code generation models: generated text token size')
    comment_list.append("    infer_count: Limit the Text/Code generation models' output token size")
    comment_list.append('    latency: Text/Code generation models: ms/token. Output token size / generation time')
    comment_list.append('    1st_latency: Text/Code generation models: Fisrt token latency')
    comment_list.append('    2nd_avg_latency: Text/Code generation models: Other tokens (exclude first token) latency')
    comment_list.append('    1st_infer_latency: Text/Code generation models: Fisrt inference latency')
    comment_list.append('    2nd_infer_avg_latency: Text/Code generation models: Other inferences (exclude first inference) latency')
    comment_list.append('    result_md5: MD5 of generated text')
    comment_list.append('    prompt_idx: Index of prompts')
    comment_list.append("image_gen:")
    comment_list.append("    infer_count: Tex2Image models' Inference(or Sampling) step size")
    comment_list.append('    1st_latency: First step lantency of unet')
    comment_list.append('    2nd_avg_latency: Other steps latency of unet(exclude first step)')
    comment_list.append('    1st_infer_latency: Same as 1st_latency')
    comment_list.append('    2nd_infer_avg_latency: Same as 2nd_avg_latency')
    comment_list.append('    prompt_idx: Index of prompts')
    comment_list.append("ldm_super_resolution:")
    comment_list.append("    infer_count: Tex2Image models' Inference(or Sampling) step size")
    comment_list.append('    1st_latency: First step lantency of unet')
    comment_list.append('    2nd_avg_latency: Other steps lantency of unet(exclude first step)')
    comment_list.append('    1st_infer_latency: Same as 1st_latency')
    comment_list.append('    2nd_infer_avg_latency: Same as 2nd_avg_latency')
    comment_list.append('    prompt_idx: Image Index')
    comment_list.append('tokenization_time: Tokenizer encode time')
    comment_list.append('detokenization_time: Tokenizer decode time')
    comment_list.append('pretrain_time: Total time of load model and compile model')
    comment_list.append('generation_time: Time for one interaction. (e.g. The duration of  answering one question or generating one picture)')
    comment_list.append('iteration=0: warm-up; iteration=avg: average (exclude warm-up)')
    comment_list.append(
        'max_rss_mem: max rss memory consumption;'
    )
    comment_list.append(
        'max_shared_mem: max shared memory consumption;'
    )

    for comments in comment_list:
        result['iteration'] = comments
        writer.writerow(result)


def read_avg_data(file):
    output_data = []
    with open(file, 'r') as csvfile:
        pretrain_time = ""
        reader = csv.DictReader(csvfile)
        first_row = 0
        for row in reader:
            if row.get('iteration') is not None and str(row['iteration']) == 'avg':
                if (str(row['iteration']) == '0') and first_row == 0:
                    pretrain_time = row['pretrain_time(s)']
                    first_row = first_row + 1
                elif str(row['iteration']) == 'avg':
                    row['pretrain_time(s)'] = pretrain_time
                    output_data.append(row)
    return output_data


def read_median_data(file):
    output_data = []
    with open(file, 'r') as csvfile:
        pretrain_time = ""
        reader = csv.DictReader(csvfile)
        first_row = 0
        for row in reader:
            if row.get('iteration') is not None and str(row['iteration']) == 'median':
                if (str(row['iteration']) == '0') and first_row == 0:
                    pretrain_time = row['pretrain_time(s)']
                    first_row = first_row + 1
                elif str(row['iteration']) == 'median':
                    row['pretrain_time(s)'] = pretrain_time
                    output_data.append(row)
    return output_data


def read_warm_up_data(file):
    output_data = []
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('iteration') is not None and row['iteration'] == "0":
                output_data.append(row)
    return output_data


def make_result_csv(in_file, writer, output_warmup_data, data_type):
    if output_warmup_data:
        perf_data = read_warm_up_data(in_file)
    else:
        if data_type == 'avg':
            perf_data = read_avg_data(in_file)
        elif data_type == 'median':
            perf_data = read_median_data(in_file)
        else:
            perf_data = []
    for data in perf_data:
        writer.writerow(data)
    if len(perf_data) > 0:
        return True
    return False


def output_perf_data_to_csv(perf_file_list, out_file, commitId, data_type='avg', output_warmup_data=False):
    header = write_header(perf_file_list, out_file, commitId, False)
    if len(header) > 0:
        out_file = Path(out_file)
        with out_file.open('a+',newline='') as f:
            writer = csv.DictWriter(f, header)
            idx = 0
            for perf_file in perf_file_list:
                isSucceed = make_result_csv(perf_file, writer, output_warmup_data, data_type)
                if output_warmup_data:
                    print(f"csv:{perf_file} output warmup data succeed:{isSucceed}")
                else:
                    if data_type == 'avg':
                        print(f"csv:{perf_file} output avg data succeed:{isSucceed}")
                    elif data_type == 'median':
                        print(f"csv:{perf_file} output median data succeed:{isSucceed}")
                idx += 1
            output_comments(writer, header)


def output_all_data_to_file(perf_file_list, out_file, commitId):
    header = write_header(perf_file_list, out_file, commitId)
    if len(header) > 0:
        out_file = Path(out_file)
        with out_file.open('a+',newline='') as f:
            writer = csv.DictWriter(f, header)
            for perf_file in perf_file_list:
                with open(perf_file, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    isSucceed = False
                    for row in reader:
                        if row.get('iteration') is not None:
                            if row['iteration'] == "":
                                isSucceed = True
                                break
                            writer.writerow(row)
                    print(f"csv:{perf_file} output to all_data_file succeed:{isSucceed}")


def output_min_each_column_to_file(perf_file_list, out_file, commitId):
    header = write_header(perf_file_list, out_file, commitId)
    if len(header) > 0:
        out_file = Path(out_file)
        with out_file.open('a+',newline='') as f:
            writer = csv.DictWriter(f, header)
            for perf_file in perf_file_list:
                with open(perf_file, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    isSucceed = False
                    outdata = {}
                    for row in reader:
                        if row.get('iteration') is not None:
                            if row['iteration'] != "" and row['iteration'].isnumeric():
                                if int(row['iteration']) == 0:
                                    outdata[row['prompt_idx']] = row
                                elif int(row['iteration']) == 1:
                                    prompt_idx = row['prompt_idx']
                                    if prompt_idx in outdata:
                                        for key in row:
                                            if row[key] != "":
                                                outdata[prompt_idx][key] = row[key]
                                elif int(row['iteration']) > 1:
                                    prompt_idx = row['prompt_idx']
                                    if prompt_idx in outdata:
                                        for key in row:
                                            if is_number(row[key]) and is_number(outdata[prompt_idx][key]):
                                                if float(row[key]) < float(outdata[prompt_idx][key]):
                                                    outdata[prompt_idx][key] = row[key]
                            else:
                                break
                    if len(outdata) > 0:
                        isSucceed = True
                        for key in outdata:
                            outdata[key]['iteration'] = 'mini'
                            writer.writerow(outdata[key])
                    print(f"csv:{perf_file} output to min_each_column_file succeed:{isSucceed}")


def output_min_2nd_latency_to_file(perf_file_list, out_file, commitId):
    header = write_header(perf_file_list, out_file, commitId)
    if len(header) > 0:
        out_file = Path(out_file)
        with out_file.open('a+',newline='') as f:
            writer = csv.DictWriter(f, header)
            for perf_file in perf_file_list:
                with open(perf_file, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    isSucceed = False
                    outdata = {}
                    for row in reader:
                        if row.get('iteration') is not None:
                            if row['iteration'] != "" and row['iteration'].isnumeric():
                                if int(row['iteration']) == 0:
                                    outdata[row['prompt_idx']] = row
                                elif int(row['iteration']) == 1:
                                    prompt_idx = row['prompt_idx']
                                    if prompt_idx in outdata:
                                        for key in row:
                                            if row[key] != "":
                                                outdata[prompt_idx][key] = row[key]
                                elif int(row['iteration']) > 1:
                                    prompt_idx = row['prompt_idx']
                                    if prompt_idx in outdata:
                                        key = 'generation_time(s)'
                                        if is_number(row[key]) and is_number(outdata[prompt_idx][key]):
                                            if float(row[key]) < float(outdata[prompt_idx][key]):
                                                for key1 in row:
                                                    if row[key1] != "":
                                                        outdata[prompt_idx][key1] = row[key1]
                            else:
                                break
                    if len(outdata) > 0:
                        isSucceed = True
                        for key in outdata:
                            writer.writerow(outdata[key])
                    print(f"csv:{perf_file} output to min_2nd_latency_file succeed:{isSucceed}")


def write_header(perf_file_list, out_file, commitId, add_idx=False):
    header = []
    get_header_succ = False
    for perf_file in perf_file_list:
        warmup_data = read_warm_up_data(perf_file)
        if len(warmup_data) > 0:
            get_header_succ = True
            break
    if get_header_succ is True:
        if add_idx:
            header.append("idx")
        for key in warmup_data[0].keys():
            header.append(key)
        out_file = Path(out_file)
        with out_file.open('a+',newline='') as f:
            writer = csv.writer(f)
            result = "commit_id:" + commitId
            writer.writerow([result])

            writer = csv.DictWriter(f, header)
            writer.writeheader()
    return header


def is_number(string):
    if string.isnumeric():
        return True
    else:
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False


def remove_file(file):
    if os.path.exists(file):
        os.remove(file)


def get_argprser():
    parser = argparse.ArgumentParser("LLM benchmarking tool", add_help=True)
    parser.add_argument("-p", "--path", default="test_report", help="csv file path", required=TabError)
    parser.add_argument("-id", "--commitId", default="67fddb40", help="commit id of ov version")
    return parser.parse_args()


def main():
    args = get_argprser()
    base = args.path
    rename_csv(base)
    out_short_prompts_warmup_file = base + '/llm_summary_warmup_s.csv'
    out_short_prompts_avg_file = base + '/llm_summary_avg_s.csv'
    out_short_prompts_median_file = base + '/llm_summary_median_s.csv'
    out_all_short_prompts_file = base + '/llm_summary_all_data.csv'
    out_min_each_column_short_prompts_file = base + '/llm_summary_min_each_column_s.csv'
    out_min_2nd_latency_short_prompts_file = base + '/llm_summary_min_2nd_latency_s.csv'
    out_long_prompts_warmup_file = base + '/llm_summary_warmup_l.csv'
    out_long_prompts_avg_file = base + '/llm_summary_avg_l.csv'
    out_long_prompts_median_file = base + '/llm_summary_median_l.csv'
    out_all_long_prompts_file = base + '/llm_summary_all_data_l.csv'
    out_min_each_column_long_prompts_file = base + '/llm_summary_min_each_column_l.csv'
    out_min_2nd_latency_long_prompts_file = base + '/llm_summary_min_2nd_latency_l.csv'
    remove_file(out_short_prompts_warmup_file)
    remove_file(out_short_prompts_avg_file)
    remove_file(out_short_prompts_median_file)
    remove_file(out_all_short_prompts_file)
    remove_file(out_long_prompts_warmup_file)
    remove_file(out_long_prompts_avg_file)
    remove_file(out_long_prompts_median_file)
    remove_file(out_all_long_prompts_file)
    remove_file(out_min_each_column_short_prompts_file)
    remove_file(out_min_2nd_latency_short_prompts_file)
    remove_file(out_min_each_column_long_prompts_file)
    remove_file(out_min_2nd_latency_long_prompts_file)    
    perf_s_files, perf_l_files = findAllFile(base)

    if len(perf_s_files) > 0:
        # output warm-up data
        output_perf_data_to_csv(perf_s_files, out_short_prompts_warmup_file, args.commitId, 'avg', True)
        # output average data
        output_perf_data_to_csv(perf_s_files, out_short_prompts_avg_file, args.commitId, 'avg')
        # output median data
        output_perf_data_to_csv(perf_s_files, out_short_prompts_median_file, args.commitId, 'median')
        # output all data to a file
        output_all_data_to_file(perf_s_files, out_all_short_prompts_file, args.commitId)
        # output min value of each column to a file
        output_min_each_column_to_file(perf_s_files, out_min_each_column_short_prompts_file, args.commitId)
        # output min 2nd latency to a file
        output_min_2nd_latency_to_file(perf_s_files, out_min_2nd_latency_short_prompts_file, args.commitId)

    if len(perf_l_files) > 0:
        # output warm-up data
        output_perf_data_to_csv(perf_l_files, out_long_prompts_warmup_file, args.commitId, 'avg', True)
        # output average data
        output_perf_data_to_csv(perf_l_files, out_long_prompts_avg_file, args.commitId, 'avg')
        # output median data
        output_perf_data_to_csv(perf_l_files, out_long_prompts_median_file, args.commitId, 'median')
        # output all data to a file
        output_all_data_to_file(perf_l_files, out_all_long_prompts_file, args.commitId)
        # output min value of each column to a file
        output_min_each_column_to_file(perf_l_files, out_min_each_column_long_prompts_file, args.commitId)
        # output min 2nd latency to a file
        output_min_2nd_latency_to_file(perf_l_files, out_min_2nd_latency_long_prompts_file, args.commitId)

if __name__ == '__main__':
    main()
