import datetime
import json
import os

class SerpJSON:
    """ SERP JSON """
    def __init__(self, serp_json, dt):
        self.json = serp_json
        self.timestamp = datetime.datetime.fromtimestamp(dt.timestamp())
        self.date = dt.date()
        self.time = dt.time()
        self.page = self.json['results']['paging']['page']
        self.q = self.json['results']['urlParams']['q']
        self.upwork_relat_skill_ids = ','.join(self.json['results']['relevantSkillUids'])
        self.upwork_relative_skill_names = None
    # def try_or(self, func, default=None, expected_exc=(Exception,)):
    #     try:
    #         return func()
    #     except expected_exc:
    #         return default

class Profile:
    """ Single profile from SerpJSON """
    def __init__(self, pjson, keyword, page, timestamp):
        self.json = pjson
        self.keyword = keyword
        self.page = page
        self.timestamp = timestamp
        # <<< Simple fields >>>
        self.ciphertext = pjson['ciphertext']
        self.shortName = pjson['shortName']
        self.title = pjson['title']
        self.description = pjson['description']
        self.avgFeedbackScore = pjson['avgFeedbackScore']
        self.lastActivity = pjson['lastActivity']
        self.totalHoursBilled = pjson['totalHoursBilled']
        self.totalFeedbacks = pjson['totalFeedbacks']
        self.totalPortfolioItems = pjson['totalPortfolioItems']
        self.type = pjson['type']
        self.recentAvgFeedbackScore = pjson['recentAvgFeedbackScore']
        self.recentTotalFeedbacks = pjson['recentTotalFeedbacks']
        self.recentHoursBilled = pjson['recentHoursBilled']
        self.isRecommended = pjson['isRecommended']
        self.nss100 = pjson['nss100']
        self.totalActualHoursBilled = pjson['totalActualHoursBilled']
        self.topRatedStatus = pjson['topRatedStatus']
        self.billedAssignments = pjson['billedAssignments']
        self.totalRevenue = pjson['totalRevenue']
        self.combinedTotalRevenue = pjson['combinedTotalRevenue']
        self.totalHourlyJobs = pjson['totalHourlyJobs']
        self.totalFpJobs = pjson['totalFpJobs']
        self.curAssignments = pjson['curAssignments']
        self.hideEarnings = pjson['hideEarnings']
        self.combinedTotalEarnings = pjson['combinedTotalEarnings']
        self.combinedRecentEarnings = pjson['combinedRecentEarnings']
        self.combinedAverageRecentEarnings = pjson['combinedAverageRecentEarnings']
        self.combinedRecentCharge = pjson['combinedRecentCharge']
        self.combinedAverageRecentCharge = pjson['combinedAverageRecentCharge']
        self.memberSince = pjson['memberSince']
        self.vanityUrl = pjson['vanityUrl']
        self.topTalentGroup = pjson['topTalentGroup']
        self.offerConsultations = pjson['offerConsultations']
        self.totalCompletedJobs = pjson['totalCompletedJobs']
        self.isPIBAvailable = pjson['isPIBAvailable']
        self.descriptionSanitized = pjson['descriptionSanitized']
        self.shortNameSanitized = pjson['shortNameSanitized']
        self.titleSanitized = pjson['titleSanitized']
        self.topRatedStatusEx = pjson['topRatedStatusEx']
        self.uid = pjson['uid']

        # <<< Complex fields >>>
        self.location = pjson['location']
        self.hourlyRate = pjson['hourlyRate']
        self.skills = pjson['skills']
        self.agencies = pjson['agencies']
        self.highlighting = pjson['highlighting']
        self.rankInfo = pjson['rankInfo']
        self.ptcUids = pjson['ptcUids']
        self.scores = pjson['scores']
        self.scores_vemL1Score = pjson['scores']['vemL1Score']

        # <<< CUSTOM fields >>>
        self.url = 'https://www.upwork.com/freelancers/' + self.ciphertext
        self.skills_count = len(pjson['skills'])
        self.skills_ids = ','.join([x['uid'] for x in pjson['skills']])
        self.skills_names = None
        self.highlighting_blurb = pjson['highlighting']['blurb']
        self.export_fields = None





class ExportFields:

    def __init__(self, profile, sibl, profiles_list):
        self.description_words_count = len(profile.description.split())
        self.sibl_in_description = profile.description.lower().count(sibl)
        self.sibl_to_words_count_descr = self.sibl_in_description / self.description_words_count

        self.title_words_count = len(profile.title.split())
        self.sibl_in_title = profile.title.lower().count(sibl)
        self.sibl_to_words_count_title = self.sibl_in_title / self.title_words_count

        self.uid = profile.uid
        self.ciphertext = profile.ciphertext
        self.timestamp = profile.timestamp
        self.page = profile.page
        self.keyword = profile.keyword
        self.shortName =profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName
        # self.shortName = profile.shortName


    def get_min_max(self, param, cur_value, profiles_list):
        # min = [x for x in profiles_list]
        # vars()
        values_list = []
        for profile in profiles_list:
            cur_val = vars(profile)[param]
            values_list.append(cur_val)
        min = sorted(values_list, reverse=True)
        max = sorted(values_list, reverse=False)
        return min. max







