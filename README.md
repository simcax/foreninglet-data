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
memberlist.member_count
```

Retrieve the count of genders:

```python
memberlist.count_men
memberlist.count_women
```

