"""
Class for handling the ForeningLet Memberlist data
"""
import json
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta


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
    members_age_list = {}

    def __new__(cls, *args):
        """Make sure we create a clean memberlist object every time"""
        cls.count_men = 0
        cls.count_women = 0
        cls.genuine_member_count = 0
        cls.member_count = 0
        cls.memberlist = ""
        cls.memberlist_dataframe = pd.DataFrame()
        cls.members_age_list = {}
        return super().__new__(cls)

    def __init__(self, memberlist) -> None:
        self.memberlist = memberlist
        self._load_memberlist_to_dataframe()
        self._count_members()
        self._count_genuine_members()
        self._count_genders()
        self._create_member_ages_list()

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

    def _create_member_ages_list(self) -> None:
        """
        Method to count the number of members for each age in the memberlist.
        Will fill in 0 for an age, if no members have that age.
        """
        min_age = 0
        max_age = 0
        debug_count = 0
        for member in self.memberlist:
            debug_count += 1
            birthday = datetime.strptime(member["Birthday"], "%Y-%m-%d")
            now = datetime.now()
            diff = relativedelta(now, birthday)
            age = diff.years
            if self.members_age_list.get(age, None) is None:
                self.members_age_list[age] = 1
            else:
                self.members_age_list[age] += 1
            if age < min_age or min_age == 0:
                min_age = age
            if age > max_age or max_age == 0:
                max_age = age
        # We want the age list to contain the full range of ages from min_age to max_age
        # so fill in the ages not in the list with a 0
        for i in range(min_age, max_age - min_age):
            if self.members_age_list.get(i, None) is None:
                self.members_age_list[i] = 0
        # The list should be sorted by age ascending

        sorted_list = dict(sorted(self.members_age_list.items()))
        self.members_age_list = {}
        self.members_age_list = sorted_list
