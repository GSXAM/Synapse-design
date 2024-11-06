"""
1	dir1
1	dir1/par1
1	dir1/par1/into1
1	dir1/par1/into1/sub1
1	dir1/par1/into1/sub2
1	dir1/par1/into1/sub3
1	dir1/par1/into2
1	dir1/par2
1	dir1/par2/into1
1	dir2
1	dir2/pp1

9	dir1
6	dir1/par1
4	dir1/par1/into1
1	dir1/par1/into1/sub1
1	dir1/par1/into1/sub2
1	dir1/par1/into1/sub3
1	dir1/par1/into2
2	dir1/par2
1	dir1/par2/into1
2	dir2
1	dir2/pp1
"""

def calculate_total_files(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Lưu trữ thông tin đường dẫn và số lượng file vào dictionary
    file_dict = {}
    for line in lines:
        count, path = line.strip().split('\t')
        file_dict[path] = int(count)

    # Hàm đệ quy để tính tổng số file của một thư mục
    def get_total_files(path):
        total_files = file_dict[path]
        bypass_path = ""
        for sub_path in file_dict.keys():
            if sub_path.startswith(bypass_path + '/'):
                continue
            if sub_path.startswith(path + '/'):
                total_files += get_total_files(sub_path)
                bypass_path = sub_path
        return total_files

    # Tính toán tổng số file cho từng thư mục
    result_dict = {path: get_total_files(path) for path in file_dict.keys()}

    # In kết quả
    for path, total_files in result_dict.items():
        print(f'{total_files}\t{path}')

# Đường dẫn đến file text.txt
file_path = 'text.txt'
calculate_total_files(file_path)
