from Bili import resources
# print(resources.config.videourl)

url = "https://www.bilibili.com/bangumi/play/ss6360/"
g = resources.GatherDownloader(url=url)

 # for i in g.gen_info():
     # print(i)

g._save_gen_info_to_file()
