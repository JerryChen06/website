class Verb:
    """Object representing a verb in Croatian, including its English translations

    Attributes:
    - inf: infinitive form (e.g. 'ići')
    - pres: present stem (e.g. 'id')
    - part: past-participle stem (e.g. 'iš')
    - irregular: whether infinitive stem != present stem
    - them_vowel: thematic vowel class ('a','i','e','ova','nu')
    - english: tuple[translation in present, past, participle]
    """
    def __init__(self, inf: str, pres: str, part: str,
                 eng: tuple[str, str, str], them_vowel: str):
        self.inf = inf
        self.pres = pres
        self.part = part
        self.english = eng
        self.irregular = inf[:-2] != pres
        self.them_vowel = them_vowel

    def present(self, person: int, number: str, gender: str = 'm') -> str:
        """Return present tense form: person=1,2,3 ; number='sg' or 'pl'"""
        pronoun = {
            1: {'sg': 'Ja', 'pl': 'Mi'},
            2: {'sg': 'Ti', 'pl': 'Vi'},
            3: {'sg': {'m': 'On', 'f': 'Ona', 'n': 'Ono'}[gender],
                'pl': {'m': 'Oni', 'f': 'One', 'n': 'Ona'}[gender]},
        }[person][number]

        # exceptions for suppletive verbs
        if self.inf == 'biti':
            stems = {
                '1sg': 'sam', '2sg': 'si', '3sg': 'je',
                '1pl': 'smo', '2pl': 'ste', '3pl': 'su'
            }
            return stems[f"{person}{number}"]
        if self.inf == 'htjeti':
            stems = {
                '1sg': 'hoću', '2sg': 'hoćeš', '3sg': 'hoće',
                '1pl': 'hoćemo', '2pl': 'hoćete', '3pl': 'hoće'
            }
            return stems[f"{person}{number}"]
        if self.inf == 'moći':
            stems = {
                '1sg': 'mogu', '2sg': 'možeš', '3sg': 'može',
                '1pl': 'možemo', '2pl': 'možete', '3pl': 'mogu'
            }
            return stems[f"{person}{number}"]
        # regular pattern
        endings = {
            'a': { 'sg': ('am','aš','a'), 'pl': ('amo','ate','aju') },
            'i': { 'sg': ('im','iš','i'), 'pl': ('imo','ite','e') },
            'e': { 'sg': ('em','eš','e'), 'pl': ('emo','ete','u') },
            'ova': { 'sg': ('ujem','uješ','uje'), 'pl': ('ujemo','ujete','uju') },
            'nu': { 'sg': ('nem','neš','ne'), 'pl': ('nemo','nete','nu') }
        }
        cls = self.them_vowel
        idx = person - 1
        suf = endings[cls][number][idx]
        se = ""
        if " se" in self.inf:
            se = " se"
        return ' '.join([pronoun, self.pres + suf + se])

    def perfect(self, person: int, number: str, gender: str = 'm') -> str:
        """biti (present) + past participle"""
        pronoun = {
            1: {'sg': 'Ja', 'pl': 'Mi'},
            2: {'sg': 'Ti', 'pl': 'Vi'},
            3: {'sg': {'m': 'On', 'f': 'Ona', 'n': 'Ono'}[gender],
                'pl': {'m': 'Oni', 'f': 'One', 'n': 'Ona'}[gender]},
        }[person][number]

        if number == 'pl':
            suffix = {'m': 'li', 'f': 'le', 'n': 'la'}[gender]
        else:
            suffix = {'m': 'ao', 'f': 'la', 'n': 'lo'}[gender]

        part = self.part
        if suffix == 'ao':
            if self.part[len(self.part)-2:] == 'je':
                part = part[:len(part)-2]
                suffix = 'io'
            elif self.part[-1] in 'aeiour':
                suffix = 'o'
        part += suffix

        bi = Verb('biti', 'sam', 'bi', ('be', 'was', 'been'),'i')
        was = bi.present(person, number, gender)
        return ' '.join([pronoun, was[was.find(' ')+1:], part])

    def future_i(self, person: int, number: str, gender: str = 'm') -> str:
        """Future I: will + infinitive"""
        pronoun = {
            1: {'sg': 'Ja', 'pl': 'Mi'},
            2: {'sg': 'Ti', 'pl': 'Vi'},
            3: {'sg': {'m': 'On', 'f': 'Ona', 'n': 'Ono'}[gender],
                'pl': {'m': 'Oni', 'f': 'One', 'n': 'Ona'}[gender]},
        }[person][number]

        aux = Verb('htjeti','hoć','htj',('want','wanted','wanted'),'e')
        stem = aux.present(person, number)
        stem = stem[stem.find(' ')+3:]
        return ' '.join([pronoun, stem, self.inf])

    def future_ii(self, person: int, number: str, gender: str = 'm') -> str:
        """Future II (will have + past participle)"""
        future = Verb("Buditi", "Bud", "Bud", ("Doesn't", "Matter", "At all"), 'e').present(person, number, gender)
        components = future.split(' ')
        past = self.perfect(person, number, gender).split(' ')
        return ' '.join([components[0], components[1].lower(), past[2]])

    def conditional_i(self, person: int, number: str, gender: str = 'm') -> str:
        """Conditional I: would + past participle"""
        pronoun = {
            1: {'sg': 'Ja', 'pl': 'Mi'},
            2: {'sg': 'Ti', 'pl': 'Vi'},
            3: {'sg': {'m': 'On', 'f': 'Ona', 'n': 'Ono'}[gender],
                'pl': {'m': 'Oni', 'f': 'One', 'n': 'Ona'}[gender]},
        }[person][number]

        prefix = 'bi'

        past = self.perfect(person, number, gender)
        past = past[past.find(' ')+1:]
        past = past[past.find(' ') + 1:]

        return ' '.join([pronoun, prefix, past])

    def conditional_ii(self, person: int, number: str, gender: str = 'm') -> str:
        """Conditional II (would have + past participle)"""
        biti_past = Verb('biti','sam','bi',('be','was','been'),'i').perfect(person, number, gender)
        needed = biti_past.split(' ')[2]
        components = self.conditional_i(person, number, gender).split(' ')
        return ' '.join([components[0], components[1], needed, components[2]])

    def get_tense(self, person: int, number: str, gender: str, tense: str) -> str:
        """Returns the conjugation for the tense specified"""
        if tense == 'Present':
            return self.present(person, number)
        elif tense == 'Perfect':
            return self.perfect(person, number, gender)
        elif tense == 'Future I':
            return self.future_i(person, number)
        elif tense == 'Future II':
            return self.future_ii(person, number, gender)
        elif tense == 'Conditional I':
            return self.conditional_i(person, number, gender)
        elif tense == 'Conditional II':
            return self.conditional_ii(person, number, gender)
        else:
            return "Tense not found"

    def get_english(self, person: int, number: str, gender: str, tense: str) -> str:
        """Returns the English translation of the verb given its tense

        Precondition: gender == 'm', 'f', or 'n'
        """
        final = []
        if number == 'sg':
            final.append({
                             1: 'I',
                             2: 'You (sg)',
                             3: {'m': 'He', 'f': 'She', 'n': 'It'}[gender]
                         }[person])
        else:
            final.append({1: 'We', 2: 'You (pl)', 3: 'They'}[person])

        if "Future" in tense:
            final.append("will")
        elif "Conditional" in tense:
            final.append("would")
        elif tense == "Perfect":
            final.append("had")

        if tense == "Future II" or tense == "Conditional II":
            final.append("have")

        if tense == "Present" or " I" in tense and " II" not in tense:
            if tense != "Present":
                final.append(self.english[0])
            else:
                english = self.english[0]
                remainder = ''
                if ' ' in english:
                    remainder = english[english.find(' '):]
                    english = english[:english.find(' ')]

                if english == "be":
                    if number == 'sg':
                        english = {
                            1: 'am',
                            2: 'are',
                            3: 'is'
                        }[person]
                    else:
                        english = 'are'
                elif person == 3 and number == 'sg' and english != "may" and english != "can":
                    if english == "have":
                        english = "ha"
                    elif english[-1] in "ho":
                        english += 'e'
                    elif english[-1] == 'y' and english[len(english)-2] not in "aeiou":
                        english = english[:len(english)-1]
                        english += 'ie'
                    english += 's'
                final.append(english + remainder)
        else:
            final.append(self.english[2])

        return ' '.join(final)

    def all_conjugations(self) -> str:
        """Return a multi-line string listing every Croatian form of this verb."""
        tenses = [
            'Present',
            'Perfect',
            'Future I',
            'Future II',
            'Conditional I',
            'Conditional II'
        ]
        # which tenses need gender-specific forms:
        gendered = {
            'Present': False,
            'Future I': False,
            'Perfect': True,
            'Future II': True,
            'Conditional I': True,
            'Conditional II': True
        }

        lines = []
        for tense in tenses:
            lines.append(f"{tense}:")
            if gendered[tense]:
                # for gendered tenses, list m, f, n
                for number in ('sg', 'pl'):
                    for person in (1, 2, 3):
                        for gender in ('m', 'f', 'n'):
                            form = self.get_tense(person, number, gender, tense)
                            label = f"{person}{number}{gender}"
                            lines.append(f"  {label}: {form}")
            else:
                # non-gendered: just use 'm' internally to fetch, but label without gender
                for number in ('sg', 'pl'):
                    for person in (1, 2, 3):
                        form = self.get_tense(person, number, 'm', tense)
                        label = f"{person}{number}"
                        lines.append(f"  {label}: {form}")
            lines.append("")  # blank line between tenses
        return "\n".join(lines)

    def test_verbs(verbs: list['Verb'], person: int, number: str, gender: str, option: str):
        """Prints out the conjugations of all the verbs for the parameters specified

        For <option>,
        1: Present
        2: Past Perfect
        3: Future I
        4. Future II
        5. Conditional I
        6. Conditional II
        """
        if option == 'Present':
            for v in verbs:
                print(f"{v.inf:6s} → {str(person) + number} Present: {v.present(person, number)}")
        elif option == "Past Perfect":
            for v in verbs:
                print(
                    f"{v.inf:6s} → {str(person) + number} Past Perfect: {v.perfect(person, number, gender)}")
        elif option == "Future I":
            for v in verbs:
                print(f"{v.inf:6s} → {str(person) + number} Future I: {v.future_i(person, number)}")
        elif option == "Future II":
            for v in verbs:
                print(
                    f"{v.inf:6s} → {str(person) + number} Future II: {v.future_ii(person, number, gender)}")
        elif option == "Conditional I":
            for v in verbs:
                print(
                    f"{v.inf:6s} → {str(person) + number} Conditional I: {v.conditional_i(person, number, gender)}")
        elif option == "Conditional II":
            for v in verbs:
                print(
                    f"{v.inf:6s} → {str(person) + number} Conditional II: {v.conditional_ii(person, number, gender)}")
        else:
            print(option + " is not a valid option.")
