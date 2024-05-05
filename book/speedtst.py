import speedtest

def network_speed():
    s = speedtest.Speedtest()
    s.get_best_server()
    download_speed = s.download() / 1024 / 1024
    upload_speed = s.upload() / 1024 / 1024
    return download_speed, upload_speed

download, upload = network_speed()
print(f"Скорость загрузки: {download:.2f} Мбит/с")
print(f"Скорость отдачи: {upload:.2f} Мбит/с")