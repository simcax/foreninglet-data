"""
Class for handling the ForeningLet Memberlist data
"""

import json
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger

from foreninglet_data.models.member_model import Member


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
    count_members_under_25 = 0
    memberlist_dataframe = pd.DataFrame()
    members_age_list = {}
    new_members_previous_month = 0
    members_current_year = 0
    members_last_year = 0
    members_per_year = {}

    def __new__(cls, *args):
        """Make sure we create a clean memberlist object every time"""
        cls.count_men = 0
        cls.count_women = 0
        cls.count_members_under_25 = 0
        cls.genuine_member_count = 0
        cls.member_count = 0
        cls.memberlist = ""
        cls.memberlist_dataframe = pd.DataFrame()
        cls.members_age_list = {}
        cls.new_members_previous_month = 0
        cls.new_members_previous_month_percentage = 0
        cls.new_members_current_month = 0
        cls.new_members_current_month_percentage = 0
        cls.members_current_year = 0
        cls.members_per_year = {}
        return super().__new__(cls)

    def __init__(self, memberlist) -> None:
        self.memberlist = memberlist
        self._load_memberlist_to_dataframe()
        self._count_members()
        self._count_genuine_members()
        self._count_genders()
        self._count_members_under_25()
        self._create_member_ages_list()
        self._set_new_members_previous_month()
        self.set_new_members_current_month()
        self.set_members_per_year()

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

    def _count_members_under_25(self):
        """
        Method to count the number of members who are 25 years old or younger
        """
        count = 0
        for member in self.memberlist:
            if member["Birthday"] == "":
                # Skip members with no birthday - they won't be counted
                continue
            try:
                birthday = datetime.strptime(member["Birthday"], "%Y-%m-%d")
                now = datetime.now()
                diff = relativedelta(now, birthday)
                age = diff.years
                if age <= 25:
                    count += 1
            except (ValueError, TypeError):
                # Skip members with invalid birthday format
                continue
        self.count_members_under_25 = count

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

    def count_members_in_municipality_over_under_25(
        self,
        zip_code: str,
        member_in_year: int = None,
        include_membership_breakdown: bool = False,
    ) -> dict:
        """
        Count members over and under 25, living in and outside of the specified zip code.
        Optionally include breakdown by membership type and months of membership.

        Args:
            zip_code (str): The zip code to check against
            member_in_year (int, optional): Year to filter members by enrollment date.
                                          Only count members who were already enrolled in this year.
            include_membership_breakdown (bool): Include breakdown by membership type and months

        Returns:
            dict: Dictionary with counts for each category:
                - inside_zip_under_25: Members under 25 in the specified zip code
                - inside_zip_over_25: Members 25 and over in the specified zip code
                - outside_zip_under_25: Members under 25 outside the specified zip code
                - outside_zip_over_25: Members 25 and over outside the specified zip code

                If include_membership_breakdown=True, also includes:
                - membership_breakdown: Dict with membership type breakdowns
                - total_membership_months: Total months of membership for the year
        """
        counts = {
            "inside_zip_under_25": 0,
            "inside_zip_over_25": 0,
            "outside_zip_under_25": 0,
            "outside_zip_over_25": 0,
        }

        if include_membership_breakdown:
            membership_breakdown = {}
            total_membership_months = 0
            year_start = (
                datetime(member_in_year, 1, 1)
                if member_in_year
                else datetime(datetime.now().year, 1, 1)
            )
            year_end = (
                datetime(member_in_year, 12, 31)
                if member_in_year
                else datetime(datetime.now().year, 12, 31)
            )

        for member_data in self.memberlist:
            try:
                # Skip members without birthday or zip code
                if not member_data.get("Birthday") or not member_data.get("Zip"):
                    continue

                # Skip members without enrollment date if year filter is specified
                if member_in_year is not None and not member_data.get("EnrollmentDate"):
                    continue

                # Filter by enrollment year if specified
                if member_in_year is not None:
                    enrollment_date = datetime.strptime(
                        member_data["EnrollmentDate"], "%Y-%m-%d"
                    )
                    enrollment_year = enrollment_date.year
                    # Skip members who enrolled after the specified year
                    if enrollment_year > member_in_year:
                        continue

                # Calculate age
                birthday = datetime.strptime(member_data["Birthday"], "%Y-%m-%d")
                now = datetime.now()
                diff = relativedelta(now, birthday)
                age = diff.years

                # Get member zip code as string for comparison
                member_zip = str(member_data["Zip"])

                # Determine if member is under or over 25
                is_under_25 = age < 25
                # Determine if member lives in the specified zip code
                is_inside_zip = member_zip == zip_code

                # Increment appropriate counter
                if is_inside_zip:
                    if is_under_25:
                        counts["inside_zip_under_25"] += 1
                    else:
                        counts["inside_zip_over_25"] += 1
                else:
                    if is_under_25:
                        counts["outside_zip_under_25"] += 1
                    else:
                        counts["outside_zip_over_25"] += 1

                # Handle membership breakdown if requested
                if include_membership_breakdown:
                    # Get membership type using helper method
                    membership_type = self._get_membership_for_member(member_data)

                    # Initialize membership breakdown structure if not exists
                    if membership_type not in membership_breakdown:
                        membership_breakdown[membership_type] = {
                            "inside_zip_under_25": 0,
                            "inside_zip_over_25": 0,
                            "outside_zip_under_25": 0,
                            "outside_zip_over_25": 0,
                            "total_months": 0,
                        }

                    # Count by membership type and location/age
                    if is_inside_zip:
                        if is_under_25:
                            membership_breakdown[membership_type][
                                "inside_zip_under_25"
                            ] += 1
                        else:
                            membership_breakdown[membership_type][
                                "inside_zip_over_25"
                            ] += 1
                    else:
                        if is_under_25:
                            membership_breakdown[membership_type][
                                "outside_zip_under_25"
                            ] += 1
                        else:
                            membership_breakdown[membership_type][
                                "outside_zip_over_25"
                            ] += 1

                    # Calculate months of membership in the specified year
                    enrollment_start = max(enrollment_date, year_start)
                    membership_end = min(datetime.now(), year_end)

                    if enrollment_start <= membership_end:
                        months_diff = relativedelta(membership_end, enrollment_start)
                        months_in_year = (
                            months_diff.months
                            + (months_diff.years * 12)
                            + (1 if months_diff.days > 0 else 0)
                        )
                        membership_breakdown[membership_type]["total_months"] += (
                            months_in_year
                        )
                        total_membership_months += months_in_year

            except (ValueError, TypeError):
                # Skip members with invalid date formats
                continue

        if include_membership_breakdown:
            counts["membership_breakdown"] = membership_breakdown
            counts["total_membership_months"] = total_membership_months

        return counts

    def _get_membership_for_member(self, member_data: dict) -> str:
        """
        Helper method to get membership type for a member using the Member model validation.
        
        Args:
            member_data (dict): Member data dictionary
            
        Returns:
            str: Membership type name or "Unknown" if unable to determine
        """
        try:

            
            # Create a minimal Member instance just to get the membership
            # Fill in required fields with defaults if missing
            member_dict = member_data.copy()
            
            # Ensure required fields have values and fix data type issues
            required_defaults = {
                "MemberId": member_dict.get("MemberId", 0),
                "MemberNumber": member_dict.get("MemberNumber", 0),
                "MemberCode": member_dict.get("MemberCode", ""),
                "FirstName": member_dict.get("FirstName", ""),
                "LastName": member_dict.get("LastName", ""),
                "Address": member_dict.get("Address", ""),
                "Zip": member_dict.get("Zip", 0),
                "City": member_dict.get("City", ""),
                "CountryCode": member_dict.get("CountryCode", "DK"),
                "Email": member_dict.get("Email", ""),
                "Birthday": member_dict.get("Birthday", ""),
                "Gender": member_dict.get("Gender", ""),
                "EnrollmentDate": member_dict.get("EnrollmentDate", ""),
            }
            
            # Update member_dict with defaults for missing required fields
            for key, default_value in required_defaults.items():
                if key not in member_dict or member_dict[key] is None:
                    member_dict[key] = default_value
            
            # Fix data type issues identified in validation errors
            
            # Fix SaldoPaymentDeadline - convert int to string
            if "SaldoPaymentDeadline" in member_dict and isinstance(member_dict["SaldoPaymentDeadline"], int):
                member_dict["SaldoPaymentDeadline"] = str(member_dict["SaldoPaymentDeadline"])
            elif "SaldoPaymentDeadline" not in member_dict:
                member_dict["SaldoPaymentDeadline"] = ""
            
            # Fix activity_ids - convert list to comma-separated string
            if "activity_ids" in member_dict:
                if isinstance(member_dict["activity_ids"], list):
                    member_dict["activity_ids"] = ",".join(str(id) for id in member_dict["activity_ids"])
                elif member_dict["activity_ids"] is None:
                    member_dict["activity_ids"] = ""
            else:
                member_dict["activity_ids"] = ""
            
            member = Member(**member_dict)
            return member.Membership if member.Membership else "Unknown"
            
        except Exception:
            return "Unknown"
