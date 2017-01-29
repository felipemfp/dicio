class Utils(object):
    @staticmethod
    def remove_tags(str):
        """
        Return a new string without html tags.

        >>> remove_tags("<a href='#'>Something</a>")
        'Something'
        """
        import re
        return re.sub('<[^>]*>', ' ', str).strip()

    @staticmethod
    def text_before(str, after):
        """
        Return text before after.

        >>> text_before("<a href='#'>Something</a>", "</a>")
        "<a href='#'>Something"
        """
        index = str.find(after)
        if index > -1:
            return str[:index]
        return str

    @staticmethod
    def text_after(str, before):
        """
        Return text after before.

        >>> text_after("<a href='#'>Something</a>", "<a href='#'>")
        'Something</a>'
        """
        index = str.find(before)
        if index > -1:
            index += len(before)
            return str[index:]
        return str

    @staticmethod
    def text_between(str, before, after, force_html = False):
        """
        Return text between before and after.
        Use force_html when before and after were html tags.

        >>> text_between("<a href='#'>Something</a>", "<a href='#'>", "</a>")
        'Something'
        """
        start = str.find(before)
        if start > -1:
            start += len(before)
        if force_html:
            if before[-1] != ">":
                start = str.find(">", start) + 1
        end = str.find(after, start)
        if force_html:
            if after[0] != "<":
                end = str.find("<", start)
        if -1 < start < end:
            return str[start:end]
        return str

    @staticmethod
    def remove_spaces(str):
        """
        Return a new string without double space, tabs, carriage return or line feed.

        >>> remove_spaces("Something  else")
        'Something else'
        """
        str = str.replace("\t", " ")
        str = str.replace("\n", " ")
        str = str.replace("\r", " ")
        while str.find("  ") > -1:
            str = str.replace("  ", " ")
        return str.strip()

    @staticmethod
    def remove_accents(str):
        """
        Return a new string without accents from portuguese

        >>> remove_accents("trava-língua")
        'trava-lingua'
        """
        encode = ["á", "à", "â", "ã", "ä",
                  "é", "è", "ê", "ë",
                  "í", "ì", "î", "ï",
                  "ó", "ò", "ô", "õ", "ö",
                  "ú", "ù", "û", "ü",
                  "ç"]

        decode = ["a", "a", "a", "a", "a",
                  "e", "e", "e", "e",
                  "i", "i", "i", "i",
                  "o", "o", "o", "o", "o",
                  "u", "u", "u", "u",
                  "c"]

        out = ""
        found = False

        for chr in str:
            for x, vgl in enumerate(encode):
                if chr == vgl:
                    out += decode[x]
                    found = True
                    break
                else:
                    found = False
            if not found:
                out += chr

        return out

    @staticmethod
    def split_html_tag(str, tag):
        """
        Return a list like split, but it uses html tags in various formats.

        >>> str = "Something<br>else<br />and<br/>another<br></br>thing"
        >>> split_html_tag(str, "br")
        ['Something', 'else', 'and', 'another', 'thing']
        """
        TEMPLATE = "<{0} />"
        templates = ["<{0}></{0}>",
                   "<{0}></ {0}>",
                   "<{0} ></{0}>",
                   "<{0} ></ {0}>",
                   "<{0}>",
                   "<{0}/>",
                   "<{0} >"]

        new_str = str
        for template in templates:
            new_str = new_str.replace(template.format(tag), TEMPLATE.format(tag))
        return list(filter(None, new_str.split(TEMPLATE.format(tag))))
