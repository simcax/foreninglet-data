"""
Class for handling the ForeningLet Memberlist data
"""

import json
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger

from foreninglet_data.models.member_model import Member as MemberModel


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
    memberlist_dataframe_genuine_members = pd.DataFrame()
    members_age_list = {}
    new_members_previous_month = 0
    members_current_year = 0
    members_last_year = 0
    members_per_year = {}
    women_current_year = 0
    women_last_year = 0
    women_per_year = {}
    men_current_year = 0
    men_last_year = 0
    men_per_year = {}
    resignations_per_year = {}
    resignations_total = 0
    resignations_per_year_female = {}
    resignations_per_year_male = {}

    def __new__(cls, *args):
        """Make sure we create a clean memberlist object every time"""
        cls.count_men = 0
        cls.count_women = 0
        cls.genuine_member_count = 0
        cls.member_count = 0
        cls.memberlist = ""
        cls.memberlist_dataframe = pd.DataFrame()
        cls.memberlist_dataframe_genuine_members = pd.DataFrame()
        cls.members_age_list = {}
        cls.new_members_previous_month = 0
        cls.new_members_previous_month_percentage = 0
        cls.new_members_current_month = 0
        cls.new_members_current_month_percentage = 0
        cls.members_current_year = 0
        cls.members_per_year = {}
        cls.women_current_year = 0
        cls.women_last_year = 0
        cls.women_per_year = {}
        cls.men_current_year = 0
        cls.men_last_year = 0
        cls.men_per_year = {}
        cls.resignations_per_year = {}
        cls.resignations_total = 0
        cls.resignations_per_year_female = {}
        cls.resignations_per_year_male = {}
        return super().__new__(cls)

    def __init__(self, memberlist) -> None:
        self.memberlist = memberlist
        self._self_convert_members_to_membermodels()
        self._load_memberlist_to_dataframe()
        self._count_members()
        self._count_genuine_members()
        self._count_genders()
        self._create_member_ages_list()
        self._set_new_members_previous_month()
        self.set_new_members_current_month()
        self.set_members_per_year()
        self.set_members_per_gender_per_year()
        self._count_possible_resignations()

    def _self_convert_members_to_membermodels(self):
        """
        Method to make sure each member in the memberlist is a MemberModel object
        """
        for index, member in enumerate(self.memberlist):
            if not isinstance(member, MemberModel):
                member = MemberModel(**member)
                self.memberlist[index] = member

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
        df = self.memberlist_dataframe_genuine_members
        groups = df.groupby("Gender").size()
        men = 0
        women = 0
        if groups.get("M", "") != "":
            men = int(groups["M"])
        if groups.get("Mand", "") != "":
            men += int(groups["Mand"])
        if groups.get("K", "") != "":
            women = int(groups["K"])
        if groups.get("Kvinde", "") != "":
            women += int(groups["Kvinde"])
        self.count_men = men
        self.count_women = women

    def _count_possible_resignations(self):
        """
        Method to count the number of members who have not renewed their membership
        """
        if "ResignationDate" in self.memberlist_dataframe.columns:
            df = self.memberlist_dataframe_genuine_members
            df["ResignationDate"] = pd.to_datetime(
                df["ResignationDate"], errors="coerce"
            )
            possible_resignations = df.loc[
                (df["ResignationDate"].notnull()) & (df["GenuineMember"] == 1)
            ]
            possible_resignations_per_year = possible_resignations.groupby(
                possible_resignations["ResignationDate"].dt.strftime("%Y")
            ).size()
            self.resignations_per_year = possible_resignations_per_year.to_dict()
            self.resignations_total = len(possible_resignations)
            self.resignations_per_year_male = (
                possible_resignations.loc[possible_resignations["Gender"] == "Mand"]
                .groupby(possible_resignations["ResignationDate"].dt.strftime("%Y"))
                .size()
                .to_dict()
            )
            self.resignations_per_year_female = (
                possible_resignations.loc[possible_resignations["Gender"] == "Kvinde"]
                .groupby(possible_resignations["ResignationDate"].dt.strftime("%Y"))
                .size()
                .to_dict()
            )
            return len(possible_resignations)
        else:
            logger.warning(
                "ResignationDate column does not exist in the memberlist dataframe."
            )
            return 0

    def _load_memberlist_to_dataframe(self):
        """
        Method loading the memberlist to a dataframe
        """
        the_memberlist = self.memberlist
        if isinstance(the_memberlist, list):
            the_memberlist = json.dumps(self.memberlist)
        self.memberlist_dataframe = pd.read_json(the_memberlist)
        self.memberlist_dataframe_genuine_members = self.memberlist_dataframe.loc[
            self.memberlist_dataframe["GenuineMember"] == 1
        ]

    def _create_member_ages_list(self) -> None:
        """
        Method to count the number of members for each age in the memberlist.
        Will fill in 0 for an age, if no members have that age.
        """
        min_age = 0
        max_age = 0
        for member in self.memberlist:
            if member["Birthday"] == "":
                corrected_birthday = datetime.today().strftime("%Y-%m-%d")
                logger.warning(
                    f"Corrected birthday to be {corrected_birthday} for memberid: {member['MemberId']}, memberNumber: {member['MemberNumber']}, name: {member['FirstName']} {member['LastName']} "
                )
                member["Birthday"] = corrected_birthday
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

    # A method counting the number of members with an EnrollmentDate in the previous month
    def count_new_members_previous_month(self):
        """
        Method to count the number of members with an EnrollmentDate in the previous month
        """
        df = self.memberlist_dataframe
        now = datetime.now()
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year - 1 if now.month == 1 else now.year
        # convert EnrollmentDate to datetime
        df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
        prev_month_members = df.loc[
            (df["EnrollmentDate"].dt.month == prev_month)
            & (df["EnrollmentDate"].dt.year == prev_year)
        ]
        return len(prev_month_members)

    # A method setting class attributes for the number of members with an EnrollmentDate in the previous month
    def _set_new_members_previous_month(self):
        """
        Method to set class attributes for the number of members with an EnrollmentDate in the previous month
        """
        self.new_members_previous_month = self.count_new_members_previous_month()
        self.new_members_previous_month_percentage = (
            self.new_members_previous_month / self.member_count * 100
        )
        self.new_members_previous_month_percentage = round(
            self.new_members_previous_month_percentage, 2
        )
        self.new_members_previous_month_percentage = (
            f"{self.new_members_previous_month_percentage}%"
        )
        self.new_members_previous_month_percentage = (
            self.new_members_previous_month_percentage.replace(".", ",")
        )

    # Method to get the number of members with an EnrollmentDate in the current month
    def count_new_members_current_month(self):
        """
        Method to count the number of members with an EnrollmentDate in the current month
        """
        df = self.memberlist_dataframe
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        # convert EnrollmentDate to datetime
        df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
        current_month_members = df.loc[
            (df["EnrollmentDate"].dt.month == current_month)
            & (df["EnrollmentDate"].dt.year == current_year)
        ]
        return len(current_month_members)

    # Method to set class attributes for the number of members with an EnrollmentDate in the current month
    def set_new_members_current_month(self):
        """
        Method to set class attributes for the number of members with an EnrollmentDate in the current month
        """
        self.new_members_current_month = self.count_new_members_current_month()
        self.new_members_current_month_percentage = (
            self.new_members_current_month / self.member_count * 100
        )
        self.new_members_current_month_percentage = round(
            self.new_members_current_month_percentage, 2
        )
        self.new_members_current_month_percentage = (
            f"{self.new_members_current_month_percentage}%"
        )
        self.new_members_current_month_percentage = (
            self.new_members_current_month_percentage.replace(".", ",")
        )

    # METHOD to count the number of members per year
    def count_members_per_year(self):
        """
        Method to count the number of members per year
        """
        df = self.memberlist_dataframe
        # convert EnrollmentDate to datetime
        df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
        df_dates = (
            df[df["GenuineMember"] == 1]
            .groupby(df["EnrollmentDate"].dt.strftime("%Y"))
            .size()
        )
        return df_dates

    def count_members_per_gender_per_year(self):
        """
        Method to count the number of members per year, split by gender
        """
        df = self.memberlist_dataframe_genuine_members
        # convert EnrollmentDate to datetime
        df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
        df_gender_counts = (
            df.groupby([df["EnrollmentDate"].dt.strftime("%Y"), "Gender"])
            .size()
            .unstack(fill_value=0)
        )
        return df_gender_counts

    def set_members_per_year(self):
        """
        Method to set class attributes for the number of members per year
        """
        self.members_per_year = self.count_members_per_year()
        self.members_current_year = self.members_per_year.get(
            datetime.today().strftime("%Y"), 0
        )
        self.members_last_year = self.members_per_year.get(
            (datetime.today() - relativedelta(years=1)).strftime("%Y"), 0
        )
        self.members_per_year = self.members_per_year.to_dict()
        self.members_per_year = dict(sorted(self.members_per_year.items()))

    def get_addresses_and_zip_numbers(self) -> None:
        """Method to extract street addresses and zip numbers as a csv file"""
        df = self.memberlist_dataframe
        addresses = df[["Address", "Zip"]]
        addresses.to_csv("addresses.csv", index=False)

    def set_members_per_gender_per_year(self):
        """
        Method to set class attributes for the number of members per year
        split by gender
        """
        self.members_per_gender_per_year = self.count_members_per_gender_per_year()
        self.members_per_gender_per_year = self.members_per_gender_per_year.to_dict()
        current_year = datetime.today().strftime("%Y")
        last_year = (datetime.today() - relativedelta(years=1)).strftime("%Y")
        if self.members_per_gender_per_year.get("Mand") is None:
            self.men_current_year = 0
            self.men_last_year = 0
            self.men_per_year = {}
        else:
            self.men_current_year = self.members_per_gender_per_year.get(
                "Mand", {current_year: 0}
            ).get(current_year)
            self.men_last_year = self.members_per_gender_per_year.get("Mand").get(
                last_year
            )
            self.men_per_year = self.members_per_gender_per_year.get("Mand")

        if self.members_per_gender_per_year.get("Kvinde") is None:
            self.women_current_year = 0
            self.women_last_year = 0
            self.women_per_year = {}
        else:
            self.women_current_year = self.members_per_gender_per_year.get(
                "Kvinde", {current_year: 0}
            ).get(current_year)
            self.women_last_year = self.members_per_gender_per_year.get("Kvinde").get(
                last_year
            )
            self.women_per_year = self.members_per_gender_per_year.get("Kvinde")

    def count_members_per_membership_types(self):
        """
        Method to count the number of members per membership type
        """
        df = self.memberlist_dataframe
        # Count unique values in the MembershipType column and add to a dictionary
        self.membership_types = df["MembershipType"].value_counts().to_dict()
        return self.membership_types
