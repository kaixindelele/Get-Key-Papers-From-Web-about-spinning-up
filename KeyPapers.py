import urllib.request
import re
import os


# 读取本地paper列表，返回有效信息的列表
def ReadTxtName(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            if len(line) > 2 and (line[0].isalnum() or line[0] == "."):
                lines.append(line)
    return lines


# 从arxiv网站链接获取PDF
def get_pdf_arxiv(web_site, path):
    rep = urllib.request.urlopen(urllib.request.Request(web_site))
    page = rep.read().decode('utf-8')
    pdf_download = re.findall('<meta name="citation_pdf_url" content="(.*?)"/>',page,re.S)
    print(pdf_download[0])
    if (len(pdf_download) != 0):
        try:
            u = urllib.request.urlopen(pdf_download[0])
        except urllib.error.HTTPError:
            print(pdf_download[0], "url file not found")
            return
        block_sz = 8192
        with open(path, 'wb') as f:
            while True:
                buffer = u.read(block_sz)
                if buffer:
                    f.write(buffer)
                else:
                    break
        print("Sucessful to download " + path)


# 直接从PDF链接下载PDF
def get_pdf_direct(web_site, path):
    rep = urllib.request.urlopen(urllib.request.Request(web_site))
    block_sz = 8192
    with open(path, 'wb') as f:
        while True:
            buffer = rep.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break
    print("Sucessful to download " + path)


def main():
    # 需要加入你的根目录

    root_dir = os.getcwd() + r"\url_txt.txt"
    txt_content = ReadTxtName(root_dir)
    paper_count = 1
    success_count = 0    
    failed_list = []
    
    # 先创建总的文件夹
    try:
        main_flie = txt_content[0]
        os.mkdir(main_flie)
    except Exception as e:
        print(e)
    
    class_file = txt_content[0] + "/" + txt_content[1] + "/"
    print("current file", class_file)
    
    for index, line in enumerate(txt_content[1:]):
        # print(index, line)
        # 再根据数字创建子文件夹
        if line[0].isdigit():
            # print(line)
            class_file = txt_content[0] + "/" + line + "/"
            paper_class_file = class_file
            try:
                os.mkdir(paper_class_file)                
            except Exception as e:
                print(e)
        # 如果是字母,则创建子文件夹，并更新paper file
        if line[0].isalpha():            
            paper_class_file = class_file + line + "/"            
            try:
                os.mkdir(paper_class_file)
            except Exception as e:
                print(e)

        if line[:2] == "..":
            paper_name = re.findall(r'`.* <', line)[0][1:-1]
            # 先去掉不能当文件名的冒号
            paper_name = paper_name.replace(r':', '-')
            try:
                paper_author = re.findall(r"_, .*, \d", line)[0][3:-3]
                if paper_author[-5:] == "et al":
                    paper_author = paper_author[:-5]
            except Exception as e:
                print(e)
            paper_year = re.findall(r'(\d+)', line)[-1]
            save_name = str(paper_count) + ". " + paper_year + "-" + paper_author + "-" + paper_name
    
            paper_url = re.findall(r"<.*>", line)[0][1:-1]
            end_save_path = paper_class_file + save_name + ".pdf"
            print(paper_count, " end_save_path:", end_save_path)

            # 这里可以指定下载哪个出现问题的文件。
            if paper_count > 0:
                # 处理一个积极拒绝爬虫的报错
                try:
                    if paper_url[-4:] == ".pdf":
                        try:
                            get_pdf_direct(web_site=paper_url, path=end_save_path)
                            success_count += 1
                            print("success_count:", success_count)
                        except Exception as e:
                            print(e)
                            failed_list.append([paper_count, paper_class_file, paper_url])
                    print(re.findall(r"arxiv", paper_url))
                    if re.findall(r"arxiv", paper_url):
                        try:
                            get_pdf_arxiv(web_site=paper_url, path=end_save_path)
                            success_count += 1
                            print("success_count:", success_count)
                        except Exception as e:
                            print(e)
                            failed_list.append([paper_count, paper_class_file, paper_url])
                except Exception as e:
                    print(e)
                    failed_list.append([paper_count, paper_class_file, paper_url])
            paper_count += 1
    
    print("failed list", failed_list)
    print("success count", success_count)
    fileObject = open('Failed List.txt', 'w')
    for ip in failed_list:
        fileObject.write(str(ip))
        fileObject.write('\n')
    fileObject.close()
    
    
if __name__ == '__main__':
    main()
