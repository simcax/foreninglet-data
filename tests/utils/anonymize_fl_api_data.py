"""
    Anonymise data files for testing
"""
import json
import os
import random
from pathlib import Path

import typer
import yaml
from faker import Faker
from typing_extensions import Annotated

app = typer.Typer(
    help="Anonymizes data from the ForeningLet API, so personal data is not spread"
)


@app.command()
def anonymize_data(
    input_file: Annotated[
        (str, typer.Argument(help="Full path to the file needed to be anonimized"))
    ] = None
) -> bool:
    """
    Loads input file and anonymizes the data,
    then outputs a new file with anonymized content
    Original filename appended with _anon
    """
    if input_file is None:
        member_data = None
    else:
        input_file_path = Path(input_file)
        if input_file_path.exists is False:
            raise OSError("No such file")

        data = input_file_path.read_text(encoding="utf-8")
        yaml_data = yaml.safe_load(data)
        member_data = json.loads(
            yaml_data["interactions"][0]["response"]["body"]["string"]
        )

    if member_data is None:
        member_data = []
        for i in range(1, 200):
            member_data.append(sub_member_data())
    else:
        i = 0
        for member in member_data:
            member = sub_member_data(member)
            member_data[i] = member
            i += 1

    yaml_data["interactions"][0]["response"]["body"]["string"] = json.dumps(member_data)
    output_file = os.path.join(
        input_file_path.parent, f"{input_file_path.stem}_anon{input_file_path.suffix}"
    )
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(yaml.dump(yaml_data))
        # outfile.write(json.dumps(yaml_data))


@app.command()
def member_fields():
    """
    Prints out all the field names
    """
    fields = {
        "MemberId": 911516,
        "MemberNumber": 19751,
        "MemberCode": "x6tnBEr4&i",
        "FirstName": "Karla",
        "LastName": "Nilsson",
        "Address": "B\u00e6kkeskovvej 957",
        "Address2": "",
        "Zip": "4565",
        "City": "H\u00f8ng",
        "CountryCode": "DK",
        "Email": "hbruun@example.com",
        "Birthday": "1916-03-14",
        "Gender": "K",
        "Phone": "96 94 77 51",
        "Mobile": "+45 91 79 53 30",
        "EnrollmentDate": "2020-04-12",
        "DeliveryMethod": "Manuelt",
        "PbsAgreementNumber": "0",
        "Note": "Konventionelle trick g\u00e5rd enhed adgang.",
        "Password": "wDCm*_d$+4",
        "Saldo": "0.00",
        "SaldoPaymentDeadline": 0,
        "Created": "2020-04-12T15:07:48+0000",
        "Updated": "2022-11-15T05:28:57+0000",
        "Property": "",
        "GenuineMember": "1",
        "Image": "1",
        "ReceiveNewsletter": "0",
        "MemberField1": "2",
        "MemberField2": "Ja",
        "MemberField3": 552,
        "MemberField4": "",
        "MemberField5": "",
        "MemberField6": "",
        "MemberField7": "",
        "MemberField8": "",
        "MemberField9": "",
        "MemberField10": "",
        "MemberField11": "",
        "MemberField12": "",
        "MemberField13": "",
        "MemberField14": "",
        "MemberField15": "",
        "MemberField16": "",
        "MemberField17": "",
        "MemberField18": "",
        "MemberField19": "",
        "MemberField20": "",
        "ConsentField1": "Ja",
        "ConsentField2": "Ja",
        "ConsentField3": "",
        "ConsentField4": "",
        "ConsentField5": "",
        "Activities": "45057, 48331, 51654, 57390, 68173, 95039, 95041, 96867, 97037, 97040",
        "activity_ids": [
            "45057",
            "48331",
            "51654",
            "57390",
            "68173",
            "95039",
            "95041",
            "96867",
            "97037",
            "97040",
        ],
    }
    for field in fields:
        print(field)


def sub_member_data(member: dict = None) -> dict:
    """
    Substitutes data in a member dict or creates fake data
    """
    if member is None:
        member = {}
    # Faker.seed()
    fake = Faker("da_DK")
    delivery_method = [
        "Manuel",
        "Email",
        "Dankort automatisk tr\u00e6k",
        "Email/Dankort & udlandskort",
    ]
    saldi = [0, 400, 750, 1250]
    member_field_1_values = ["ja", "nej"]
    consent_field_values = ["ja", "nej"]
    sex = {"M": "M", "F": "K"}
    member["MemberId"] = random.randrange(999999)
    member["MemberNumber"] = random.randrange(99999)
    member["MemberCode"] = fake.password()
    member["FirstName"] = fake.first_name()
    member["LastName"] = fake.last_name()
    member["Address"] = fake.street_address()
    member["Zip"] = fake.postcode()
    member["City"] = fake.city()
    member["CountryCode"] = "DK"
    member["Email"] = fake.email()
    member["Birthday"] = fake.date_of_birth(minimum_age=15).strftime("%Y-%m-%d")
    member["Gender"] = sex[fake.profile()["sex"]]
    member["Phone"] = fake.phone_number()
    member["Mobile"] = fake.phone_number()
    member["EnrollmentDate"] = fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d")
    member["DeliveryMethod"] = delivery_method[random.randrange(len(delivery_method))]
    member["Note"] = fake.paragraph(nb_sentences=1)
    member["Password"] = fake.password()
    member["Saldo"] = saldi[random.randrange(len(saldi))]
    member["SaldoPaymentDeadline"] = 0
    member["Created"] = fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d")
    member["Updated"] = fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d")
    member["Property"] = ""
    member["GenuineMember"] = 1
    member["Image"] = random.randrange(1)
    member["ReceiveNewsletter"] = random.randrange(1)
    member["MemberField1"] = random.randrange(1)
    member["MemberField2"] = member_field_1_values[
        random.randrange(len(member_field_1_values))
    ]
    member["MemberField3"] = random.randrange(999)
    member["ConsentField1"] = consent_field_values[
        random.randrange(len(consent_field_values))
    ]
    member["ConsentField2"] = consent_field_values[
        random.randrange(len(consent_field_values))
    ]
    ids = ""
    id_list = []
    id_comma = ""
    for i in range(1, 10):
        activity_id = random.randrange(40000, 50000)
        ids += f"{id_comma}{activity_id}"
        id_list.append(activity_id)
        id_comma = ","
    member["Activities"] = ids
    member["activity_ids"] = id_list
    return member


if __name__ == "__main__":
    app()
