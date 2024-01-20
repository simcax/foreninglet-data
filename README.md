# foreninglet-data
Python module for generalising access to the ForeningLet (www.foreninglet.dk) member system API

# Current functionality
The project is work in progress. As of now, calling the ForeningLet API has been generalised, and the memberlist can be retrieved. 

A memberlist object can be genereated, and so far has functionality to count the members, and genders. 

# Installation
For now this code can be pip installed by referring to the get repo:

```bash
python -m pip install git+https://github.com/simcax/foreninglet-data
```

# Compulsory Settings
Export settings as environment variables:

```bash
API_USERNAME=username
API_PASSWORD=password
API_BASE_URL=https://foreninglet.dk/api/
API_VERSION=version=1
API_MEMBERS_API=members
API_ACTIVITIES_API=activities
```


# Usage
Then import:

```python
from foreninglet_data.api import ForeningLet
from foreninglet_data.memberlist import Memberlist
```

And get the memberlist:

```python
fl_obj = ForeningLet()
memberlist = fl_obj.get_memberlist()
memberlist_obj = Memberlist(memberlist)
```

Retrieve the membercount:

```python
# All members
memberlist.member_count
# All the GenuineMembers
memberlist.genuine_member_count
# The number of new members in the current month
memberlist.new_members_current_month
memberlist.new_members_current_month_percentage
# The number of new members in the previous month
memberlist.new_members_previous_month
memberlist.new_members_previous_month_percentage
```

Retrieve the count of genders:

```python
memberlist.count_men
memberlist.count_women
```

Getting a list of member ages 
```python
memberlist.member_age_list
```
This is a dict with a full range of each age from the youngest to the eldest member. 
In the case no members are of a given age, the dict will contain the age but a count of 0.

The dict is sorted by age.

i.e:
```python
{23: 1, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 1, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0, ...}
```

