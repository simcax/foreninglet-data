"""
Class for handling the ForeningLet Memberlist data
"""
import json

import pandas as pd


class Memberlist:
    """
    Handles memberlist data from the ForeningLet API
    The class is instatiated by passing a JSON object containing memberlist data
    as it is returned from the API.
    """

    memberlist = ""
    member_count = 0
    count_men = 0
    count_women = 0

    def __init__(self, memberlist) -> None:
        self.memberlist = memberlist
        self.member_count = len(memberlist)
        self._count_genders()

    def _count_genders(self):
        """
        Method to count the number of men and women in the memberlist
        Men are signified by 'Gender' = 'M' (danish - M for Mand)
        Women are signified by 'Gender' = 'K' (danish - K for Kvinde)
        """
        the_memberlist = self.memberlist
        if isinstance(the_memberlist, list):
            the_memberlist = json.dumps(self.memberlist)
        df = pd.read_json(the_memberlist)
        groups = df.groupby("Gender").size()
        men = 0
        women = 0
        if groups.get("M", "") != "":
            men = groups["M"]
        if groups.get("K", "") != "":
            women = groups["K"]
        self.count_men = men
        self.count_women = women
