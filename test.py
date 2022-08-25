
class Str_test:
    def __init__(self, param):
        self.a = 'field_a'
        self.b = 'field_b'

class_test = Str_test('a')
print(vars(class_test)['a'])




# import glob
# import json
#
# files = glob.glob('D:\!!!!Andriy\Stats_upwork\parse\*.json')
# for f in files:
#     with open(f, 'r', encoding='utf-8') as file:
#         js = json.loads(file.read())
#         profiles = js['results']['profiles']
#         for p in profiles:
#             skills_ids = ','.join([x['uid'] for x in p['skills']])
#             d = p['description'].split()
#             c = p['description'].count('pars')
#
#             print(c)




# def try_or(func, default=None, expected_exc=(Exception,)):
#     try:
#         return func()
#     except expected_exc:
#         return default
# ids = ['111', '222']
# b = try_or(lambda:ids[2], default=None)
# print(b)