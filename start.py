from Bili import resources
# print(resources.config.videourl)

# url = "https://www.bilibili.com/bangumi/play/ss6360/"
url = "https://www.bilibili.com/bangumi/play/ep206639/"


g = resources.GatherDownloader(url=url)
 
  # for i in g.gen_info():
      # print(i)
 
g._save_gen_info_to_file()
g._save_base_content_text()

# a = resources.OneInGatherDownloader(url=url)
# print(a.ep_signature)
# a._save_one_info_to_file()

