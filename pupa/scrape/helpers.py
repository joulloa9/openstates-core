""" these are helper classes for object creation during the scrape """
from .popolo import Person, Organization, Membership


class Legislator(Person):
    """
    Legislator is a special case of Person that has a district, party, and perhaps a chamber
    """
    def __init__(self, name, district, party=None, chamber=None, role='member', **kwargs):
        super(Legislator, self).__init__(name, **kwargs)
        self._district = district
        self._party = party
        self._chamber = chamber
        self._role = role

    def pre_save(self, jurisdiction_id):
        # before saving create a membership to the current jurisdiction
        membership = Membership(
            self._id,
            # placeholder id is jurisdiction:chamber:id
            'legislature:' + (self._chamber or '') + ':' + jurisdiction_id,
            # post placeholder id is district:chamber:name
            post_id='district:' + (self._chamber or '') + ':' + self._district,
            role=self._role)
        self._related.append(membership)

        # create a party membership
        if self._party:
            membership = Membership(self._id, 'party:' + self._party, role='member')
            self._related.append(membership)


class Committee(Organization):
    """
    Committee is a special Organization that makes it easy to add members
    """

    def __init__(self, name, chamber=None, **kwargs):
        super(Committee, self).__init__(name=name, classification='committee', chamber=chamber,
                                        **kwargs)

    def pre_save(self, jurisdiction_id):
        # before saving set parent to the chamber
        if not self.parent_id:
            self.parent_id = 'legislature:' + (self.chamber or '') + ':' + jurisdiction_id

    def add_member(self, name_or_person, role='member', **kwargs):
        if isinstance(name_or_person, Person):
            membership = Membership(person_id=name_or_person._id, organization_id=self._id,
                                    role=role, **kwargs)
        else:
            membership = Membership(person_id=None, organization_id=self._id, role=role,
                                    unmatched_legislator={'name': name_or_person}, **kwargs)
        self._related.append(membership)