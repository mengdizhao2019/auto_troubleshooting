import re
import json
import os
from utility import convert_to_filename
from execution_obj import ExecutionObj, ExecutionDef, ExecutionObjEncoder,MatchDef,SingleStrategy, ExecutionDefEncoder, ExecutionDefDecoder
import param_filter

def extract_example_category(s):
    # 匹配 example 字段
    example_match = re.search(r'example\s*=\s*\[\[(.*?)\]\]', s)
    if example_match:
        example = example_match.group(1)
    else:
        example = None

    # 匹配 category 字段
    category_match = re.search(r'{name\s*=\s*"category"\s*;\s*pattern\s*=\s*lpeg\.Cc\("(.*?)"\)}', s)
    if category_match:
        category = category_match.group(1)
    else:
        category = None

        
    # 匹配 description 字段
    description_match = re.search(r'{name\s*=\s*"description"\s*;\s*pattern\s*=\s*lpeg\.Cc\("(.*?)"\)}', s)
    if description_match:
        description = description_match.group(1)
    else:
        description = None

    # 匹配 level 字段
    level_match = re.search(r'{name\s*=\s*"level"\s*;\s*pattern\s*=\s*lpeg\.Cc\("(.*?)"\)}', s)
    if level_match:
        level = level_match.group(1)
    else:
        level = None

    # # regex part
    # pattern = r'{prefix\s*=\s*"(.+?)".+?name\s*=\s*"(.+?)".+?pattern\s*=\s*(.+?)\s*},'
    # matches = re.findall(pattern, s, re.DOTALL)

    # # 打印匹配结果
    # for m in matches:
    #     print('prefix:', m[0])
    #     print('name:', m[1])
    #     print('pattern:', m[2])

    
    # 使用正则表达式搜索含有"prefix"的整行字符串
    pattern = r'.*prefix.*'
    matches = re.findall(pattern, s)

    # 输出搜索结果
    prefix = ""
    for match in matches:
        prefix += match

    return example, category, description, level, prefix

def find_string(s):
    stack = []
    start_index = None
    for i, c in enumerate(s):
        if c == '{':
            stack.append(i)
            if start_index is None:
                start_index = i  # 记录第一个左括号的位置   
        elif c == '}':
            stack.pop()
            if not stack:
                # 找到第一个左括号开始的字符串
                if start_index is not None:
                    return s[start_index:i+1]
        
    return None  # 没有找到左括号，返回空字符串或 None

def DoProcessOne(filepath, outputfolder):
    ss = ""
    filename = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        ss = f.read()

    ret = re.search(r'(local\s+\w+\s+=\s*\{)', ss)
    firstBracket = ret.group()
    #print(firstBracket)
    begin = ss.find(firstBracket)
    end = ss.rfind('}')

    properties = {}
    if begin!=-1 and end!=-1:
        
        contents = ss[begin + len(firstBracket):end]
        #print(contents)
    
        ll = []
        ret = find_string(contents)
        while ret:
            itemContent = ret.strip('{').strip('}').strip()
            print(itemContent)

            example, category, description, level, prefix = extract_example_category(itemContent)
            if not example or example=="":
                continue
            #print("example:{}, category:{}, description:{}, level:{}".format( example, category, description, level))
            properties['example'] = example
            properties['category'] = category
            properties['description'] = description
            properties['level'] = level
            properties['prefix'] = prefix

            ed = ExecutionDef('{}_{}_{}'.format(filename,category,description), 'log')
            ed._defInfo = properties
            ed._matchDefList.append(MatchDef('simple_string', example))
            
            ed._collect.append('pid')
            ed._collect.append('msg')
            #ed._collect.append('time')
            ed._groupby.append('pid')

            ll.append(ed)
            
            ed_filename = os.path.join(outputfolder, '{}_{}_P{}.json'.format(filename, convert_to_filename(category), convert_to_filename(description)))
            with open( ed_filename, 'w') as file:
                json_data = json.dumps(ed, cls= ExecutionDefEncoder, indent=4)
                file.write(json_data)

            with open(ed_filename, 'r') as f:
                ed_cp = json.load(f, cls=  ExecutionDefDecoder)
                print('ed_cp:', ed_cp._name)
                
            #print(itemContent)
            contents = contents.replace(ret, ' ')
            ret = find_string(contents)
            
     
    # if len(ll) == 0:
    #     return
    # eo = ExecutionObj(ll)

    
    # with open(filename + '.json', 'w') as file:
    #     json_data = json.dumps([eo], cls= ExecutionObjEncoder)
    #     file.write(json_data)

        
if __name__ == '__main__':
    scanfolder = r'C:\temp\auto_troubleshooting\sm'
    outputfolder = r'C:\temp\auto_troubleshooting\sm\converted'

    for root, dirs, files in os.walk(scanfolder):
        for file in files:
            file_path = os.path.join(root, file)
            
            _, extension = os.path.splitext(file_path)
            if extension != ".lua":
                continue
            print(file_path)

            DoProcessOne(file_path, outputfolder)