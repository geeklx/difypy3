import os
import subprocess
import time

from flask import Flask, request, send_from_directory

app = Flask(__name__)

# 获取marp的路径os.getenv
# marp_path = os.getenv('MARP_PATH', '/Users/habhy/.npm-global/bin/marp')
# marp_path = os.getenv('MARP_PATH', 'C:/Users/liang/AppData/Roaming/npm/node_modules/@marp-team/marp-cli/marp-cli.js')
marp_path = os.getenv('MARP_PATH', 'C:/Users/liang/AppData/Roaming/npm/node_modules/@marp-team/marp-cli')
# marp_path = os.getenv('MARP_PATH', 'C:\\Users\liang\AppData\Roaming\npm\node_modules\@marp-team\marp-cli')
# 检查是否获取到了路径 C:\Users\liang\AppData\Roaming\npm\node_modules\@marp-team\marp-cli\node_modules
if marp_path:
    print(f"Marp 的路径是: {marp_path}")
else:
    print("未找到 Marp 的路径，请确保环境变量 MARP_PATH 已设置。")


# 保存上传的Markdown内容，并转换成PPT
@app.route('/ppt2upload/', methods=['POST'])
def upload_markdown():
    content = request.get_data(as_text=True)
    timestamp = str(int(time.time()))
    md_filename = f"{timestamp}.md"
    pptx_filename = f"{timestamp}.pptx"

    # 保存Markdown文件
    with open(f"tmp/{md_filename}", 'w', encoding='utf-8') as f:
        f.write(content)

        # 检查文件是否存在
    md_file = f"tmp/{md_filename}"
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} does not exist.")
    else:
        print("File exists.")
    ppt_file = f"tmp/{pptx_filename}"
    if not os.path.exists(ppt_file):
        print(f"Error: File {ppt_file} does not exist.")
    else:
        print("File exists.")

    # 使用marp-cli将Markdown转换为PPT
    try:
        subprocess.run([marp_path, f'tmp/{md_filename}', '-o', f'tmp/{pptx_filename}'],
                       shell=True,
                       check=True)
    except subprocess.CalledProcessError as e:
        return {
            'message': 'Failed to convert Markdown to PPT',
            'error': str(e)
        }

    # 返回文件链接

    return f'Markdown 文件已保存\n预览链接: http://127.0.0.1:5004/tmp/{md_filename} \n下载链接: http://127.0.0.1:5004/tmp/{pptx_filename}?pptx'


# 提供静态文件服务
@app.route('/tmp/<path:filename>')
def serve_file(filename):
    return send_from_directory('tmp', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1112)
