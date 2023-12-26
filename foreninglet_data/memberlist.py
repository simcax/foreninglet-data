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
        self.count_men = df["Gender"].value_counts()["M"]
        self.count_women = df["Gender"].value_counts()["K"]
