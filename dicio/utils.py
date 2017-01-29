class Utils(object):

    @staticmethod
    def remove_tags(html):
        """
        Return a new string without html tags.

        >>> remove_tags("<a href='#'>Something</a>")
        'Something'
        """
        import re
        return re.sub('<[^>]*>', ' ', html).strip()

    @staticmethod
    def text_before(text, after):
        """
        Return text before after.

        >>> text_before("<a href='#'>Something</a>", "</a>")
        "<a href='#'>Something"
        """
        index = text.find(after)
        if index > -1:
            return text[:index]
        return text

    @staticmethod
    def text_after(text, before):
        """
        Return text after before.

        >>> text_after("<a href='#'>Something</a>", "<a href='#'>")
        'Something</a>'
        """
        index = text.find(before)
        if index > -1:
            index += len(before)
            return text[index:]
        return text

    @staticmethod
    def text_between(text, before, after, force_html=False):
        """
        Return text between before and after.
        Use force_html when before and after were html tags.

        >>> text_between("<a href='#'>Something</a>", "<a href='#'>", "</a>")
        'Something'
        """
        start = text.find(before)
        if start > -1:
            start += len(before)
        if force_html:
            if before[-1] != ">":
                start = text.find(">", start) + 1
        end = text.find(after, start)
        if force_html:
            if after[0] != "<":
                end = text.find("<", start)
        if -1 < start < end:
            return text[start:end]
        return text

    @staticmethod
    def remove_spaces(text):
        """
        Return a new string without double space, tabs, carriage return
        or line feed.

        >>> remove_spaces("Something  else")
        'Something else'
        """
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        while text.find("  ") > -1:
            text = text.replace("  ", " ")
        return text.strip()

    @staticmethod
    def remove_accents(text):
        """
        Return a new string without accents from portuguese

        >>> remove_accents("trava-língua")
        'trava-lingua'
        """
        reference = [
            ('a', 'áàâãä'),
            ('e', 'éèêë'),
            ('i', 'íìîï'),
            ('o', 'óòôõö'),
            ('u', 'úùûü'),
            ('c', 'ç')
        ]

        new_text = ""
        for char in text:
            found = False
            for clear_vowal, possible_accents in reference:
                if char in possible_accents:
                    new_text += clear_vowal
                    found = True
                    break
            if not found:
                new_text += char
        return new_text

    @staticmethod
    def split_html_tag(text, tag):
        """
        Return a list like split, but it uses html tags in various formats.

        >>> str = "Something<br>else<br />and<br/>another<br></br>thing"
        >>> split_html_tag(str, "br")
        ['Something', 'else', 'and', 'another', 'thing']
        """
        import re
        expression = '<[^>]*{0}[^>]*>'.format(tag)
        return list(filter(None, re.split(expression, text)))
