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
    genuine_member_count = 0
    member_count = 0
    count_men = 0
    count_women = 0
    memberlist_dataframe = pd.DataFrame()

    def __init__(self, memberlist) -> None:
        self.memberlist = memberlist
        self._load_memberlist_to_dataframe()
        self._count_members()
        self._count_genuine_members()
        self._count_genders()

    def _count_members(self):
        """
        Method to count the number of members
        """
        df = self.memberlist_dataframe
        self.member_count = len(df)

    def _count_genuine_members(self):
        """
        Method to get the count of genuine members
        """
        df = self.memberlist_dataframe
        self.genuine_member_count = len(df.loc[df["GenuineMember"] == 1])

    def _count_genders(self):
        """
        Method to count the number of men and women in the memberlist
        Men are signified by 'Gender' = 'M' (danish - M for Mand)
        Women are signified by 'Gender' = 'K' (danish - K for Kvinde)
        """
        df = self.memberlist_dataframe
        groups = df.groupby("Gender").size()
        men = 0
        women = 0
        if groups.get("M", "") != "":
            men = groups["M"]
        if groups.get("Mand", "") != "":
            men += groups["Mand"]
        if groups.get("K", "") != "":
            women = groups["K"]
        if groups.get("Kvinde", "") != "":
            women += groups["Kvinde"]
        self.count_men = men
        self.count_women = women

    def _load_memberlist_to_dataframe(self):
        """
        Method loading the memberlist to a dataframe
        """
        the_memberlist = self.memberlist
        if isinstance(the_memberlist, list):
            the_memberlist = json.dumps(self.memberlist)
        self.memberlist_dataframe = pd.read_json(the_memberlist)
