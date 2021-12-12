class Player():

        def is_valid(self):
                return self.username != "" and self.housenumber != "" and self.cgnumber != ""

        def separate_args_with_commas(self, *args):
            args = map(lambda x: str(x), args)
            return ",".join(args)

        def to_csv_row(self):
            return self.separate_args_with_commas(self.username, self.playername, self.genderpref, self.genderplayer, self.interests, self.twotruthsonelie, self.introduction, self.housenumber, self.cgnumber, self.yearofstudy, self.faculty)

        def __init__(self, **kwargs):
                self.username = kwargs.get('username')
                self.playername = kwargs.get('playername')
                self.genderpref = kwargs.get('genderpref')
                self.genderplayer = kwargs.get('genderplayer')
                self.interests = kwargs.get('interests')
                self.twotruthsonelie = kwargs.get('twotruthsonelie')
                self.introduction = kwargs.get('introduction')
                self.housenumber = kwargs.get('housenumber')
                self.cgnumber = kwargs.get('cgnumber')
                self.yearofstudy = kwargs.get('yearofstudy')
                self.faculty = kwargs.get('faculty')

        def __repr__(self):
                return str(self.username)

