import argparse
from configparser import ConfigParser
import fnmatch
import os
import re
import sys


# 处理配置文件
cfg = ConfigParser()
cfg.read('./config.ini')

try:
    mkvmerge_path = cfg.get('mkvtoolnix','path')
    mkvmerge_exec = os.path.join(mkvmerge_path , 'mkvmerge.exe')
except BaseException:
    sys.stderr.write("Error: please config mkvtoolnix's path")
    sys.exit(2)
else:
    if not os.path.isfile(mkvmerge_exec):
        sys.stderr.write("Error: please config mkvtoolnix's path")
        sys.exit(2)

# 支持的文件类型列表
ext_list = ['flv','mp4','hlv','f4v','mkv']

# 处理参数
parser = argparse.ArgumentParser(
    description="merge all video files in current directory to a mkv file")

parser.add_argument(
    "-e", "--extension", 
    choices=ext_list,
    default=ext_list,
    help="the extension of file you want to merge")

parser.add_argument(
    "directory", 
    nargs='?', default=os.getcwd(),
    help="the directory files exists",
    )

parser.add_argument(
    "-o", "--output", 
    default=os.path.basename(os.getcwd()),
    help="output to filename 'OUTPUT'")

parser.add_argument(
    "-x", "--exclude", 
    default='',
    help="exclude files from input (wildcard is enabled)")

args = parser.parse_args()


# 逻辑开始
input_files_list = []
output_basename = re.sub('[^\w\-_\. ]', '', args.output)
output_ext = '.mkv'

work_dir = os.path.abspath(args.directory)
for name in os.listdir(work_dir):
    file_extension = os.path.splitext(name)[1]
    path = os.path.join(work_dir, name)
    if os.path.isfile(path) and file_extension[1:] and file_extension[1:] in args.extension:
        if not args.exclude :
            input_files_list.append(path)
        elif args.exclude and not fnmatch.fnmatch(name, args.exclude):
            input_files_list.append(path)

input_files_list.sort()
# 输出文件名
while os.path.isfile(os.path.join(work_dir, output_basename + output_ext)):
    output_basename = output_basename + '_copy'
output_name = output_basename + output_ext

command_and_args = []
command_and_args.append(mkvmerge_exec)
command_and_args.append('-o')
command_and_args.append(output_name)
command_and_args.append(' + '.join(input_files_list))
# print(input_files_list)
# print(' '.join(command_and_args))

os.system(' '.join(command_and_args))



