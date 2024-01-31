import json

def increase_num_in_jsonl(input_file_path, output_file_path, increase_amount=16152):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            # 解析 JSON 数据
            data = json.loads(line)

            # 增加 'num' 键的值
            if 'num' in data:
                data['num'] += increase_amount

            # 将修改后的 JSON 数据写入新文件
            output_file.write(json.dumps(data) + '\n')

# 使用函数
input_path = r'C:\Users\Morning\Desktop\hiwi\gpt_score\twitter_spider\twitter_spider\new_ethical ai_sentiment.jsonl'
output_path = 'output_file.jsonl'
increase_num_in_jsonl(input_path, output_path)
