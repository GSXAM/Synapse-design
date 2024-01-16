#!/usr/bin/awk -f

BEGIN	{
    while (getline line < "input/inputfile.txt") {
        # Nếu là line Endpoint thì raise flag lên
        if (match(line, "Endpoint")) {
            ep_flag = 1;
            endpoint_val = line;
        }
        else if (match(line, "slack")) {
            # Lấy giá trị slack
            split(line, words, " ");
            slack_val = words[length(words)];
            # Check flag Endpoint, đảm bảo line trước slack là line Endpoint
            if (ep_flag) {
                # Duyệt mảng Endpoint, nếu có tồn tại Endpoint trong mảng thì so sánh slack
                for (EP_name in EP_arr) {
                    if (EP_name == endpoint_val) {
                        if (EP_arr[EP_name] > slack_val) {
                            EP_arr[EP_name] = slack_val;
                        }
                        # Reset flag Endpoint
                        ep_flag = 0;
                    }
                }
                # Nếu không tìm thấy Endpoint thì thêm Endpoint mới vào mảng
                if (ep_flag) {
                    EP_arr[endpoint_val] = 0;
                    ep_flag = 0;
                }
            }
        }
    }

    # In ra mang Endpoint
    for (EP_name in EP_arr) {
        print EP_name, ": ", EP_arr[EP_name];
    }
}